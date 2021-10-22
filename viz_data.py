""" viz_data.py

Functions to Visualize the Data

    SCALE PROJECT -- KRONFORST LABORATORY AT THE UNIVERSITY OF CHICAGO
                  -- ALL RIGHTS RESERVED

        Lukas Elsrode - Undergraduate Researcher at the Kronforst Laboratory wrote and tested this code
        (10/21/2021)

"""
import itertools
import color
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


def feature_distribution(df, feature='scale_color'):
    """Shows Distributions of Measurements at the 'segby' level grouped by 'feature'

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df' : DataFrame to plot our Morphometric measurements
            (string) - 'feature' : What The Classes should be split up by
        Outputs:
            (None) - Plots Violin Plots of Features
    """
    measurements = DEF_FEATURES
    for m in measurements:
        g = sns.violinplot(x=feature, y=m, data=df, width=0.7)
        t = m + ' ' + 'distribution ' + 'for' + ' ' + make_title(df)
        g.set(title=t)
        plt.show()
    print('\n')
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
        title=make_title(df) + ' - Original Dimension',
        color_discrete_map=c_map
    )

    fig.update_traces(diagonal_visible=False)
    fig.show()
    print('\n')
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
        fig = px.scatter_3d(
            components, x=0, y=1, z=2, color=df_n[field],
            title='3-Component PCA : ' + make_title(df),
            labels={'0': 'PC1', '1': 'PC2', '2': 'PC3'},
            color_discrete_map=c_map
        )
        fig.show()
        print_axis_components(pca, features)
        print('\n')
        return


def print_axis_components(pca, features):
    """ For a PCA model list the number of components and show the normalized wheights of each of the features.

        Inputs:
            ('sklearn.decomposition._pca.PCA' Object Class) - 'pca' : The principle component axes
            (List of Strings) - 'features': The column names of the features making up the axes
        Outputs:
            (None)
    """
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    for i, paxis in enumerate(pca.components_):
        print(f"~ PC{str(i+1)} ~")
        for j, comp in enumerate(paxis):
            print(f"{features[j]} : {comp}")
        print('\n')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
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
            title=make_title(df) + " PCA's  of N-dimensions"
        )
        fig.show()
        print('\n')
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
        # Get the contributions of each feature in the PC1,PC2 plane
        loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
        # Make The Figure
        fig = px.scatter(components, x=0, y=1, title='2-Component PCA : ' + make_title(df), labels={
                         '0': 'PC1', '1': 'PC2'}, color=df_n[field], color_discrete_map=c_map)
        # Show the Feature Contribution to PC1 & PC2
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
        print_axis_components(pca, features)
        print('\n')
    return

# FEATURE NORMALIZATION AND DATA FORMATING ~ DROP EMPTY ROWS FOR CLEAN PROCESSING


def resize_data(df, features, field):
    """ Given DataSet with a field to be determined from Features drop any rows which have missing feature inputs

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df': The DataFrame to plot our morphometric measurements
            (List of Strings) - 'features': the column names for the morphometric measurements to be examined
            (String) - 'field': What is the target variable in the dataset
        Outputs:
            (tuple) - 'df_n', 'X' : The new resized data, the indicator variables columns from the resized data
    """
    # seperate target and predictor variables
    r = features + [field]
    df_n = df[r]
    # Drop any rows with empty data ===> YES THIS SKEWS OUR DATA A LOT TOWARDS PLANAR FEATURES
    df_n = df_n.dropna()
    X = df_n[features]
    M = X.to_numpy()
    n, _ = M.shape
    # Stoping condition if no PCA can be made
    if n <= 0:
        return 0, 0
    # RETURN AN ARRAY OF THE DATA
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
def optimize_feature_set(df, c_map, num_features=2, field='scale_color', opt_to_n_components=2):
    """ Return The best Set of  Features given the input feature sets and the desired data

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df': The DataFrame to plot our morphometric measurements
            (Dictionary) - 'c_map': Dictionary Mapping Field values to the color descriptions for the Visulizations
            (Int) - 'num_features' : The fixed number of ultra-structure features the PCA axes can be constructed from
            (Int) - 'opt_to_n_components': The number of components the PCA can have for which the features are optimized to.
        Outputs:
            (List of Strings) - Best Feature Sub-Set given selection methedology
    """
    assert opt_to_n_components in set(
        [2, 3]), 'Reductions above 3 dimensions and below 2 dimensions are not possible '
    # Change Up the conditions so our Data is still Meaningful
    feature_sets = [x for x in get_all_possible_combinations()
                    if len(x) == num_features]
    # Optimize:  find a local max in feature sets, value given all possible combinations
    # Get a way to store ~ (feature_list,pca_explained_vairance_ratio)
    rv = [None]*len(feature_sets)
    # Fill rv[i] with values of explained variance score of feature_sets[i]
    for i, fset in enumerate(feature_sets):
        try:
            # Here we generate the 'Samples Data', 'Wilde Type Data', and  'Mutant Data'
            data = deepcopy(df)
            df_n, X = resize_data(data, fset, field)
            if type(df_n) != int:
                pca = PCA(n_components=opt_to_n_components)
                pca.fit_transform(X)
                score = round(sum(list(pca.explained_variance_ratio_))*100, 2)
                entry = fset, score
                rv[i] = entry
        except:
            entry = fset, 0.0
            rv[i] = entry
            continue
    # Remove any entries that failed to write into our storage
    rv = [i for i in rv if i != None]
    # get the best feature set in  pair tuples filling rv with lambda function
    best_entry = max(rv, key=lambda i: i[1])
    best_features, _ = best_entry
    # Run appropriate visualizations
    if opt_to_n_components == 2:
        # Show The Loaded PCA
        Load_Features(df, c_map, best_features, field)
    else:
        # Show a 3D model PCA
        PCA_3D(df, c_map, best_features, field)

    print(
        f" The {num_features} features selected to optimize for {opt_to_n_components} components in the data provided is : {best_features}")
    # Show How Explained Variance Grows with added axes
    mk_explained_variance_curve(df, best_features, field)

    return best_features


