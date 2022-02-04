from functools import lru_cache
from time      import time
from pandas    import read_pickle

@lru_cache(None)
def get_data():
    path = 'data/merged.pkl.gz'
    print(f'Reading {path}... ', end='')

    start_time = time()
    df = read_pickle(path)
    end_time = time()

    print(f'done! ({end_time - start_time:.2f} seconds.)')

    SAMPLING_RATE = None
    while not type(SAMPLING_RATE) is int:
        SAMPLING_RATE = int(input('Please provide a sampling rate: '))

    print(f'Sampling... ', end='')

    start_time = time()
    df = df[df.index % SAMPLING_RATE == 1]
    end_time = time()

    print(f'done! ({end_time - start_time:.2f} seconds.)')
    return df

@lru_cache(None)
def test_data():
    return read_pickle(f'data/casualty-final.pkl.gz')