from .MakeAnndata import MakeAnndata
from .RemoveMt import RemoveMt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scanpy as sc
from matplotlib_venn import venn3

class Normalisation:
    """
    A class for preprocessing and normalizing spatial transcriptomics data using the CURIO pipeline.

    Parameters:
    - anndata (Anndata): Anndata object containing the spatial transcriptomics data.
    - barcode_num (str): Barcode number for a specific whitelist (e.g., "A0026_009").
    - figure_folder (str): Folder where figures should be saved. Subfolders should be created within for specific figures.
    - species (str): The species of the data, either "human" or "mouse".
    - resolution (float): Desired Leiden resolution (default 1.0).
    - n_top (int): Number of top genes for plotting.
    - target_sum (float): Target sum for normalization.

    Note: The subfolders should be created within the specified figure_folder to save figures correctly.
    """

    def __init__(self, anndata, barcode_num, figure_folder, species, n_top, target_sum, resolution=1.0):
        """
        Initialize an instance of the Normalisation class.

        Parameters:
        - anndata (Anndata): Anndata object containing the spatial transcriptomics data.
        - barcode_num (str): Barcode number for a specific whitelist (e.g., "A0026_009").
        - figure_folder (str): Folder where figures should be saved. Subfolders should be created within for specific figures.
        - species (str): The species of the data, either "human" or "mouse".
        - resolution (float): Desired Leiden resolution (default 1.0).
        - n_top (int): Number of top genes for plotting.
        - target_sum (float): Target sum for normalization.
        """
        print('Starting Analysis')
        self.data = anndata
        self.species = species
        self.barcode_num = barcode_num
        self.figure_folder = figure_folder
        self.resolution = resolution
        self.n_top = n_top
        self.target_sum = target_sum
        self.mito_obs, self.mito_data = self.mito_stats()
        self.normalised_data = self.preprocessing_anndata()

    def mito_stats(self):
        """
        Calculate and visualize mitochondrial gene statistics.

        Returns:
        - mito_obs (pd.DataFrame): Dataframe containing mitochondrial gene statistics.
        - mito_data (Anndata): Anndata object with mitochondrial gene statistics.
        """
        print('Quality Measures')
        data = self.data
        tmp = RemoveMt(data, self.species)
        mito_obs = tmp.mito_obs
        mito_data = tmp.mito_data

        # Visualizations
        self.plot_quality_measures_violin(mito_data, ['n_genes_by_counts', 'total_counts', 'pct_counts_mt'])
        self.plot_quality_measures_violin(mito_data, ['pct_counts_mt'])
        self.plot_scatter_plot(mito_data, 'total_counts', 'pct_counts_mt', "Scatter Plot of pct_counts_mt")
        self.plot_scatter_plot(mito_data, 'total_counts', 'n_genes_by_counts', "Scatter Plot of n_genes_by_counts")
        self.plot_quality_measures_spatial(mito_data, ["total_counts", "n_genes_by_counts", "pct_counts_mt"])
        self.plot_quality_measures_spatial(mito_data, ["pct_counts_mt"])
        self.plot_histogram(data.obs.pct_counts_mt, "Histogram of Percentage Counts Mito")

        return mito_obs, mito_data

    def preprocessing_anndata(self):
        """
        Preprocess and normalize the anndata object.

        Returns:
        - data (Anndata): Preprocessed and normalized Anndata object.
        """
        print('Preprocessing and Normalization')
        data = self.data
        tmp = RemoveMt(data, self.species)
        data = tmp.data

        self.plot_highest_expressed_genes(data, n_top=self.n_top)

        # Normalization
        sc.pp.normalize_total(data, inplace=True, target_sum=self.target_sum)

        # Log transformation
        sc.pp.log1p(data)

        return data

    def plot_quality_measures_violin(self, data, genes):
        """
        Plot violin plots for quality measures.

        Parameters:
        - data (Anndata): Anndata object containing quality measures.
        - genes (list): List of genes to be plotted.
        """
        sc.pl.violin(data, genes, jitter=0.4, rotation=45,
                     save=self.figure_folder + f'Quality_Measures_Violin_{self.barcode_num}.pdf')

    def plot_scatter_plot(self, data, x, y, title):
        """
        Plot scatter plot for quality measures.

        Parameters:
        - data (Anndata): Anndata object containing quality measures.
        - x (str): Variable for x-axis.
        - y (str): Variable for y-axis.
        - title (str): Title of the scatter plot.
        """
        sc.pl.scatter(data, x=x, y=y, title=title,
                      save=self.figure_folder + f'Quality_Measures_Scatter_{self.barcode_num}.pdf')

    def plot_quality_measures_spatial(self, data, genes):
        """
        Plot spatial quality measures.

        Parameters:
        - data (Anndata): Anndata object containing spatial quality measures.
        - genes (list): List of genes to be plotted.
        """
        sc.pl.spatial(data, color=genes, spot_size=30, vmin=0, vmax='p99.2',
                      save=self.figure_folder + f'Quality_Measures_Spatial_{self.barcode_num}.pdf')

    def plot_histogram(self, data, title):
        """
        Plot histogram.

        Parameters:
        - data (pd.Series): Pandas Series for histogram.
        - title (str): Title of the histogram plot.
        """
        data.hist(bins=100)
        plt.title(title)
        plt.savefig(self.figure_folder + f'histogramfigures/Histogram_{title}_{self.barcode_num}.pdf')
        plt.clf()

    def plot_highest_expressed_genes(self, data, n_top):
        """
        Plot highest expressed genes.

        Parameters:
        - data (Anndata): Anndata object containing gene expression data.
        - n_top (int): Number of top genes to be plotted.
        """
        sc.pl.highest_expr_genes(data, n_top=n_top,
                                 save=self.figure_folder + f'Highest_Expressed_Genes_{self.barcode_num}.pdf')
