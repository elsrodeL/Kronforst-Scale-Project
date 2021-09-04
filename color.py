"""color.py

Applies a variety of color classification and identification methods to our data

    SCALE PROJECT -- KRONFORST LABORATORY AT THE UNIVERSITY OF CHICAGO 
                  -- ALL RIGHTS RESERVED 
        
        Lukas Elsrode - Undergraduate Researcher at the Kronforst Laboratory wrote and tested this code 
        (09/01/2021)
"""

import numpy as np
import webcolors
import math

# The Default Colors that we expect in our DataSet
default_colors = [
    'white',
    'black',
    'brown',
    'yellow',
    'red',
    'beige',
    'orange',
    'purple',
    'blue',
    'green',
    'grey',
    'lime'
]


def closest_colour(requested_colour):
    """Returns Closest Color in String Format given RGB input

        Inputs:
            (tupl) - 'requested_colour': The RGB values of the color i.e (0,0,0)
        Outputs:
            (string) - The Closest definable color as per the CSS3 color library 
    """
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def return_closest_RGBcolor(requested_colour):
    """Get the Closest Definable Color Name in CSS3

        Inputs: 
            (tuple) - 'requested_colour' : The RGB value of the color i.e (0,0,0)
        Outputs:
            (string) - 'actual_name' or 'closest_name'
    """
    # Try and see if there is a direct hit in the range for a specific color name
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        # Get the closest definable color in CSS3
        closest_name = closest_colour(requested_colour)
        actual_name = None
    # Return Best of two options
    if actual_name:
        return actual_name
    return closest_name


def closest_bincolor(input_color, def_colors=default_colors):
    """Returns Closest Color to Input color given a color list 

        Inputs:
            (String) - 'input_color' : The name of the color 
            (List of Strings) - 'def_colors' : A list of color names 
        Outputs:
            (String) : The color in 'def_colors' closest to 'input_color' in RGB space
    """
    r, g, b = webcolors.name_to_rgb(input_color)[0:3]
    color_diffs = []

    for color in def_colors:
        cr, cg, cb = webcolors.name_to_rgb(color)[0:3]
        color_diff = math.sqrt(
            abs(r - cr)**2 + abs(g - cg)**2 + abs(b - cb)**2)
        color_diffs.append((color_diff, color))

    return min(color_diffs)[1]


def swaptoRGB(df_samples, color_bins=default_colors):
    """ Changes the Labled Color in df_samples from the Publication to the closest RGB color 
            if color_bins is 'None' otherwises chooses closest color to labeled color from 'color_bins'

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df_samples' : The Sample Data for our study
            (List of Strings) - 'color_bins' : The baseline name of colors to re-organize our labeled data around i.e ['white','black'] or 'None' for no binning 

        Outputs:
            ('Pandas.DataFrame' Object Class) - 'df_samples' : The modified samples data for our study
    """
    res = []
    rbg = df_samples['rbg_color'].values

    # convert to nearest rgb_defined_color
    for c in rbg:
        truple = c[4:]
        truple = truple[:len(truple)-1]
        truple = truple.split(',')

        if type(truple) != str and truple[0] != '':
            # conv str input and return
            truple = [int(i) for i in truple]
            col = return_closest_RGBcolor(truple)
            res.append(col)
        else:
            res.append(None)

    # now we turn the closest values into the nearest value in our res list
    # default color inputs
    rv = []

    # If default colors are provided match within that list, else just take the nearest color
    if color_bins != None:
        for rgb_color in res:
            if rgb_color != None:
                classified_color = closest_bincolor(
                    rgb_color, def_colors=color_bins)
                rv.append(classified_color)
            else:
                rv.append(None)
        df_samples['classified_color'] = rv

    else:
        df_samples['classified_color'] = res

    return df_samples


def split_by_irridesence(df_samples):
    """ Splits up Samples into two separate DataFrames of iridescent and non-iridescent scales

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df_samples' : The Sample Data for our study
        Ouputs:
            (Tuple of 'Pandas.DataFrame' Object Classes) - tuple[0] : iridescent scales , tuple[1] : non-iridescent scales
    """
    # break it down by irr and non-irr colors
    irr = df_samples.loc[df_samples['irr_color'] != '']
    no_irr = df_samples.loc[df_samples['irr_color'] == '']
    return irr, no_irr


