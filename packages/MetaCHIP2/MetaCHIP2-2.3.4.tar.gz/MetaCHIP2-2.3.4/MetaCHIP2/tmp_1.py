import numpy as np
import pandas as pd
from copy import deepcopy
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


def subset_df(df_in, rows_to_keep, cols_to_keep):

    if len(rows_to_keep) == 0:
        if len(cols_to_keep) == 0:
            subset_df = df_in.loc[:, :]
        else:
            subset_df = df_in.loc[:, cols_to_keep]
    else:
        if len(cols_to_keep) == 0:
            subset_df = df_in.loc[rows_to_keep, :]
        else:
            subset_df = df_in.loc[rows_to_keep, cols_to_keep]

    return subset_df


def get_boxplot(data_matrix, hgt1_id, hgt2_id, output_plot):

    label_rotation = 0
    input_df = pd.read_csv(data_matrix, sep=',', header=0, index_col=0)
    col_id_list = input_df.columns.values.tolist()
    row_id_list = input_df.index.to_list()
    mag_list    = deepcopy(row_id_list)
    mag_list.remove(hgt1_id)
    if hgt2_id is not None:
        mag_list.remove(hgt2_id)

    input_df_mags = subset_df(input_df, mag_list, [])
    input_df_hgt1 = subset_df(input_df, [hgt1_id], [])
    if hgt2_id is not None:
        input_df_hgt2 = subset_df(input_df, [hgt2_id], [])


    fig = plt.figure(1, figsize=(9, 6))
    ax  = fig.add_subplot(111)
    median_line_props = dict(color="black", linewidth=1.5)  # customise median line
    bp  = ax.boxplot(input_df_mags, medianprops=median_line_props)
    ax.set_xticklabels(col_id_list, rotation=label_rotation, fontsize=8)

    plt.title('Filled: %s, unfilled: %s' % (hgt1_id, hgt2_id))
    plt.xlabel('COG category')
    plt.ylabel('Proportion')

    # change the style of fliers and their fill
    for flier in bp['fliers']:
        flier.set(marker='.', color='black', alpha=0.7, markersize=3, markerfacecolor='black', markeredgecolor='black')

    # add hgt1 values, https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html
    hgt1_value_list = []
    hgt1_shape_list = []
    hgt1_color_list = []
    hgt1_size_list  = []
    hgt2_value_list = []
    hgt2_shape_list = []
    hgt2_color_list = []
    hgt2_size_list  = []
    for col_id in col_id_list:

        hgt1_value              = input_df_hgt1[col_id].values[0]
        if hgt2_id is not None:
            hgt2_value          = input_df_hgt2[col_id].values[0]
        mag_value_list          = input_df_mags[col_id].values
        mag_value_percentile_25 = np.percentile(mag_value_list, 25)
        mag_value_percentile_75 = np.percentile(mag_value_list, 75)

        # get value list
        hgt1_value_list.append(hgt1_value)
        if hgt2_id is not None:
            hgt2_value_list.append(hgt2_value)

        # get shape and color list for hgt1
        if hgt1_value < mag_value_percentile_25:
            hgt1_shape_list.append('v')
            hgt1_color_list.append('deepskyblue')
            hgt1_size_list.append(7)
        elif hgt1_value > mag_value_percentile_75:
            hgt1_shape_list.append('^')
            hgt1_color_list.append('red')
            hgt1_size_list.append(7)
        else:
            hgt1_shape_list.append('s')
            hgt1_color_list.append('grey')
            hgt1_size_list.append(5)

        # get shape and color list for hgt2
        if hgt2_id is not None:
            if hgt2_value < mag_value_percentile_25:
                hgt2_shape_list.append('v')
                hgt2_color_list.append('deepskyblue')
                hgt2_size_list.append(7)
            elif hgt2_value > mag_value_percentile_75:
                hgt2_shape_list.append('^')
                hgt2_color_list.append('red')
                hgt2_size_list.append(7)
            else:
                hgt2_shape_list.append('s')
                hgt2_color_list.append('grey')
                hgt2_size_list.append(5)

    # add hgt1 points
    x_index = 1
    for (hgt1_value, hgt1_shape, hgt1_color, hgt1_size) in zip(hgt1_value_list, hgt1_shape_list, hgt1_color_list, hgt1_size_list):
        plt.plot(x_index, hgt1_value, alpha=1, marker=hgt1_shape, markersize=hgt1_size, markeredgewidth=1, color=hgt1_color)
        x_index += 1

    # add hgt2 points
    if hgt2_id is not None:
        x_index = 1
        for (hgt2_value, hgt2_shape, hgt2_color, hgt2_size) in zip(hgt2_value_list, hgt2_shape_list, hgt2_color_list, hgt2_size_list):
            plt.plot(x_index, hgt2_value, alpha=1, marker=hgt2_shape, markersize=hgt2_size, markeredgewidth=1, color=hgt2_color, fillstyle='none')
            x_index += 1

    # export plot
    plt.tight_layout()
    fig.savefig(output_plot, bbox_inches='tight', dpi=300)
    plt.close()


matrix          = '/Users/songweizhi/Desktop/MetaCHIP2/blastn_vs_mmseqs/faa_files_COG2020_fun_stats_mmseqs.txt'
output_plot     = '/Users/songweizhi/Desktop/MetaCHIP2/blastn_vs_mmseqs/faa_files_COG2020_fun_stats_mmseqs.png.pdf'
get_boxplot(matrix, 'zHGTs_mmseqs', None, output_plot)

