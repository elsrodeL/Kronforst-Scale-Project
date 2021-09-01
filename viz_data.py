"""viz_data.py

Functions to Visualize the Data

    SCALE PROJECT -- KRONFORST LABORATORY AT THE UNIVERSITY OF CHICAGO 
                  -- ALL RIGHTS RESERVED 
        
        Lukas Elsrode - Undergraduate Researcher at the Kronforst Laboratory wrote and tested this code 
        (09/01/2021)
        
"""
import scale_data as data
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.decomposition import PCA
from scale_data import segment_df_by_field


DEF_FEATURES = [
    'lacuna_area_window',
    'lacuna_perimeter',
    'lacuna_circularity',
    'crossrib_thickness',
    'ridge_to_ridge_distance',
    'trabernaculae_length',
    'ridge_elevation'
]


def make_title(df):
    """ Make the Title for what all entries in this dataset have in common
            e.g if data comprised of all Nymphalids that are Black >> nymphalidia black

                Inputs:
                    ('Pandas.DataFrame' Object Class) - 'df' : The DataSet used 
                Outputs:
                    (string)  - The unifying common family & color which unites our dataset
    """
    # Get Every Possible Entry
    s = [i for i in set(df['species'].values)]
    g = [i for i in set(df['genus'].values)]
    t = [i for i in set(df['tribe'].values)]
    sf = [i for i in set(df['subfamily'].values)]
    f = [i for i in set(df['family'].values)]
    c = [i for i in set(df['scale_color'].values)]
    # All Possible Values
    vals = [s, g, t, sf, f, c]
    # Values for which their exists only 1 type of entry
    singles = [i[0] for i in vals if len(i) == 1]
    # One thing units data
    if len(singles) == 1:
        return singles[0]
    # If Not Diffrent by color then just get the Closest Family
    if len(singles) > 1 and singles[-1] not in c:
        return singles[0]
    # Return Family and Color
    elif len(singles) > 1 and singles[-1] in c:
        return singles[0] + ' ' + singles[-1]

    return 'Raw Data'

def feature_distribution(df, feature='scale_color', segby='f'):
    """Shows Distributions of Measurements at the 'segby' level grouped by 'feature'

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df' : DataFrame to plot our Morphometric measurements
            (string) - 'feature' : What The Classes should be split up by 
            (string) - 'segby': By What Class attribute in the Column of the dataset should the data be split up by

        Outputs:
            (None) - Plots Box Plots of Features
    """
    dfs = segment_df_by_field(df, segby)
    measurements = DEF_FEATURES
    for df_ in dfs:
        for m in measurements:
            g = sns.violinplot(x=feature, y=m, data=df_, width=0.7)
            t = m + ' ' + 'distribution ' + 'for' + ' ' + make_title(df_)
            g.set(title=t)
            plt.show()
    return

def run_viz_by_field(df, foo, c_map, field, segby='f'):
    """Recursively runs through vizulization function 'foo' to our data segmented 'df' 
    by a group 'f', running each vizulization obeserving variable 'field' and applies a 
    color mapping 'c_map' to those visualization.

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df' : DataFrame to plot our Morphometric measurements
            ('Function' Python Object Class) - 'foo' : funtion in viz_data.py that takes a 'color mapping' and 'field' as inputs
            (Dictionary) - 'c_map': Dictionary Mapping Field values to the color descriptions for the Visulizations
            (string) - 'field': What Variable to classify the plot against i.e 'scale_color'
            (string) - what to segment the data by i.e 'f'- by family 
    
        Outputs:
            (None) - Plots Viszilizations 

    """

    if segby == None:
        foo(df, c_map=c_map, field=field)

    else:
        l_df = segment_df_by_field(df, segby)

        for d in l_df:
            foo(d, c_map=c_map, field=field)
    return


def show_originaldim(df, c_map, features=DEF_FEATURES, field='scale_color'):
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
    df_n, X = resize_data(df, features, field)
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


def mk_subset_of_PC_components(df, c_map, N=4, features=DEF_FEATURES, field='scale_color'):

    df_n, X = resize_data(df, features, field)

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


def mk_explained_variance_curve(df, features=DEF_FEATURES, field='scale_color'):

    df_n, X = resize_data(df, features, field)
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


def Load_Features(df, c_map, features=DEF_FEATURES, field='scale_color'):

    df_n, X = resize_data(df, features, field)

    if type(df_n) != int:
        pca = PCA(n_components=2)
        components = pca.fit_transform(X)
        loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

        fig = px.scatter(components, x=0, y=1, title=make_title(df), labels={
                         '0': 'PC1', '1': 'PC2'}, color=df_n[field], color_discrete_map=c_map)

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


def resize_data(df, features, field):
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
