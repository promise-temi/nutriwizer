from modules.clean_big_df_empty_cols import Clean_Big_Df_Empty_Cols
from modules.big_csv_to_parquet import Massive_Csv_To_Parquet

# # retirer les colonnes trop vides du dataset massif, qui n'apporteront rien à l'analyse
# CleanEmptyCols = Clean_Big_Df_Empty_Cols(dataset_path="data/full_openfoodfacts_products_dataset.csv.gz", separator= "\t", chunksize=1_000_000, encoding = "utf_8", outputs_path = "data" ) 
# CleanEmptyCols.Pipeline()

#Transformer le dataset massif au for csv en format parquet
CsvToParquet = Massive_Csv_To_Parquet(dataset_path="data/no_empty_col_dataset.csv", separator= "\t", chunksize=1_000_000, encoding = "utf_8", outputs_path = "data")
CsvToParquet.csv_to_parquet()
