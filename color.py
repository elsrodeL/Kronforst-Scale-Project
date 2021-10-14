""" color.py

Applies a variety of color classification and identification methods to our data

    SCALE PROJECT -- KRONFORST LABORATORY AT THE UNIVERSITY OF CHICAGO
                  -- ALL RIGHTS RESERVED

        Lukas Elsrode - Undergraduate Researcher at the Kronforst Laboratory wrote and tested this code
        (09/01/2021)

File uncompleted...- (10/14/2021)

"""


import webcolors
import math

# The Default Colors that we expect in our DataSet
DEFAULT_COLORS = [
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
    'lime',
    'ivory',
    'gold'
]


def closest_colour(requested_colour):
    """Returns Closest Color in String Format given RGB input

        Inputs:
            (tupl) - 'requested_colour': The RGB values of the color i.e (0,0,0)
        Outputs:
            (string) - The Closest definable color as per the CSS3 color library

        DISCLAIMER: THIS IS NOT MY CODE 
        Thank you to SBRG who uses and MIT liscense and to the open-source comunity
        Source: https://www.programcreek.com/python/example/97156/webcolors.hex_to_rgb


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

    DISCLAIMER: THIS IS MODIFIED CODE FROM 
    https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green-with-python

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


def closest_bincolor(input_color, def_colors=DEFAULT_COLORS):
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


def reindex_hierarchy(df, with_color=False, mutants=False):
    """ Alters a DataFrame creating a New Column by which to re-index the table entries by 
        Used for to create a color mapping between a key:value for our data visualizations 

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df' : The Sample Data, WT Data, or Mutant Data from our study
            (Boolean) - 'with_color' : Include the color of the scale in the new index
            (Boolean) - 'mutants' : Is the DataFrame 'df' that of the mutant scale data
        Outputs:
            ('Pandas.DataFrame' Object Class) - 'df' : The Sample Data, Wt Morphometric Data, or Mutant Data from our study with a new column 'index'
    """
    # Init list to return a column with a new index
    # Iterate through the rows of the DataFrame and make a new index for each row
    rv, H = [], df.to_numpy()
    r, _ = H.shape
    # Column indexes in our table reffering to Species,Genotype,Color_Feature_1, Color_Feature_2
    SP_INDEX, GENO_INDEX, C1_INDEX, C2_INDEX = 4, 5, 6, 7
    for i in range(r):
        # Index our entries based off 'string': <species> and 'string': <genotype>
        new_index = " ".join([str(H[i][SP_INDEX]), str(H[i][GENO_INDEX])])
        # All our DataTables have 2 color entries in their data entry
        c1, c2 = str(H[i][C1_INDEX]), str(H[i][C2_INDEX])
        # Do we include the color of the scale in the new index
        if with_color and not mutants:
            # We are not dealing with a mutant we only care about the scale and iridescent color
            scale_color, irr_color = c1, c2
            # Check for iridescent color as that tends to be the dominant visible color
            if irr_color not in ['', 'nan']:
                new_index += ' ' + scale_color + ' + i(' + irr_color + ')'
            else:
                new_index += ' ' + scale_color

        elif with_color and mutants:
            # Get the color of the mutant before and after the mutation
            color_transition = "->".join([c1, c2])
            new_index += ' ' + color_transition
        # Add the new entries to the list
        rv.append(new_index)
    df['index'] = rv
    return df


def fill_dictionary(df, k, v):
    """ Maps Keys to Values by row entry in DataFrame returning a dictionary of mappings
        Given a DataFrame 'df' containing columns 'k','v' map entries.

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df' : The Sample Data, WT Data, or Mutant Data from our study
            (string)- 'k' : The column which is to be the keys in this mapping.                 ~ It MUST BE A COLUMN IN THE DF
            (string)- 'v' : The column which is to be the value to the key 'k' in this mapping. ~ It MUST BE A COLUMN IN THE DF
        Outputs:
            (Dictionary): 'd_2': A dictionary returning all the values of df[k] : df[v] by row 
    """
    # init dict, get all key:value pairs in order
    d, d_2 = {}, {}
    values = df[v].tolist()
    keys = df[k].tolist()
    # Go through them and see if their are no conflicting values (ideally we want a 1:1 mapping)
    for i, val in enumerate(values):
        key = keys[i]
        if key not in set(d.keys()):
            d[key] = [val]

        elif val in set(d[key]):
            pass

        else:
            d[key].append(val)
    # Remove List within dictionary for keys with one-to-one mapping
    for k, v in d.items():
        if len(v) == 1:
            d_2[k] = v[0]

    return d_2


def color_name_to_custom_RGB_format(color_name):
    """ Converts the string color name into the RGB code format we use in our DataTable in GoogleSheets
        (i.e) 'white' -> 'rgb(0,0,0)' 

        Inputs:
            (string): 'color_name': The name common English word for the color 
        Outputs:
            (string): 'new_v': The RGB code of the input color formated to write into our table
    """
    # A couple colors in our study which we think fit a better description than their given name in publication
    if color_name == 'cream':
        color_name = 'ghostwhite'
    if color_name == 'glass':
        color_name = 'cyan'
    # A lot of string formating
    # ~ There is a probably a better way to do this, we just formated our entries in our table this way
    rgb = webcolors.name_to_rgb(color_name)
    rgb = str(rgb).split(',')
    rgb = [i.split('=') for i in rgb]
    r, g, b = [i[1] for i in rgb]
    if b[-1] == ')':
        b = b[:-1]
    new_v = 'rgb(' + r + ',' + g + ',' + b + ')'
    return new_v


def fill_cmap(df, color_description='scale_color', on_index=True, keys='index'):
    """ Fills the Color Mapping for our Data Visualizations 
    makes a dictionary of 

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df': The DataFrame from which to construct our color mapping

            (String) - 'color_description': The column in the DataFrame that describes the color of the scales


            (Boolean) - 'on_index': The custom index by which we define each entry of data from a measurement 

            *** NOTE THAT BOTH TRUE AND FALSE ARE SCALE COLOR AS DESCRIBED BY THE DATA SOURCE's AUTHORS ***

                True --  key to values are 'custom_index': str_rgb_literal('scale_color')
                False -- key to values are 'scale_color' : srt_rgb_literal('scale_color')

            (String) - 'keys': The column in the the DataFrame that describes what values in the DataFrame should be mapped to color values of 'color_description'

        Outputs:
            (Dictionary) - 'c_map': A dictionary of keys and values mapping string color names to rgb values (i.e : 'white' : 'rgb(255,255,255)')
    """

    d, c_map = fill_dictionary(df, keys, color_description), {}
    # Then map to specific species color
    if on_index:
        # {'index'.unique() :-> rgb('scale_color')}
        for k, v in d.items():
            rgb = color_name_to_custom_RGB_format(v)
            c_map[k] = rgb

    # Then map the scale_color : rgb(scale_color as labeled)
    else:
        for _, v in d.items():
            # {'scale_color' :-> rgb('scale_color')}
            rgb = color_name_to_custom_RGB_format(v)
            c_map[v] = rgb

    return c_map


def split_by_irridesence(df_samples):
    """ Splits up Samples into two separate DataFrames of iridescent and non-iridescent scales

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df_samples' : The Sample Data for our study
        Ouputs:
            (Tuple of 'Pandas.DataFrame' Object Classes) - tuple[0] : iridescent scales , tuple[1] : non-iridescent scales
    """
    # break it down by irr and non-irr colors
    no_irr = df_samples.loc[df_samples['irr_color'] == 'nan']
    irr = df_samples.loc[df_samples['irr_color'] != 'nan']
    return irr, no_irr


def add_color_classification_from_rbg_code(df_samples, color_bins=DEFAULT_COLORS):
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


def drop_misclassified_colors(df_samples, df_data, color_bins=DEFAULT_COLORS):
    """ Removes 'misclassified colors' from samples data and morphometric data

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
    samples = add_color_classification_from_rbg_code(samples, color_bins)
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


