#  Lukas Elsrode (2021)

import scale_data
import viz_data
import color
from phy_tree import Tree
from time import sleep


def gen_rgb_data():
    # Switch the 'scale_color' field in both datasets to the RGB name
    info, data = color.use_RBG(
        scale_data.df_samples, scale_data.df_data, colors=None)
    # Add the 'R','G','B' columns
    data = color.make_R_G_B_cols(data)
    return info, data


def gen_validated_by_data():
    info, data = color.drop_misclassified_colors(
        scale_data.df_samples, scale_data.df_data)
    data = color.make_R_G_B_cols(data)
    return info, data


def gen_custom_closest(colors):
    info, data = color.use_RBG(
        scale_data.df_samples, scale_data.df_data, colors=colors)
    # Add the 'R','G','B' columns
    data = color.make_R_G_B_cols(data)
    return info, data


if __name__ == "__main__":
    # info, data
    info, data = gen_custom_closest(['white', 'black'])
    # Make our phylogenetic Tree
    #tree = Tree(data)
    # Color Map
    color_map = color.fill_cmap(data, on_index=None)
    # Vizulization Functions
    #foo_0 = viz_data.show_originaldim
    #foo_1 = viz_data.PCA_2D
    #foo_2 = viz_data.PCA_3D
    foo_3 = viz_data.Load_Features

    vizulizations = [foo_3]
    for f_viz in vizulizations:
        # Applied on all data
        f_viz(data, color_map)
        # Applied to each family in data
        viz_data.run_viz_by_field(data, f_viz, color_map, field='scale_color')
        print('\n')
