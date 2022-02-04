from functools import lru_cache
from time      import time
from pandas    import read_pickle

# lru_cache returns the last result of get_data(). This way, it is not loaded
# twice.
@lru_cache(None)
def get_data():
    # load the pickled Dataframe
    path = 'data/merged.pkl.gz'
    print(f'Reading {path}... ', end='')

    # time and display how long loading took
    start_time = time()
    df = read_pickle(path)
    end_time = time()

    print(f'done! ({end_time - start_time:.2f} seconds.)')

    # prompt the user for their desired sampling rate
    SAMPLING_RATE = None
    while not type(SAMPLING_RATE) is int:
        SAMPLING_RATE = int(input('Please provide a sampling rate: '))

    # drop rows from the dataframe depending on the sampling rate
    # keep a timer to display how long the computation took
    print(f'Sampling... ', end='')

    start_time = time()
    df = df[df.index % SAMPLING_RATE == 1]
    end_time = time()

    print(f'done! ({end_time - start_time:.2f} seconds.)')
    return df

@lru_cache(None)
def test_data():
    return read_pickle(f'data/casualty-final.pkl.gz')