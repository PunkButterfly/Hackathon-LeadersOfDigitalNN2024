from datetime import datetime as dt
import streamlit as st
import streamlit.components.v1 as components

import os
import folium
import geopandas as gpd

def draw_map(dataframe, selected_column):

    path_to_data = "./data/"

    russia_regions = gpd.read_file(os.path.join(path_to_data, "russia_regions.geojson"))

    okato2mapid = {54: 0, 86: 1, 93: 2, 38: 3, 18: 4, 4: 5, 66: 6, 1: 7, 95: 8, 14: 9, 35: 10,
                                78: 11, 94: 12, 82: 13, 99: 14, 87: 15, 46: 16, 84: 17, 53: 18, 52: 19, 61: 20,
                                79: 21, 89: 22, 44: 23, 80: 24, 41: 25, 69: 26, 81: 27, 32: 28, 33: 29, 28: 30,
                                75: 31, 3: 32, 27: 33, 24: 34, 42: 35, 88: 36, 22: 37, 40: 38, 70: 39, 34: 40,
                                56: 41, 58: 42, 36: 43, 49: 44, 68: 45, 85: 46, 11: 47, 37: 48, 17: 49, 98: 50,
                                25: 51, 65: 52, 19: 53, 50: 54, 71: 55, 76: 56, 64: 57, 47: 58, 90: 59, 73: 60,
                                8: 61, 30: 63, 57: 65, 63: 66, 83: 67, 20: 68, 91: 69, 10: 70, 15: 71, 97: 72,
                                60: 74, 5: 75, 67: 76, 92: 77, 29: 78, 12: 79, 7: 80, 26: 81, 45: 82, 96: 83,
                                77: 84}

    m = folium.Map(location=[63.391522, 96.328125], zoom_start=3, tiles="cartodb positron", attr="Punk Butterfly", attributionControl=0)

    dataframe['id'] = dataframe['okato'].map(okato2mapid).astype(int)
    dataframe = dataframe.rename(columns={selected_column: "values"})

    folium.Choropleth(
        geo_data=russia_regions,
        name='Регионы России',
        data=dataframe,
        columns=['id', 'values'],
        key_on='feature.properties.id',
        bins=5,
        fill_color='YlOrRd',
        nan_fill_color='gray',
        nan_fill_opacity=0.2,
        # fill_opacity=0.7,
        line_opacity=0.2,
        # legend_name='Регионы России',
        highlight=True,
        show=True,
    ).add_to(m)

    m.save(os.path.join(path_to_data, "map.html"))

    components.html(open(os.path.join(path_to_data, "map.html"), 'r', encoding='utf-8').read(), height=500)
