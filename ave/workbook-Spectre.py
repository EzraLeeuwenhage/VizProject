#%%
import pandas as pd
import time

"""
casualty:
        0 accident_index
        2 accident_reference

accident:
        0 accident_index
        2 accident_reference
        15 local_authority_ons_district
        16 local_authority_highway     
        35 lsoa_of_accident_location   

vehicle:
        0 accident_index
        2 accident_reference
        24 generic_make_model
"""

#%%
subs = ['casualty', 'accident', 'vehicle']
dfs = {sub: pd.read_pickle(f'{sub}-stage2.pkl.gz') for sub in subs}
"""
for sub in subs:
    df = dfs[sub]
    #print(df.select_dtypes(include='object').head())

    uhh = df.select_dtypes(include='object').head()
    uhh = uhh.apply(lambda s: [print(type(x)) for x in s])#, axis=1)
    #print(uhh)
"""
"""
print(sub + ':')
for i, name in enumerate(df.columns):
    if sub == 'casualty' and (i == 0 or i == 2):
        print(f'\t{i} {name}')
    if sub == 'accident' and i in [0,2,15,16,35]:
        print(f'\t{i} {name}')
    if sub == 'vehicle' and i in [0,2,24]:
        print(f'\t{i} {name}')
print()
"""
                                 
#%%
def stage2():
    for sub in ['casualty', 'accident', 'vehicle']:
        start_time = time.time()
        df = pd.read_pickle(f'{sub}-stage1.pkl.gz')
        print(f'read {sub} pkl in {time.time() - start_time} seconds.')
        if sub == 'casualty':
            cost_data = '../data/ras60001.ods'
            cost_df = pd.read_excel(cost_data, sheet_name=None, header=7)

            # severities: 1 = fatal, 2 = serious, 3 = slight
            def cost_by_year_casualty(year: int, severity: int):
                return cost_df[str(year)]['Cost per casualty'][severity - 1]

            print(f"sanity check: cost of fatal casualty in 2011 is {cost_by_year_casualty(2011, 1):.2f}")

            df['cost'] = df.apply(lambda row: 1 * cost_by_year_casualty(row['accident_year'], row['casualty_severity']), axis=1)
        print('compression and writing...')
        df.to_pickle(f'{sub}-stage2.pkl.gz')

#%%
"""
TODO: check import warnings

* casualty
DtypeWarning: Columns (0,2) have mixed types.Specify dtype option on import or set low_memory=False.

* accident
DtypeWarning: Columns (0,2,15,16,35) have mixed types.Specify dtype option on import or set low_memory=False.

* vehicle
DtypeWarning: Columns (0,2,24) have mixed types.Specify dtype option on import or set low_memory=False.

"""
def stage1():
    for sub in ['casualty', 'accident', 'vehicle']:
        path = f'../data/dft-road-casualty-statistics-{sub}-1979-2020.csv'
        print('reading csv...')
        df = pd.read_csv(path)
        print('editing df...')
        df = df[(df['accident_year'] >= 2010)]
        print('compression and writing...')
        df.to_pickle(f'{sub}-stage1.pkl.gz')
        print('done!')

#%%
def test1():
    start = time.time()
    df = pd.read_csv('../data/dft-road-casualty-statistics-casualty-2020.csv')
    print(f'CSV: {time.time() - start} seconds.')

    df.to_pickle('./comppickled.xz')
    
    start = time.time()
    df = pd.read_pickle('./comppickled.xz')
    print(f'XZ PKL: {time.time() - start} seconds.')

    df.to_pickle('./comppickled.gz')

    start = time.time()
    df = pd.read_pickle('./comppickled.gz')
    print(f'GZ PKL: {time.time() - start} seconds.')

    df.to_pickle('./comppickled.zstd')

    start = time.time()
    df = pd.read_pickle('./comppickled.zstd')
    print(f'ZSTD PKL: {time.time() - start} seconds.')

    df.to_pickle('./comppickled.bz2')

    start = time.time()
    df = pd.read_pickle('./comppickled.bz2')
    print(f'BZ2 PKL: {time.time() - start} seconds.')

    df.to_pickle('./pickled.pkl', compression=None)

    start = time.time()
    df = pd.read_pickle('./pickled.pkl')
    print(f'Uncompressed PKL: {time.time() - start} seconds.')

stage3()