def full_data_analysis(data, c_map, optimize_to_n_features=3):
    """ Runs the full data analysis on the entire WT data. 

        NOTE: CANNOT RUN THIS FUNCTION ON MUTANT DATA - due to issue in color.py with the color mapping and indexing

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df': The DataFrame to plot our morphometric measurements (WT ONLY)
            (Dictionary) - 'c_map': Dictionary Mapping Field values to the color descriptions for the Visulizations
            (Int) - 'optimize_to_n_features': The fixed number of ultra-structure features the PCA axes can be constructed from
        Outputs:
            (None)
    """
    # 3D PCA
    PCA_3D(data, c_map)
    # 2D PCA
    Load_Features(data, c_map)
    # Optimization
    optimize_feature_set(data, c_map, num_features=optimize_to_n_features)
    return


def family_analysis(wt_data, c_map, num_features=3):
    """ Runs Family by Family analysis 

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df': The DataFrame to plot our morphometric measurements (WT ONLY)
            (Dictionary) - 'c_map': Dictionary Mapping Field values to the color descriptions for the Visulizations
            (Int) - 'num_features': The fixed number of ultra-structure features the PCA axes can be constructed from
        Outputs:
            (None)

    """
    # Segment Data By Family and Apply Desired Functions
    fams = segment_df_by_field(wt_data, 'f')
    for fam in fams:
        feature_distribution(fam)
        Load_Features(fam, c_map)
        top_features = optimize_feature_set(fam, c_map, num_features)
        show_originaldim(fam, c_map, top_features)
        print('\n')
    return


def wt_analysis(data, n_features):
    """ Runs The Wilde Type Analysis part of our program

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'data': The DataFrame to plot our morphometric measurements (WT ONLY)
            (Int) - 'n_features': The fixed number of ultra-structure features the PCA axes can be constructed from
        Outputs:
            (None)
    """
    print('*** WT ANALYSIS ***')
    cmap = color.fill_cmap(data, on_index=False)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f'COLOR MAPPING : {cmap}')
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print('\n')
    print('*** RAW DATA ANALYSIS ***')
    full_data_analysis(data, cmap, n_features)
    print('\n')
    print('*** FAMILY ANALYSIS ***')
    family_analysis(data, cmap, num_features=n_features)
    return


def mutant_analysis(wt_data, mutant_data, N):
    """ Runs the Mutant analysis part of our program

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'wt_data': The DataFrame of morphometric measurements (WT ONLY)
            ('Pandas.DataFrame' Object Class) - 'mutant_data': The DataFrame of morphometric measurements (MUTANT ONLY)
            (Int) - 'N': The fixed number of ultra-structure features the PCA axes can be constructed from
        Outputs:
            (None)
    """
    print('*** MUTANT ANALYSIS ***')
    print('\n')
    mutant_variants = color.gen_mutants(wt_data, mutant_data)
    for mutant in mutant_variants:
        c_map = color.fill_cmap(mutant, on_index=False)
        analyze_mutant_transition_from_scale(mutant, N, c_map)
        print('\n')


def analyze_mutant_transition_from_scale(mutant_data, n_features, c_map):
    """ Runs the analyis on a single mutant scale. Showing what ultra-structure 
        features corespond with an exhibited scale color change in the mutant variants. 

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'wt_data': The DataFrame of morphometric measurements of the wilde and mutated scales of one variant 
            (Int) - 'n_features': The fixed number of ultra-structure features the PCA axes can be constructed from
            (Dictionary) - 'c_map': Dictionary Mapping Field values to the color descriptions for the Visulizations
        Outputs:
            (None)
    """
    # Print Mutation Type
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f'SCALE MUTATION TYPE : ', color.examine_mutant_df(mutant_data))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # Violin Plot
    feature_distribution(mutant_data)
    # 2D PCA
    Load_Features(mutant_data, c_map)
    # Optimization
    top_features = optimize_feature_set(
        mutant_data, c_map, num_features=n_features)
    show_originaldim(mutant_data, c_map, top_features)
    return
