import pandas as pd
import scanpy as sc
import numpy as np


class RemoveMt:
    """
    A class for quality control and gene filtering in a spatial transcriptomics dataset.
    It calculates mitochondrial (mt) gene statistics and
    filters out these genes from the data.

    Parameters:
    - anndata (anndata): Anndata object containing the spatial transcriptomics data.
    - species (str): The species of the data, either "human" or "mouse".

    Example:
    ```
    # Create an instance of the RemoveMt class
    filter_obj = RemoveMt(anndata, species="human")

    # Access the filtered Anndata object
    filtered_data = filter_obj.data
    ```

    Note: To obtain the filtered Anndata object, access the `.data` attribute after class initiation.
    """

    def __init__(self, anndata, species):
        """
        Initialize an instance of the RemoveMt class.

        Parameters:
        - anndata (anndata): Anndata object containing the spatial transcriptomics data.
        - species (str): The species of the data, either "human" or "mouse".
        """
        self.anndata = anndata
        self.species = species

        if self.species == "human":
            self.mito = 'MT-'
            self.malat1 = 'MALAT1'
        elif self.species == "mouse":
            self.mito = 'mt-'
            self.malat1 = 'Malat1'

        self.mito_obs, self.mito_data = self._before_mt()
        self.data = self._remove_mt()

    def _before_mt(self):
        """
        Calculate mitochondrial gene statistics before filtering.
        """
        anndata = self.anndata
        anndata.var['mt'] = anndata.var_names.str.startswith(self.mito)

        sc.pp.calculate_qc_metrics(anndata, qc_vars=['mt'], percent_top=None, log1p=False, inplace=True)

        anndata = self.anndata
        mito_genes = anndata.var_names.str.startswith(self.mito)
        anndata.obs['percent_mt2'] = np.sum(anndata[:, mito_genes].X, axis=1).A1 / np.sum(anndata.X, axis=1).A1
        anndata.obs['n_counts'] = anndata.X.sum(axis=1).A1

        return anndata[:, mito_genes].obs, anndata

    def _remove_mt(self):
        """
        Filter out mitochondrial genes from the dataset.
        """

        anndata = self.anndata
        malat1 = anndata.var_names.str.startswith(self.malat1)
        mito_genes = anndata.var_names.str.startswith(self.mito)

        remove = np.add(mito_genes, malat1)
        remove = np.add(remove)
        keep = np.invert(remove)

        anndata = anndata[:, keep]

        return anndata
