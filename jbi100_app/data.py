import pandas as pd
from time import time
from functools import lru_cache
import sys
from jbi100_app.config import casualty_data, vehicle_data, accident_data

# Sampling rate tells us how many rows of the data to skip.
# Counts and costs are then scaled back up by this rate.
# For testing make this higher, for final presentation set it lower.
SAMPLING_RATE = 20

@lru_cache(None)
def get_data():
    start = time()
    print("Reading the data")
    cost_data = 'data/ras60001.ods'
    cost_df = pd.read_excel(cost_data, sheet_name=None, header=7)

    # severities: 1 = fatal, 2 = serious, 3 = slight
    def cost_by_year_casualty(year: int, severity: int):
        return cost_df[str(year)]['Cost per casualty'][severity - 1]

    print(f"sanity check: cost of fatal casualty in 2011 is {cost_by_year_casualty(2011, 1):.2f}")

    try:
        casualty_df = pd.read_csv(casualty_data)
    except FileNotFoundError:
        print('Casualty data not found! Please download it to the data/ folder.')
        print(f'expected path is {casualty_data}')
        print(
            'url: https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-casualty-1979-2020.csv')
        sys.exit(1)
    casualty_df = casualty_df[
        # since we only have costs since 2010, drop all data from before it
        (casualty_df['accident_year'] >= 2010) &
        # apply sampling rate (to make it faster, maybe reset to 1 in final report)
        (casualty_df.index % SAMPLING_RATE == 1)
        ]
    # augment each row with a cost value based on severity
    casualty_df['cost'] = casualty_df.apply(
        lambda row: SAMPLING_RATE * cost_by_year_casualty(row['accident_year'], row['casualty_severity']), axis=1)

    try:
        accident_df = pd.read_csv(accident_data)
    except FileNotFoundError:
        print('Accident data not found! Please download it to the data/ folder.')
        print(f'expected path is {accident_data}')
        print(
            'url: https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-accident-1979-2020.csv')
        sys.exit(1)

    # remove the row for 2016210132254 because it has NULL speed limit
    bad_index = accident_df[accident_df['accident_index'] == '2016210132254'].index
    accident_df = accident_df.drop(bad_index)
    # first, drop the columns that conflict from the accident table
    accident_df = accident_df.drop('accident_year', axis=1)
    accident_df = accident_df.drop('accident_index', axis=1)
    # then, merge all the columns of accidents into casualties
    # https://pandas.pydata.org/docs/user_guide/merging.html#
    merged = pd.merge(
        casualty_df,
        accident_df,
        how="inner",
        on='accident_reference',
    )

    try:
        vehicle_df = pd.read_csv(vehicle_data)
    except FileNotFoundError:
        print('Vehicle data not found! Please download it to the data/ folder.')
        print(f'expected path is {vehicle_data}')
        print(
            'url: https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-vehicle-1979-2020.csv')
        sys.exit(1)
    vehicle_df = vehicle_df[
        (vehicle_df.index % SAMPLING_RATE == 1) &
        (vehicle_df['accident_year'] >= 2010)
        ]
    # "cost" is the value that's summed in the area chart, so here it's just a count
    vehicle_df['cost'] = SAMPLING_RATE

    # TODO: remove accident_df entirely
    return merged, vehicle_df, accident_df


# function that enables faster testing due to less pre-computation
@lru_cache(None)
def test_data():
    start = time()
    print("Reading the data")
    cost_data = 'data/ras60001.ods'
    cost_df = pd.read_excel(cost_data, sheet_name=None, header=7)

    # severities: 1 = fatal, 2 = serious, 3 = slight
    def cost_by_year_casualty(year: int, severity: int):
        return cost_df[str(year)]['Cost per casualty'][severity - 1]

    print(f"sanity check: cost of fatal casualty in 2011 is {cost_by_year_casualty(2011, 1):.2f}")

    try:
        casualty_df = pd.read_csv(casualty_data)
    except FileNotFoundError:
        print('Casualty data not found! Please download it to the data/ folder.')
        print(f'expected path is {casualty_data}')
        print(
            'url: https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-casualty-1979-2020.csv')
        sys.exit(1)
    casualty_df = casualty_df[
        # since we only have costs since 2010, drop all data from before it
        (casualty_df['accident_year'] >= 2010) &
        # apply sampling rate (to make it faster, maybe reset to 1 in final report)
        (casualty_df.index % SAMPLING_RATE == 1)
        ]
    # augment each row with a cost value based on severity
    casualty_df['cost'] = casualty_df.apply(
        lambda row: SAMPLING_RATE * cost_by_year_casualty(row['accident_year'], row['casualty_severity']), axis=1)
    print(f"Done reading data in {time() - start:.2f}s")
    return casualty_df

