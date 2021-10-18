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

# THIS NEEDS TO BE BROKEN UP


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
            _, mutant_data = color.gen_rgb_data(
                SAMPLES, MUTANTS, mutants=True)
            _, wt_data = color.gen_rgb_data(SAMPLES_DATA, WT)

        if dataset == 'closest':
            if type(colors) != list:
                _, mutant_data = color.gen_custom_closest(
                    SAMPLES, MUTANTS, mutants=True)
                _, wt_data = color.gen_custom_closest(SAMPLES_DATA, WT)

            else:
                info1, mutant_data = color.gen_custom_closest(
                    SAMPLES, MUTANTS, colors=colors, mutants=True)
                info2, wt_data = color.gen_custom_closest(
                    SAMPLES_DATA, WT, colors)

        mutant_variants = color.gen_mutants(wt_data, mutant_data)
        for mutant in mutant_variants:
            viz_data.mutant_analysis(mutant)


if __name__ == "__main__":
    # Intro Text to Our Program
    txt = pyfiglet.figlet_format('The Scale Project')
    print(txt)
    main(dataset='closest', analysis='mutant')
