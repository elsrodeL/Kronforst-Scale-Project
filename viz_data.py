""" viz_data.py

Functions to Visualize the Data

    SCALE PROJECT -- KRONFORST LABORATORY AT THE UNIVERSITY OF CHICAGO
                  -- ALL RIGHTS RESERVED

        Lukas Elsrode - Undergraduate Researcher at the Kronforst Laboratory wrote and tested this code
        (10/11/2021)

"""
import itertools
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.decomposition import PCA
from scale_data import segment_df_by_field
from copy import deepcopy

# These are the default morphometric features of our ultra-structures of diffrent scales
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
            (None) - Plots Violin Plots of Features
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
    """Recursively runs through visualization function 'foo' to our data segmented 'df'
    by a group 'f', running each visualization observing variable 'field' and applies a
    color mapping 'c_map' to those visualization.

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df' : DataFrame to plot our Morphometric measurements
            ('Function' Python Object Class) - 'foo' : function in viz_data.py that takes a 'color mapping' and 'field' as inputs
            (Dictionary) - 'c_map': Dictionary Mapping Field values to the color descriptions for the Visulizations
            (string) - 'field': What Variable to classify the plot against i.e 'scale_color'
            (string) - what to segment the data by i.e 'f'- by family

        Outputs:
            (None) - Plots Visualizations

    """

    if segby == None:
        foo(df, c_map=c_map, field=field)

    else:
        l_df = segment_df_by_field(df, segby)

        for d in l_df:
            foo(d, c_map=c_map, field=field)
    return


def show_originaldim(df, c_map, features=DEF_FEATURES, field='scale_color'):
    """Shows original feature distribution of our dataset
    Plots all the diffrent included features and maps the color using a color map.

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df' : DataFrame to plot our Morphometric measurements
            (Dictionary) - 'c_map': Dictionary Mapping Field values to the color descriptions for the Visulizations
            (List of Strings) - 'features': the column names for the morphometric measurements to be examined
            (String) - 'field': By what column is the data divided by
        Outputs:
            (None)
    """

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


def PCA_3D(df, c_map, features=DEF_FEATURES, field='scale_color'):
    """ Makes a 3-component PCA of data given, Dimensional Reduction to 3 dimensions

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df': The DataFrame to plot our morphometric measurements
            (Dictionary) - 'c_map': Dictionary Mapping Field values to the color descriptions for the Visualizations
            (List of Strings) - 'features': the column names for the morphometric measurements to be examined
            (String) - 'field': What is the target variable in the dataset
        Outputs:
            (None)
    """
    df_n, X = resize_data(df, features, field)
    if type(df_n) != int:

        pca = PCA(n_components=3)
        components = pca.fit_transform(X)
        print_axis_components(pca, features)
        fig = px.scatter_3d(
            components, x=0, y=1, z=2, color=df_n[field],
            title='3-Component PCA',
            labels={'0': 'PC1', '1': 'PC2', '2': 'PC3'},
            color_discrete_map=c_map
        )
        fig.show()
        return


def print_axis_components(pca, features):
    """ For a PCA model list the number of components and show the normalized wheights of each of the features.

        Inputs:
            ('sklearn.decomposition._pca.PCA' Object Class) - 'pca' : The principle component axes
            (List of Strings) - 'features': The column names of the features making up the axes
        Outputs:
            (None)

    """
    for i, paxis in enumerate(pca.components_):
        print(f"~ PC{str(i+1)} ~")
        for j, comp in enumerate(paxis):
            print(f"{features[j]} : {comp}")
        print('\n')


def mk_explained_variance_curve(df, features=DEF_FEATURES, field='scale_color'):
    """ Given The Data Set and features how much vairance is explaied per number of principle of component
        axes added

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df': The DataFrame to plot our morphometric measurements
            (List of Strings) - 'features': the column names for the morphometric measurements to be examined
            (String) - 'field': What is the target variable in the dataset
        Outputs:
            (None)
    """
    df_n, X = resize_data(df, features, field)
    if type(df_n) != int:

        pca = PCA()
        pca.fit(X)

        exp_var_cumul = np.cumsum(pca.explained_variance_ratio_)
        fig = px.area(
            x=range(1, exp_var_cumul.shape[0] + 1),
            y=exp_var_cumul,
            labels={"x": "# Components", "y": "Explained Variance"},
            title=make_title(df)
        )
        fig.show()
    return


