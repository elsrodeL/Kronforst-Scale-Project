# Lukas Elsrode - scale_data.py (09/10/2020)

'''  This File is where information from our GoogleSheets Database is pre-processed for analysis
'''

import pygsheets
import pandas as pd



def get_df(sheet_ID, sheet_range,q1,q2):

    # Authorization for API
    gc = pygsheets.authorize(service_file='quickstart.json')

    # All data #
    sheet = gc.get_range(sheet_ID,sheet_range)
    data_raw = pd.DataFrame(sheet).to_numpy()

    # Fix Header
    data = data_raw[1:]
    vars_ = data_raw[0]

    # Data_frame of all results as strings #
    df_raw = pd.DataFrame(data, columns = vars_)

    if q1 == None and q2 == None:
        return df_raw

    else:
        # define the collumns which are numbers not strings
        quant_vars = [i for i in df_raw.columns[q1:q2]]
        qual_vars = [i for i in df_raw.columns if i not in quant_vars]

        for numeric_var in quant_vars:
            df_raw[numeric_var] = pd.to_numeric(df_raw[numeric_var], errors = 'coerce')

        for qual_var in qual_vars:
            # Format some strings to be uniform
            df_raw[qual_var] = [str(i).lower() for i in df_raw[qual_var].values]
            df_raw[qual_var] = df_raw[qual_var].str.replace(" ","")

        return df_raw

def segment_df_by_field(df, group_by):
    '''
            input: split
            ________________

            'f': by family
            's': by species
            'g': by genotype
            'sf': by subfamily
            't': by tribe
            'ge': by genus
            'c': by scale color

    '''

    # initilize list to return
    l = []

    # set of all_possible results
    all_species, all_families, all_colors, all_genotypes, all_subfams, all_tribes, all_genuses= set(df.species), set(df.family), set(df.scale_color), set(df.genotype),set(df.subfamily), set(df.tribe), set(df.genus)

    # initilize relavant dictionary
    d = {'f': ('family', all_families),
         's': ('species', all_species),
         'c': ('scale_color', all_colors),
         'g': ('genotype', all_genotypes),
         'sf': ('subfamily', all_subfams),
         't' : ('tribe', all_tribes),
        'ge': ('genus', all_genuses)}

    # set the variables needed
    # breaking up the data-frame

    for m in d[group_by][1]:
        df_member = df[df[d[group_by][0]] == m]
        l.append(df_member)

    return l

sheet_url = '10YVwgtR8W4JqSWyDhCpJFUdw1BIJZXSx89oly8HHhwI'

# Our three DataSheets
df_data = get_df(sheet_url,'wt_table', 8, 15)
df_mutants = get_df(sheet_url,'mutant_table',14,21)
df_samples = get_df(sheet_url,'samples_info',12,19)

