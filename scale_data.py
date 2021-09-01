"""scale_data.py
This File is where information from our 
GoogleSheets Database is pre-processed for analysis

    SCALE PROJECT -- KRONFORST LABORATORY AT THE UNIVERSITY OF CHICAGO 
                  -- ALL RIGHTS RESERVED 
        
        Lukas Elsrode - Undergraduate Researcher at the Kronforst Laboratory wrote and tested this code 
        (09/01/2021)
"""
import pandas as pd

# The Numeric Ranges of Our Measurments in the GoogleSheets Spreadsheet
DEFAULT_WT_RANGE = (8, 15)
DEFAULT_MUTANT_RANGE = (14, 21)
DEFAULT_SAMPLES_RANGE = (12, 19)

# Associate Inputs to get a certain DataFrame to work with
sheet_input_range = {
    'wt_table': DEFAULT_WT_RANGE,
    'mutant_table': DEFAULT_MUTANT_RANGE,
    'samples_info': DEFAULT_SAMPLES_RANGE}


def get_df(sheet_name='wt_table'):
    """Returns DataFrame of Relevant DataSheet Associated with our DataBase 
        Inputs:
            (string)- sheet_name : Name of the sheet i.e 'wt_table','mutant_table','samples_info'
        Outputs:
            ('Pandas.DataFrame' Class Object) - df_raw : Raw Data of our study formated
    """
    # All data #
    sheet_id = '10YVwgtR8W4JqSWyDhCpJFUdw1BIJZXSx89oly8HHhwI'
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url)
    rv = []
    # manual cleaning of columns
    for c in df.columns:
        if c[0:3] == 'Unn':
            pass
        else:
            rv.append(c)
    df_raw = df[rv]

    # range of the measurement data
    if sheet_name not in sheet_input_range.keys():
        return df_raw

    else:
        # get the numeric range of measurment entries
        q1, q2 = sheet_input_range[sheet_name]
        # define the collumns which are numbers not strings
        quant_vars = [i for i in df_raw.columns[q1:q2]]
        qual_vars = [i for i in df_raw.columns if i not in quant_vars]
        # Force strings into floats
        for numeric_var in quant_vars:
            df_raw[numeric_var] = pd.to_numeric(
                df_raw[numeric_var], errors='coerce')

        for qual_var in qual_vars:
            # Format some strings to be uniform
            df_raw[qual_var] = [str(i).lower().replace(" ", "")
                                for i in df_raw[qual_var].values]

        return df_raw


def segment_df_by_field(df, group_by='f'):
    """ Segments Pandas.DataFrame of Data by Group of total entries within the set of Group_By
        i.e 'scale_color'

            Inputs: 
                (string) - group_by: Single letter to represent what to segment the dataset by
                    ________________
                    'f': by family -- DEFAULT VALUE
                    's': by species
                    'g': by genotype
                    'sf': by subfamily
                    't': by tribe
                    'ge': by genus
                    'c': by scale color
            Outputs:
                (list of 'Pandas.DataFrame' Object Classes) - l : A list of datasets 
                    segmented by all values in the group_by set.
    """
    # initilize list to return
    l = []

    # set of all_possible results
    all_species, all_families, all_colors, all_genotypes, all_subfams, all_tribes, all_genuses = set(df.species), set(
        df.family), set(df.scale_color), set(df.genotype), set(df.subfamily), set(df.tribe), set(df.genus)

    # initilize relavant dictionary
    d = {'f': ('family', all_families),
         's': ('species', all_species),
         'c': ('scale_color', all_colors),
         'g': ('genotype', all_genotypes),
         'sf': ('subfamily', all_subfams),
         't': ('tribe', all_tribes),
         'ge': ('genus', all_genuses)}

    # set the variables needed
    # breaking up the data-frame

    for m in d[group_by][1]:
        df_member = df[df[d[group_by][0]] == m]
        l.append(df_member)

    return l
