import os
import sys
import pandas as pd
import numpy as np
import anndata as ad
import tacco as tc
import scanpy as sc

class TaccoDeconvolution:
    """
    A class for spatial analysis of cell type annotations and spatial images.

    Parameters:
    - data_path (str): Path to the folder containing the spatial transcriptomics data.
    - plot_path (str): Folder where figures should be saved.
    - reference_file (str): Path to the reference file for cell type annotations.
    """

    def __init__(self, data_path, plot_path, reference_file):
        self.data_path = data_path
        self.plot_path = plot_path
        self.reference_file = reference_file
        self.reference = sc.read(filename=reference_file)

    def load_data(self, puck_file):
        """
        Load spatial transcriptomics data.

        Parameters:
        - puck_file (str): Path to the spatial transcriptomics data file.

        Returns:
        - puck (Anndata): Anndata object containing spatial transcriptomics data.
        """
        puck = ad.read(puck_file)
        puck.var.reset_index(inplace=True)

        return puck

    def annotate_cell_types(self, puck):
        """
        Annotate cell types in the spatial transcriptomics data using the reference.

        Parameters:
        - puck (Anndata): Anndata object containing spatial transcriptomics data.

        Returns:
        - puck (Anndata): Annotated Anndata object.
        """
        tc.tl.annotate(puck, self.reference, 'cell_type_original', result_key='cell_type_original')
        puck.obs = puck.obs.join(puck.obsm['cell_type_original'])
        return puck

    def plot_spatial_images(self, puck, color_variable):
        """
        Plot spatial images based on the specified color variable.

        Parameters:
        - puck (Anndata): Anndata object containing spatial transcriptomics data.
        - color_variable (str): Variable for color in spatial images.
        """
        sc.pl.spatial(puck, color=[color_variable], spot_size=30, wspace=0.5)

