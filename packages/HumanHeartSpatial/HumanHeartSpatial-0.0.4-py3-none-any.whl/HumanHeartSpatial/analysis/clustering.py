from . import MakeAnndata
from . import remove_mt_ribo
from matplotlib_venn import venn3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scanpy as sc
import scanpy.external as sce
from matplotlib_venn import venn3


print("To access final preprocessed, clustered and scaled anndata: .final_anndata")
        print("To get ranked genes (wilcoxon): .ranked_genes")
        self.final_anndata, self.ranked_genes = self.clustering()


class clustering:


    def __init__(self, anndata, anndata_normalised, figure_folder, barcode_num, cell_cycle_gene_path):

        self.data = anndata
        self.normalised_data = anndata_normalised

        self.barcode_num = barcode_num
        self.figure_folder = figure_folder

        self.cell_cycle_gene_path = cell_cycle_gene_path
        self.s_genes, self.g2m_genes = self.cell_cycle()

    def cell_cycle(self):
        """
        Extract and filter cell cycle genes into S and G2M phases.
        """
        tmp = MakeAnndata(self.data)
        data = tmp.data
        tmp = remove_mt_ribo(data)
        data = tmp.data

        cell_cycle_genes = [x.strip() for x in open(self.cell_cycle_gene_path)]
        s_genes = cell_cycle_genes[:43]
        g2m_genes = cell_cycle_genes[43:]

        cell_cycle_genes = [x for x in cell_cycle_genes if x in data.var_names]

        return s_genes, g2m_genes

    def highly_variable(self):
        sc.settings.set_figure_params(dpi_save=400, fontsize=20, figsize=(10, 10), facecolor='white', frameon=False,
                                      transparent=True, format="pdf")

        sc.pp.highly_variable_genes(data, max_mean=10, min_mean=0, min_disp=0.25)
        sc.pl.highly_variable_genes(data, save=self.figure_folder + f'Highly_Variable_Genes_{self.barcode_num}.pdf')

        sc.tl.score_genes_cell_cycle(data, s_genes=self.s_genes, g2m_genes=self.g2m_genes)

        data.raw = data
        data = data[:, data.var.highly_variable]

        sc.pl.violin(data, ['S_score', 'G2M_score'], jitter=0.4, rotation=45,
                     save=self.figure_folder + f'Cellcycle_Violin_{self.barcode_num}.pdf')

        sc.pp.scale(data, max_value=10, zero_center=False)

        sc.pp.pca(data, random_state=0)

        sc.pl.pca_variance_ratio(data, n_pcs=50, log=True, save=self.figure_folder + f'PCA_{self.barcode_num}.pdf')

        sc.pp.neighbors(data, n_pcs=5)
        sc.tl.umap(data)

        data.to_df().mean(axis=0).hist(bins=100)
        plt.savefig(self.figure_folder + f'histogramfigures/Histogram_Mean_after_Normalisation_{self.barcode_num}.pdf')
        plt.clf()

        data.to_df().iloc[:, 1000:2000].var(axis=0).hist()
        plt.savefig(self.figure_folder + f'histogramfigures/Histogram_Variance_after_Normalisation_{self.barcode_num}.pdf')
        plt.clf()



