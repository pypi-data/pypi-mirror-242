import anndata as ad
import pandas as pd
import scanpy as sc
from typing import Optional

class MakeAnndata:
    """
    A class to create an AnnData object with spatial coordinates from CURIO data.

    Attributes
    ----------
    sample_path : str
        Path to the CURIO-generated h5ad file.
    barcodes_path : str
        Path to the sample-specific bead barcode whitelist.

    Methods
    -------
    create_anndata()
        Create an AnnData object with spatial coordinates.
    """
    def __init__(self, sample_path: str, barcodes_path: str):
        """
        Constructs all the necessary attributes for the MakeAnndata object.

        Parameters
        ----------
        sample_path : str
            Path to the CURIO-generated h5ad file.
        barcodes_path : str
            Path to the sample-specific bead barcode whitelist.
        """
        self.sample_path = sample_path
        self.barcodes_path = barcodes_path

    def _process_whitelist(self) -> pd.DataFrame:
        """
        Preprocess the bead barcode whitelist.

        Returns
        -------
        pd.DataFrame
            Processed bead barcode whitelist as a DataFrame.
        """
        barcodes = pd.read_csv(self.barcodes_path, delimiter="\t", names=["barcode", "x", "y"])
        barcodes.set_index("barcode", inplace=True)
        return barcodes

    def _process_h5ad(self) -> ad.AnnData:
        """
        Preprocess the h5ad file from CURIO.

        Returns
        -------
        ad.AnnData
            Preprocessed AnnData object.
        """
        data = sc.read_h5ad(self.sample_path)
        sc.pp.filter_cells(data, min_counts=1)
        data.obs_names = [''.join(x.split("_")) for x in data.obs_names]
        return data

    def create_anndata(self) -> ad.AnnData:
        """
        Create an AnnData object with spatial coordinates.

        Returns
        -------
        ad.AnnData
            AnnData object with spatial coordinates.
        """
        barcodes = self._process_whitelist()
        data = self._process_h5ad()

        shared_barcodes = list(set(data.obs_names).intersection(barcodes.index))
        data = data[shared_barcodes]
        barcodes = barcodes.loc[data.obs_names]
        data.obs = data.obs.join(barcodes)
        data.obsm["spatial"] = barcodes[["x", "y"]].values
        return data














