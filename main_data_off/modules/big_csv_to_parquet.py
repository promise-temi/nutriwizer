import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

class Massive_Csv_To_Parquet:
    def __init__(self, dataset_path="", separator="\t", chunksize=1_000_000, encoding="utf-8", outputs_path=""):
        self.chunksize = chunksize
        self.separator = separator
        self.encoding = encoding
        self.low_memory = False
        self.on_bad_lines = "skip"
        self.dataset_path = dataset_path
        self.output_path = outputs_path
        self.writer = None


    def csv_to_parquet(self):
        for i, chunk_df in enumerate(pd.read_csv(self.dataset_path, 
                                         sep=self.separator,
                                         encoding=self.encoding,
                                         low_memory=self.low_memory,
                                         chunksize=self.chunksize,
                                         on_bad_lines=self.on_bad_lines)):
            
            table = pa.Table.from_pandas(chunk_df)
            # Initialiser le writer au premier chunk avec le bon schéma
            if self.writer is None:
                self.writer = pq.ParquetWriter(f"{self.output_path}/no_empty_col_dataset.parquet", table.schema, compression='snappy')
            # Écrire le chunk
            self.writer.write_table(table)

            print(f"Chunk {i+1} écrit dans le Parquet")



        # Fermer le writer à la fin
        if self.writer:
            self.writer.close()