def correct_color_description_using_rbg_codes(df_samples, df_data, mutants=False, colors=DEFAULT_COLORS):
    """ Replaces the 'scale color' description with what the RBG value is closest to. 
        Replaces the scale color description of the 'df_data' table with a more accurate classification
        according to the CSS3 library. Input NoneType into colors to classify to closest possible defianable color in the CSS3 library. 

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df_samples' : The Sample Data for our study
            ('Pandas.DataFrame' Object Class) - 'df_data' : The Morphometric Data for our study of wilde type or mutant species
            (Boolean) - 'mutants' : Is the 'df_data' variable mutant data
            (List of Strings) - 'colors': A list of default colors to match to the labled color 
                                          if None then the color value will be changed to the closest identifiable color in CSS3

        Outputs:
            (Tuple of 'Pandas.DataFrame' Object Classes) - df_samples, df_data 

    """
    # Map the Custom Indexes -> string color name using a dictionary
    samples = add_color_classification_from_rbg_code(
        reindex_hierarchy(df_samples, with_color=True), color_bins=colors)
    d = fill_dictionary(samples, k='index', v='classified_color')

    # Apply New RGB Colors replacing them for the WT and mutant DataSets
    # Iter through the indexes and their actual color
    # and set the 'scale_color' or 'scale_color_post' variable to that value
    if not mutants:
        df = reindex_hierarchy(df_data, with_color=True)
        for k, v in d.items():
            df.loc[df_data['index'] == k, 'scale_color'] = v

    else:
        df = reindex_hierarchy(df_data, with_color=True, mutants=True)
        for k, v in d.items():
            df.loc[df_data['index'] == k, 'scale_color_post'] = v

    return samples, df


