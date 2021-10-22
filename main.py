""" main.py
    Runs Our Program.   
    
    SCALE PROJECT -- KRONFORST LABORATORY AT THE UNIVERSITY OF CHICAGO
                  -- ALL RIGHTS RESERVED

        Lukas Elsrode - Undergraduate Researcher at the Kronforst Laboratory wrote and tested this code
        (10/21/2021)
"""

# The Source Code for this Project can be found in these libraries
import os
import pyfiglet
import color
import viz_data
from scale_data import WT_DATA, SAMPLES_DATA, MUTANT_DATA
from copy import deepcopy


def generate_data(color_classification, colors=None, mutants=False):
    """ Generates the data To run our Visualizations

        Inputs:
            (String) - 'color_classification' : The Type of color classification to apply to our data 

                VALID INPUTS:  ['rgb','validated','closest']
                ______________
                - 'rgb': scale color is labeled to the closest definable color in CSS3 given the color's RGB values
                - 'closest': scale color is labeled to the closest definable color in CSS3 given the color's RGB values from within 'colors' or a default bin of common colors
                - 'validate': data generated is only in cases where the scale color description given in the publication is confirmed by our color classification
                            NOTE : 'validated' does not work on mutant analysis
            (List of Strings or None) - 'colors' : A list of colors to bin scale_color definitions by. if None then DEFAULT_COLORS in color.py is used
            (Boolean) - 'mutants' : generate data for mutant analysis

        Outputs:
            (Tuple of Pandas.DataFrame Type Object Classes) - either samples_data,wt_data for mutants == False or wt_data, mutant_data for mutants  == True
    """
    # Make a copy of the dataframes so they aren't overwritten
    WT, SAMPLES, MUTANTS = deepcopy(WT_DATA), deepcopy(
        SAMPLES_DATA), deepcopy(MUTANT_DATA)

    if not mutants:
        if color_classification is 'rgb':
            samples, data = color.gen_rgb_data(SAMPLES_DATA, WT_DATA)
        if color_classification is 'validated':
            samples, data = color.gen_validated_by_data(SAMPLES_DATA, WT_DATA)

        if color_classification is 'closest':
            if type(colors) != list:
                samples, data = color.gen_custom_closest(SAMPLES_DATA, WT_DATA)
            else:
                samples, data = color.gen_custom_closest(
                    SAMPLES_DATA, WT_DATA, colors)
        return samples, data
    else:
        if color_classification is 'rgb':
            _, mutant_data = color.gen_rgb_data(SAMPLES, MUTANTS, mutants=True)
            _, wt_data = color.gen_rgb_data(SAMPLES_DATA, WT)

        if color_classification is 'closest':
            if type(colors) != list:
                _, mutant_data = color.gen_custom_closest(
                    SAMPLES, MUTANTS, mutants=True)
                _, wt_data = color.gen_custom_closest(SAMPLES_DATA, WT)

            else:
                _, mutant_data = color.gen_custom_closest(
                    SAMPLES, MUTANTS, colors=colors, mutants=True)
                _, wt_data = color.gen_custom_closest(
                    SAMPLES_DATA, WT, colors)
        return wt_data, mutant_data


def save_data(data, file_name):
    """ Writes out DataFrame and saves it as a csv file in ../data
        Inputs:
            ('Pandas.DataFrame' Type Object Classes) - 'data': The data to write out and save as a csv
            (String) - 'file_name' : What to name our file

        Outputs:
            (None)
    """
    os.chdir('../data')
    data.to_csv(file_name, sep='\t', encoding='utf-8')
    return


def main(color_classification='closest', mutant_analysis=False, colors=None, N=3):
    """ ~ Main Function For our Program: 
            Generates the data for scale analysis given our color classification methods. 
            Applies our feature selection method using a PCA on either a family by family basis 
            or on a mutant by mutant basis. Shows how ultra-scale characteristics are distributed 
            with regards to their relative scale color. 

        Inputs:
            (String) - 'color_classification' : How to classify the scale_color value based on RGB values for pictures of that scale.
            (Boolean) - 'mutant_analysis' : determines the analysis conducted -- True for mutant, false for family 
            (List of strings or None) - 'colors':  A list of colors to bin scale_color definitions by. if None then DEFAULT_COLORS in color.py is used
            (Int) - 'N' : The number of ultra-scale charecteritics to select from the default range of all charecteristics

        Outputs:
            (None)
    """
    if not mutant_analysis:
        _, data = generate_data(color_classification, colors, False)
        # Case of family analysis
        viz_data.wt_analysis(data, N)
        save_data(data, 'fam_data_'+color_classification+'.csv')
    else:
        # Case of Mutants
        data = generate_data(color_classification, colors, True)
        wt_data, mutant_data = data
        viz_data.mutant_analysis(wt_data, mutant_data, N)
        save_data(mutant_data, 'mutant_data_'+color_classification+'.csv')


if __name__ == "__main__":
    # Intro Text to Our Program
    txt = pyfiglet.figlet_format('The Scale Project')
    print(txt)
    main(color_classification='closest', mutant_analysis=False, N=2)
    print('*** SCALE ANALYSIS COMPLETE ***')
