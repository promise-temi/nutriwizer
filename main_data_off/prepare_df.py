from modules.clean_big_df_empty_cols import Clean_Big_Df_Empty_Cols

# retirer les colonnes trop vides du dataset, qui n'apporteront rien a l'analyse
CleanEmptyCols = Clean_Big_Df_Empty_Cols(dataset_path="data/full_openfoodfacts_products_dataset.csv.gz", separator= "\t", chunksize=1_000_000, encoding = "utf_8", outputs_path = "data" ) 
CleanEmptyCols.Pipeline()