def gen_rgb_data(df_samples, df_data, mutants=False):
    """ Generates Data and changes 'scale_color' description to the closest identifiable color in CSS3 given rgb code

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df_samples' : The Sample Data for our study
            ('Pandas.DataFrame' Object Class) - 'df_data' : The Morphometric Data for our study of wilde type or mutant species
            (Boolean) - 'mutants' : Is the 'df_data' mutant data
        Outputs:
            (Tuple of 'Pandas.DataFrame' Object Classes) : 'info', 'data'

    """
    if not mutants:
        # Switch the 'scale_color' field in both datasets to the RGB name
        info, data = correct_color_description_using_rbg_codes(
            df_samples, df_data, colors=None)
    else:
        # Switch the 'scale_color' field in both datasets to the RGB name
        info, data = correct_color_description_using_rbg_codes(
            df_samples, df_data, mutants=True, colors=None)

    return info, data


def gen_validated_by_data(df_samples, df_data):
    """ Generates Data who's 'labeled_color' field is the same as the color identified by our algorithm

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df_samples' : The Sample Data for our study
            ('Pandas.DataFrame' Object Class) - 'df_data' : The Morphometric Data for our study of wilde type species

        Outputs:
            (Tuple of 'Pandas.DataFrame' Object Classes) : 'info', 'data'
    """
    info, data = drop_misclassified_colors(df_samples, df_data)
    return info, data


def gen_custom_closest(df_samples, df_data, colors=DEFAULT_COLORS, mutants=False):
    """ Generates Data and changes 'scale_color' field to the closest color in the 'colors' list

        Inputs:
            ('Pandas.DataFrame' Object Class) - 'df_samples' : The Sample Data for our study
            ('Pandas.DataFrame' Object Class) - 'df_data' : The Morphometric Data for our study of wilde type or mutant species
            (List) - 'colors' : The list of colors to match to i.e ['black','white']
            (Boolean)- 'mutants': Is the df_data mutant data ? 
        Outputs:
            (Tuple of 'Pandas.DataFrame' Object Classes) : 'info', 'data'

    """
    if not mutants:
        # Switch the 'scale_color' field in both datasets to the RGB name
        info, data = correct_color_description_using_rbg_codes(
            df_samples, df_data, colors=colors)
    else:
        # Switch the 'scale_color' field in both datasets to the RGB name
        info, data = correct_color_description_using_rbg_codes(
            df_samples, df_data, mutants=True, colors=colors)

    return info, data


# TO-DO; Need to write this up.
def gen_mutants(df_samples, df_data, colors=DEFAULT_COLORS):
    return None