def Load_Features(df, c_map, features=DEF_FEATURES, field='scale_color'):
    """ Creates a 2D PCA and Shows you the vector components of features to each axis.

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df': The DataFrame to plot our morphometric measurements
            (Dictionary) - 'c_map': Dictionary Mapping Field values to the color descriptions for the Visulizations
            (List of Strings) - 'features': the column names for the morphometric measurements to be examined
            (String) - 'field': What is the target variable in the dataset
        Outputs:
            (None)
    """
    df_n, X = resize_data(df, features, field)
    if type(df_n) != int:
        pca = PCA(n_components=2)
        components = pca.fit_transform(X)
        print_axis_components(pca, features)
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
    """ Given DataSet with a field to be determined from Features drop any rows which have missing feature inputs

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df': The DataFrame to plot our morphometric measurements
            (List of Strings) - 'features': the column names for the morphometric measurements to be examined
            (String) - 'field': What is the target variable in the dataset
        Outputs:
            (tuple) - 'df_n', 'X' : The new resized data, the indicator variables columns from the resized data
    """
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


# GET ALL POSSIBLE SUBSETS OF FEATURES
def get_all_possible_combinations(features=DEF_FEATURES):
    """ Get a list of all the possible subsets of features from containing none [] to all features [x0,x1,...,xn]

        Inputs:
            (List) - 'features': A list of the morphological features which could be ploted in one plane (i.e 'DEF_FEATURES')
        Outputs:
            (List) - 'features_all_combinations': A list of all the possible subsets of the original features list (i.e [[],[x0],[x1,x0],[x0,x2],...,[x0,x1,...,xn])
    """
    features_all_combinations = []
    for N in range(0, len(features)+1):
        for feat_subset in itertools.combinations(features, N):
            features_all_combinations.append(list(feat_subset))
    return features_all_combinations


# GET THE BEST POSSIBLE FEATURE SET AND DISPLAY IT
def optimize_feature_set(df, c_map, min_num_features=2, field='scale_color', components=2):
    """ Return The best Set of  Features given the input feature sets and the desired data

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df': The DataFrame to plot our morphometric measurements
            (Dictionary) - 'c_map': Dictionary Mapping Field values to the color descriptions for the Visulizations
            (Int) - 'min_num_features' : The minimum number of Features the PCA axes can be constructed from
            (components) - 'components': The number of components the PCA can have.
        Outputs:
            (List of Strings) - Best Feature Sub-Set given selection methedology
    """
    assert components in set(
        [2, 3]), 'Reductions above 3 dimensions and below 2 dimensions are not possible '
    # Change Up the conditions so our Data is still Meaningful
    feature_sets = get_all_possible_combinations()
    feature_sets = [x for x in feature_sets if len(x) >= min_num_features]
    # Get a way to store ~ (feature_list,pca_explained_vairance_ratio)
    rv = [None]*len(feature_sets)
    # Fill rv[i] with values of explained variance score of feature_sets[i]
    for i, fset in enumerate(feature_sets):
        try:
            # Here we generate the 'Samples Data', 'Wilde Type Data', and  'Mutant Data'
            data = deepcopy(df)
            df_n, X = resize_data(data, fset, field)
            if type(df_n) != int:
                pca = PCA(n_components=components)
                pca.fit_transform(X)
                score = round(sum(list(pca.explained_variance_ratio_))*100, 2)
                entry = fset, score
                rv[i] = entry
        except:
            entry = fset, 0.0
            rv[i] = entry
            continue

    # get the key in the (k,v) pair tuples filling rv with lambda
    best_entry = max(rv, key=lambda i: i[1])
    best_features, _ = best_entry

    # Run appropriate visualizations
    if components == 2:
        # Show The Loaded PCA
        Load_Features(df, c_map, best_features, field)

    else:
        # Show a 3D model PCA
        PCA_3D(df, c_map, best_features, field)

    print('\n')
    # Show How Explained Variance Grows with added axes
    mk_explained_variance_curve(df, best_features, field)
    return best_features
