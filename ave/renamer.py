#%%
import pandas as pd
non_cat = {
    'accident': [
        'accident_index',
        'accident_year',
        'accident_reference',
        'location_easting_osgr',
        'location_northing_osgr',
        'longitude',
        'latitude',
        'number_of_vehicles',
        'number_of_casualties',
        'date',
        'time',
        'first_road_number',
        # speed_limit is actually categorical!
        'second_road_number'
    ],
    'vehicle': [
        'accident_index',
        'accident_year',
        'accident_reference',
        'vehicle_reference'
    ],
    'casualty': [
        'accident_index',
        'accident_year',
        'accident_reference',
        'vehicle_reference',
        'casualty_reference',
        'age_of_casualty'
    ]
}

#%%
"""
    Excel sheet had to modified, as vehicle_direction_from had a typo.
    Also vehicle_direction_to!
    (South East appears twice, had to be changed to South.)
"""
index = pd.read_excel('Road-Safety-Open-Dataset-Data-Guide.xlsx')

# %%
dfs = {}
for sub in non_cat.keys():
    dfs[sub] = pd.read_pickle(f'{sub}-stage3.pkl.gz')

#%%
for sub in non_cat.keys():
    df = dfs[sub]
    for col in df.columns:
        if col in non_cat[sub]: continue
        Sub = sub[0].upper() + sub[1:]

        i_df = index[index['table'] == Sub]
        i_df = i_df[index['field name'] == col]
        i_map = {row['code/format']: row['label'] for _, row in i_df.iterrows()}

        print(i_map)

        df[col] = df[col].astype('category')
        df[col] = df[col].cat.rename_categories(i_map)    
    dfs[sub] = df

#%%
dfs['merged'] = pd.merge(
    dfs['casualty'],
    dfs['accident'],
    how='inner',
    on='accident_reference',
)

#%%
from time import time
for sub in dfs.keys():
    path = f'{sub}-final.pkl.gz'
    print(f'Pickling {path}... ', end='')
    start = time()
    pd.to_pickle(dfs[sub], path)
    print(f'done! ({time() - start:.2f} seconds.)')

# %%