def clustering(self):
    """
    Perform clustering and analysis.
    """
    print('Clustering')
    data = self.normalised_data
    data.uns['log1p'] = {'base': None}

    sc.tl.leiden(data, key_added="leiden_0.3", resolution=0.3)
    sc.tl.leiden(data, key_added="leiden_0.5", resolution=0.5)
    sc.tl.leiden(data, key_added="leiden_0.8", resolution=0.8)
    sc.tl.leiden(data, key_added="leiden_1.0", resolution=1.0)

    sc.settings.set_figure_params(dpi_save=400, fontsize=20, figsize=(10, 10), facecolor='white', frameon=False,
                                  transparent=True, format="pdf")

    sc.pl.spatial(data, color=["leiden_0.3", "leiden_0.5", "leiden_0.8", "leiden_1.0"], spot_size=30, wspace=0.5,
                  save=self.figure_folder + f'Leiden_Spatial_{self.barcode_num}.pdf')

    if self.resolution == None:
        sc.pl.spatial(data, color=["leiden_1.0"], spot_size=30, wspace=0.5,
                      save=self.figure_folder + f'Leiden_0.1_Spatial_{self.barcode_num}.pdf')
        sc.tl.dendrogram(data, groupby="leiden_1.0")
        sc.pl.dendrogram(data, groupby="leiden_1.0",
                         save=self.figure_folder + f'Leiden_0.1_Dendrogram_{self.barcode_num}.pdf')
        sc.pl.umap(data, color=["leiden_1.0"], palette="tab20",
                   save=self.figure_folder + f'Leiden_0.1_Umap_{self.barcode_num}.pdf')

        sc.tl.rank_genes_groups(data, 'leiden_1.0', method='wilcoxon', key_added='wilcoxon')
        sc.pl.rank_genes_groups(data, n_genes=25, sharey=False, key="wilcoxon",
                                save=self.figure_folder + f'Leiden_0.1_Wilcoxon_Ranked_Genes_{self.barcode_num}.pdf')

        sc.tl.rank_genes_groups(data, 'leiden_1.0', method='t-test', key_added='t-test')
        sc.pl.rank_genes_groups(data, n_genes=25, sharey=False, key="t-test",
                                save=self.figure_folder + f'Leiden_0.1_t-test_Ranked_Genes_{self.barcode_num}.pdf')

        sc.tl.rank_genes_groups(data, 'leiden_1.0', method='logreg', key_added="logreg")
        sc.pl.rank_genes_groups(data, n_genes=25, sharey=False, key="logreg",
                                save=self.figure_folder + f'Leiden_0.1_Logreg_Ranked_Genes_{self.barcode_num}.pdf')

        sc.tl.rank_genes_groups(data, 'leiden_1.0', method='t-test_overestim_var', key_added="t-test_ov")
        sc.pl.rank_genes_groups(data, n_genes=25, sharey=False, key="t-test_ov",
                                save=self.figure_folder + f'Leiden_0.1_t-test_Ov_Ranked_Genes_{self.barcode_num}.pdf')

        ranked_genes = pd.DataFrame(data.uns['wilcoxon']['names'])

        sc.pl.rank_genes_groups_heatmap(data, n_genes=5, key="wilcoxon", groupby="leiden_1.0",
                                        show_gene_labels=True,
                                        save=self.figure_folder + f'Leiden_0.1_Wilcoxon_Heatmap_{self.barcode_num}.pdf')

        sc.pl.rank_genes_groups_dotplot(data, n_genes=5, key="wilcoxon", groupby="leiden_1.0",
                                        save=self.figure_folder + f'Leiden_0.1_Wilcoxon_Dotplot_{self.barcode_num}.pdf')

        sc.pl.rank_genes_groups_stacked_violin(data, n_genes=5, key="wilcoxon", groupby="leiden_1.0",
                                               save=self.figure_folder + f'Leiden_0.1_Wilcoxon_Stacked_Violin_{self.barcode_num}.pdf')

        sc.pl.rank_genes_groups_matrixplot(data, n_genes=5, key="wilcoxon", groupby="leiden_1.0",
                                           save=self.figure_folder + f'Leiden_0.1_Wilcoxon_Matrixplot_{self.barcode_num}.pdf')


    else:
        sc.pl.spatial(data, color=[f"leiden_{self.resolution}"], spot_size=30, wspace=0.5,
                      save=self.figure_folder + f'Leiden_{self.resolution}_Spatial_{self.barcode_num}.pdf')
        sc.tl.dendrogram(data, groupby=f"leiden_{self.resolution}")
        sc.pl.dendrogram(data, groupby=f"leiden_{self.resolution}",
                         save=self.figure_folder + f'Leiden_{self.resolution}_Dendrogram_{self.barcode_num}.pdf')
        sc.pl.umap(data, color=[f"leiden_{self.resolution}"], palette="tab20",
                   save=self.figure_folder + f'Leiden_{self.resolution}_Umap_{self.barcode_num}.pdf')

        sc.tl.rank_genes_groups(data, f"leiden_{self.resolution}", method='wilcoxon', key_added='wilcoxon')
        sc.pl.rank_genes_groups(data, n_genes=25, sharey=False, key="wilcoxon",
                                save=self.figure_folder + f'Leiden_{self.resolution}_Wilcoxon_Ranked_Genes_{self.barcode_num}.pdf')

        sc.tl.rank_genes_groups(data, f"leiden_{self.resolution}", method='t-test', key_added='t-test')
        sc.pl.rank_genes_groups(data, n_genes=25, sharey=False, key="t-test",
                                save=self.figure_folder + f'Leiden_{self.resolution}_t-test_Ranked_Genes_{self.barcode_num}.pdf')

        sc.tl.rank_genes_groups(data, f"leiden_{self.resolution}", method='logreg', key_added="logreg")
        sc.pl.rank_genes_groups(data, n_genes=25, sharey=False, key="logreg",
                                save=self.figure_folder + f'Leiden_{self.resolution}_Logreg_Ranked_Genes_{self.barcode_num}.pdf')

        sc.tl.rank_genes_groups(data, f"leiden_{self.resolution}", method='t-test_overestim_var',
                                key_added="t-test_ov")
        sc.pl.rank_genes_groups(data, n_genes=25, sharey=False, key="t-test_ov",
                                save=self.figure_folder + f'Leiden_{self.resolution}_t-test_Ov_Ranked_Genes_{self.barcode_num}.pdf')

        ranked_genes = pd.DataFrame(data.uns['wilcoxon']['names'])
        sc.pl.rank_genes_groups_heatmap(data, n_genes=5, key="wilcoxon", groupby=f"leiden_{self.resolution}",
                                        show_gene_labels=True,
                                        save=self.figure_folder + f'Leiden_{self.resolution}_Wilcoxon_Heatmap_{self.barcode_num}.pdf')

        sc.pl.rank_genes_groups_dotplot(data, n_genes=5, key="wilcoxon", groupby=f"leiden_{self.resolution}",
                                        save=self.figure_folder + f'Leiden_{self.resolution}_Wilcoxon_Dotplot_{self.barcode_num}.pdf')

        sc.pl.rank_genes_groups_stacked_violin(data, n_genes=5, key="wilcoxon", groupby=f"leiden_{self.resolution}",
                                               save=self.figure_folder + f'Leiden_{self.resolution}_Wilcoxon_Stacked_Violin_{self.barcode_num}.pdf')

        sc.pl.rank_genes_groups_matrixplot(data, n_genes=5, key="wilcoxon", groupby=f"leiden_{self.resolution}",
                                           save=self.figure_folder + f'Leiden_{self.resolution}_Wilcoxon_Matrixplot_{self.barcode_num}.pdf')
    try:
        wc = sc.get.rank_genes_groups_df(data, group='0', key='wilcoxon', pval_cutoff=0.01, log2fc_min=0)['names']
        tt = sc.get.rank_genes_groups_df(data, group='0', key='t-test', pval_cutoff=0.01, log2fc_min=0)['names']
        tt_ov = sc.get.rank_genes_groups_df(data, group='0', key='t-test_ov', pval_cutoff=0.01, log2fc_min=0)[
            'names']

        # compare cluster1 genes, only stores top 100 by default
        venn3([set(wc), set(tt), set(tt_ov)], ('Wilcox', 'T-test', 'T-test_ov'))
        plt.savefig(self.figure_folder + f'vennfigures/Venn_Diagram_Comparison_Ranked_Genes_{self.barcode_num}.pdf')
        plt.show()
    except:
        print('Failed to converge')

    print('Finished Analysis')
    return data, ranked_genes