import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from shapely.wkt import loads
import matplotlib.pyplot as plt
import seaborn as sns

def processing(files, var):
    '''
    :param files: list object with the file names.
    :return: concated geodataframe with reference system 3857
    '''
    # list to store the data frames
    dfs = []
    for f in files:
        # Import df with the geometry_column
        df = gpd.read_file(f, engine='pyogrio')

        # Convert WKT geometries to Shapely geometries and assign to 'geometry' column
        df = df.assign(geometry=loads(df['geometry_x']))

        # Transform to long, drop corrupt columns, and transform into metric system
        df = gpd.GeoDataFrame(df, geometry='geometry', crs=4346)
        # assign city code
        df['city'] =f.split('_')[-1].split('.')[0]

        dfs.append(df)

    # Concatenate DataFrames along axis 0 (indexes)
    df_conc = gpd.GeoDataFrame(pd.concat(dfs, ignore_index=True), crs=dfs[0].crs)

    # Transform to long, drop corrupt columns, and transform into metric system
    df_conc.drop(['geometry_x', 'geometry_y', 'pos', 'road', 'limit', 'lanes'], inplace=True, axis =1)

    # Set ID
    df_conc.set_index('detid', inplace=True)

    # change the dtype of the par_vars
    for p in var:
        df_conc[p] = df_conc[p].astype(float)

    df_conc['city'] = df_conc['city'].astype(str)

    return df_conc


def var_inf_calc(df, var):
    collect ={}
    df_g = df.groupby('city')
    for c, data in df_g:
        var_inf = [variance_inflation_factor(data[var], j) for j in range(data[var].shape[1])]
        collect[c] = var_inf

    return pd.DataFrame(collect)