def drop_misclassified_colors(df_samples, df_data):
    """Removes 'misclassified colors' from samples data and morphometric data

            A 'misclassified' color is a color which was labeled in the publication as 'red'/'X' but is closer 
            to another color in the default_color bin such as 'yellow'/'Y' given its RGB reference value. 

            Inputs:
                ('Pandas.DataFrame' Object Class) - 'df_samples' : The Sample Data for our study
                ('Pandas.DataFrame' Object Class) - 'df_data' : The Morphometric Data for our study of wilde type species 
            Outputs:
                (Tuple of Pandas.DataFrame' Object Classes) - 'samples', 'df' : updated samples and wt morphometric data 
    """
    # initialize rv to return correctly classified indexes
    rv = []
    # re-index one another
    samples, df = reindex_hierarchy(
        df_samples, with_color=True), reindex_hierarchy(df_data, with_color=True)
    # get the rbg color
    samples = swaptoRGB(samples)
    # break it down by irr and non-irr colors
    irr, no_irr = split_by_irridesence(df_samples)
    # irr_color is determined color
    irr_correct = irr.loc[irr['irr_color'] ==
                          irr['classified_color']]['index'].tolist()
    # pigmented color is determined color
    no_irr_correct = no_irr.loc[no_irr['labeled_color']
                                == no_irr['classified_color']]['index'].tolist()
    # Append using += using python list feature
    rv += irr_correct
    rv += no_irr_correct
    # Apply a filter to original DataFrames to only allow those that were correctly classified
    s_filter, d_filter = samples['index'].isin(rv), df['index'].isin(rv)
    samples, df = samples[s_filter], df[d_filter]
    return samples, df


# TO-DO : Allow re-indexing for mutants
def reindex_hierarchy(df, with_color=False, mutants=False):
    """ Creates a New Column in the DataFrame Provided
    """

    rv = []
    H = df.to_numpy()
    r, _ = H.shape

    for i in range(r):

        hierarchy = H[i][4]
        genotype = H[i][5]

        new_index = hierarchy + ' ' + genotype

        if with_color == True:
            # Check for iridescent color as that tends to be the dominant visible color
            if H[i][7] != '':
                new_index = new_index + ' ' + H[i][7]
            else:
                new_index = new_index + ' ' + H[i][6]

        rv.append(new_index)
    df['index'] = rv

    return df


def fill_dictionary(df, k, v):
    d = {}
    new_colors = df[v].tolist()
    indexes = df[k].tolist()
    for i, j in enumerate(new_colors):
        d[indexes[i]] = j
    return d


def fill_cmap(df, i='index', on_index=None):

    d, c_map = fill_dictionary(df, i, 'scale_color'), {}
    # Then map to specific species color
    if on_index != None:
        for k, v in d.items():
            rgb = RGB_type_to_str(v)
            c_map[k] = rgb

    # Then map the scale_color : rgb(scale_color as labeled)
    else:
        for _, v in d.items():
            rgb = RGB_type_to_str(v)
            c_map[v] = rgb

    return c_map


def RGB_type_to_str(color_name):
    if color_name == 'cream':
        color_name = 'ghostwhite'

    if color_name == 'glass':
        color_name = 'cyan'

    rgb = webcolors.name_to_rgb(color_name)
    rgb = str(rgb).split(',')
    rgb = [i.split('=') for i in rgb]
    r, g, b = [i[1] for i in rgb]

    if b[-1] == ')':
        b = b[:-1]

    new_v = 'rgb(' + r + ',' + g + ',' + b + ')'
    return new_v


def make_R_G_B_cols(df):

    # use the color map
    c_map = fill_cmap(df, on_index=None)

    # Init 3 new_columns
    n = len(df)
    p = ['R', 'G', 'B']
    for i in p:
        df[i] = np.zeros([n, 1], dtype=int)

    for i, j in df.iterrows():
        nums = c_map[j['scale_color']].split(',')
        nums = [i for i in nums]
        r, g, b = nums
        r, g, b = int(r[4:]), int(g), int(b[:-1])

        df.at[i, 'R'] = r
        df.at[i, 'G'] = g
        df.at[i, 'B'] = b

    return df


def use_RBG(df_samples, df_data, colors=default_colors):
    ''' Replaces the scale color input with the RGB value
    '''
    # re-index one another
    samples, df = reindex_hierarchy(
        df_samples, with_color=True), reindex_hierarchy(df_data, with_color=True)
    # get the rbg color
    samples = swaptoRGB(samples, color_bins=colors)
    # create a dictionary to get the k:v pairs together
    d = fill_dictionary(samples, k='index', v='classified_color')

    for k, v in d.items():
        df.loc[df_data['index'] == k, 'scale_color'] = v
    return samples, df
