# Lukas Elsrode - viz_data.py (11/04/2020)

'''
Functions to Vizulize the Data

'''

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
from scale_data import segment_df_by_field


DEF_FEATURES = ['lacuna_area_window', 'lacuna_perimeter', 'lacuna_circularity','crossrib_thickness', 'ridge_to_ridge_distance']

def make_title(df):

    s = [i for i in set(df['species'].values)]
    g = [i for i in set(df['genus'].values)]
    t = [i for i in set(df['tribe'].values)]
    sf = [i for i in set(df['subfamily'].values)]
    f = [i for i in set(df['family'].values)]
    c = [i for i in set(df['scale_color'].values)]

    vals = [s, g, t, sf, f, c]

    singles = [i[0] for i in vals if len(i) == 1]

    if len(singles) == 1:
        return singles[0]

    if len(singles) > 1 and singles[-1] not in c:
        return singles[-1]

    elif len(singles) > 1 and singles[-1] in c:
        return singles[0] + ' ' + singles[-1]

def feature_distrobution(df,class_='scale_color',feature='family'):
    measurements = DEF_FEATURES
    for m in measurements:
        g = sns.catplot(data=df,hue=feature,kind="box",x=class_,y=m)
        t = m + ' ' + 'distrobution at the' + ' ' + feature + ' ' + 'level' + ' ' + 'grouped by' + ' ' + class_
        g.set(title=t)
        plt.show()
    return

def run_viz_by_field(df, foo, c_map, field, segby='f'):
    ''' Recursively runs through vizulizations of our data segmented by a group
    '''

    if segby == None:
        foo(df,c_map = c_map, field=field)

    else:
        l_df = segment_df_by_field(df, segby)

        for d in l_df:
            foo(d, c_map = c_map, field=field)
    return

def show_originaldim(df,c_map,features=DEF_FEATURES,field='scale_color'):
    '''Shows original feature distrobution of our dataset
    '''

    fig = px.scatter_matrix(
        df,
        dimensions=features,
        color=field,
        title=make_title(df),
        color_discrete_map=c_map
    )


    fig.update_traces(diagonal_visible=False)
    fig.show()

    return

def PCA_2D(df, c_map, features=DEF_FEATURES, field='scale_color'):
    '''Makes a Two component PCA of data given
    '''
    df_n, X = resize_data(df, features, field)
    if type(df_n) != int:
        pca = PCA(n_components=2)
        components = pca.fit_transform(X)
        fig = px.scatter(
            components, x=0, y=1, color=df_n[field],
            title='2-Component PCA',
            labels={'0': 'PC1', '1': 'PC2'},
            color_discrete_map=c_map)
        fig.show()
    return

def PCA_3D(df, c_map, features=DEF_FEATURES, field='scale_color'):
    '''Makes a Three component PCA of data given
    '''
    df_n, X=resize_data(df, features, field)
    if type(df_n) != int:

        pca = PCA(n_components=3)
        components = pca.fit_transform(X)
       
        fig = px.scatter_3d(
            components, x=0, y=1, z=2, color=df_n[field],
            title='3-Component PCA',
            labels={'0': 'PC1', '1': 'PC2', '2': 'PC3'},
            color_discrete_map=c_map
        )
        fig.show()
        return

def mk_subset_of_PC_components(df,c_map,N=4,features=DEF_FEATURES,field='scale_color'):

    df_n, X = resize_data(df,features,field)

    if type(df_n) != int:
        # make a high dimentional reduction to explain as much variance as possible
        pca = PCA(n_components=N)
        components = pca.fit_transform(X)

        total_var = pca.explained_variance_ratio_.sum() * 100

        labels = {str(i): f"PC {i+1}" for i in range(N)}
        labels['color'] = field

        fig = px.scatter_matrix(
            components,
            color=df_n[field],
            dimensions=range(N),
            labels=labels,
            title=f'Total Explained Variance: {total_var:.2f}%',
            color_discrete_map=c_map
        )
        fig.update_traces(diagonal_visible=False)
        fig.show()
    return

def mk_explained_variance_curve(df,features=DEF_FEATURES,field='scale_color'):

    df_n, X = resize_data(df,features,field)
    if type(df_n) != int:

        pca = PCA()
        pca.fit(X)

        exp_var_cumul = np.cumsum(pca.explained_variance_ratio_)
        fig = px.area(
            x=range(1, exp_var_cumul.shape[0] + 1),
            y=exp_var_cumul,
            labels={"x": "# Components", "y": "Explained Variance"}
        )
        print(make_title(df))
        fig.show()
    return

def Load_Features(df,c_map,features=DEF_FEATURES,field='scale_color'):

    df_n, X = resize_data(df,features,field)

    if type(df_n) != int:
        pca = PCA(n_components=2)
        components = pca.fit_transform(X)
        loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

        fig = px.scatter(components, x=0, y=1, title= make_title(df), labels={'0': 'PC1', '1': 'PC2'} , color=df_n[field], color_discrete_map=c_map)


        for i, feature in enumerate(features):
            fig.add_shape(
                type='line',
                x0=0, y0=0,
                x1=loadings[i, 0],
                y1=loadings[i, 1]
            )
            fig.add_annotation(
                x=loadings[i, 0],
                y=loadings[i, 1],
                ax=0, ay=0,
                xanchor="center",
                yanchor="bottom",
                text=feature,
            )
        fig.show()
    return

def resize_data(df,features,field):
    r = features + [field]
    df_n = df[r]
    df_n = df_n.dropna()
    X = df_n[features]
    M = X.to_numpy()
    n, _ = M.shape

    # Stoping condition if no PCA can be made
    if n <= 0:
        return 0
    else:
        return df_n, X
