""" main.py

    Runs Our Program.   

"""
# The Source Code for this Project can be found in these libraries
import sys
import pyfiglet
import color
import viz_data
from scale_data import WT_DATA, SAMPLES_DATA, MUTANT_DATA
from copy import deepcopy


def main(dataset='closest', analysis='family', colors=None, N=3):
    """ ~ Main Function For our Program ~

        Inputs:
            dataset
            ______________
                - 'closest'    - Gives you closest color in colors to the labeled scale color.
                - 'validated'  - Gives you data who's color description is validated by a sampled RGB value.
                - 'rgb'        - Gives you closest Definable scale color as defined by the CSS3 library.

            analysis:
            ____________
                - 'family'    - Does a Family by Family Analysis of the Scale colors.
                - 'mutant'    - Does a Mutant /CRISPR CAS9 analysis for pre and post mutation ultra-structures.
    """
    # Init our main Function
    WT, SAMPLES, MUTANTS = deepcopy(WT_DATA), deepcopy(
        SAMPLES_DATA), deepcopy(MUTANT_DATA)
    assert analysis in set(['mutant', 'family']
                           ), "Choose Analysis Type : 'mutant' or 'family' "

    # Case of family analysis
    if analysis == 'family' and dataset == 'rgb':
        samples, data = color.gen_rgb_data(SAMPLES_DATA, WT_DATA)
        viz_data.wt_analysis(data, n_features=N)
    if analysis == 'family' and dataset == 'validated':
        samples, data = color.gen_validated_by_data(SAMPLES_DATA, WT_DATA)
        viz_data.wt_analysis(data, n_features=N)
    if analysis == 'family' and dataset == 'closest':
        if type(colors) != list:
            samples, data = color.gen_custom_closest(SAMPLES_DATA, WT_DATA)
        else:
            samples, data = color.gen_custom_closest(
                SAMPLES_DATA, WT_DATA, colors)
        viz_data.wt_analysis(data, n_features=N)

    # Case of Mutants
    else:
        # Assign Correct Mutant DataFrame
        if dataset == 'rgb':
            samples, data = color.gen_rgb_data(
                SAMPLES_DATA, MUTANT_DATA, mutants=True)
        if dataset == 'closest':
            if type(colors) != list:
                samples, data = color.gen_custom_closest(
                    SAMPLES_DATA, MUTANT_DATA, mutants=True)
            else:
                samples, data = color.gen_custom_closest(
                    SAMPLES_DATA, WT_DATA, colors, mutants=True)
        if dataset == 'raw':
            samples, data = SAMPLES_DATA, WT_DATA


if __name__ == "__main__":
    # Intro Text to Our Program
    txt = pyfiglet.figlet_format('The Scale Project')
    print(txt)
    main(dataset='validated')

