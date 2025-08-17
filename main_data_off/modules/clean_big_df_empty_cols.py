import pandas as pd

class Clean_Big_Df_Empty_Cols:
    def __init__(self, dataset_path="", separator ="\t", chunksize=100_000, encoding="utf_8", outputs_path="" ):
        self.dataset_path = dataset_path
        self.separator = separator
        self.chunksize = chunksize
        self.encoding = encoding
        self.output_path = outputs_path
        self.low_memory = False
        self.on_bad_lines="skip"


        self.columns_emptyness_infos = []
        self.seuil = 95
        self.colonnes_a_supprimer = []


    def EmptyColsPerChunks(self, chunk):
        """
        Cette fonction identifie, pour chaques lots (chunks), toutes les colonnes présentant un taux de valeurs manquantes trop élevé.  
        Elle renvoie une liste d’objets de la forme :  
        [{column_name: x, empty_percentage: y%}]  
        où chaque objet indique le nom de la colonne et le pourcentage de valeurs manquantes.
        """
        df = chunk
        df_len = df.shape[0]
        # identification du pourcentage de vide pour chaques colonnes
        for column in df.columns.to_list():
            column_name = column
            empty_sum = df[column].isna().sum()
            empty_pourcentage = empty_sum / df_len * 100

            column_emptytiness_info = {
                "column_name" : column_name,
                "empty_pourcentage" : empty_pourcentage
            }
            self.columns_emptyness_infos.append(column_emptytiness_info)



    

    def EmptynessInfoToDataset(self):
        """
        Realisation d'un petit nettoyage et transformation de la liste d'objet donnant des informations"
        sur le taux de vides du dataset en vrac, transformation en dataset pandas puis sauvegarde csv
        """
        clean_collones_trop_vides_brut = []
        # Petit filtrage des données
        for infos in self.columns_emptyness_infos:
            if infos:
                clean_collones_trop_vides_brut.append(infos)
        # Transformation en dataframe pandas
        df_clean_collones_trop_vides_brut = pd.DataFrame(clean_collones_trop_vides_brut)
        df_clean_collones_trop_vides_brut.to_csv(f"{self.output_path}/empty_cols_brut.csv")




    
    def StatisticallyIdentifyRealEmptyCols(self):
        """
        Fonction pour regrouper les collones pour effectue une moyenne par
        leurs taux de vide et calculer le taux de variation, a partir et grace de ce nouveau 
        dataset identifier les collones a supprimer en voyant si la moyenne est fiable grace
        au coeficient de variation et que en moyenne la collones soit vide a pile ou a plus de 95%
        """
        # reccuperation du dataset de collones vides et regroupement par nom  de collones pour faire la moyenne dutaux de vide et lecart type.
        df_cols_info_brut = pd.read_csv(f"{self.output_path}/empty_cols_brut.csv")
        df_stats = df_cols_info_brut.groupby('column_name', as_index=False).agg(['mean', 'std'])

        
        def validate_empty(df_):
            """
            Fonction pour identifier le nom des collonnes a supprimer grace au 
            coeficient de variation fiable et un taux de vide en moyenne a 95% ou plus
            """
            empty_pourcentage_mean = df_[('empty_pourcentage', 'mean')]
            empty_pourcentage_std = df_[('empty_pourcentage', 'std')]
            try:
                variation_coeficient = empty_pourcentage_std / empty_pourcentage_mean
            except ZeroDivisionError:
                variation_coeficient = None

            column_name = df_[('column_name', '')]
            #verifier si le coeficiant de variation est stable (la moyenne est elle fiable)
            if variation_coeficient != None:
                if variation_coeficient < 0.1:
                    if empty_pourcentage_mean >= self.seuil:
                        self.colonnes_a_supprimer.append(column_name)

        df_stats.apply(validate_empty, axis=1)
        print("Colonnes à supprimer identifiées avec succès")
        

    def GetEmptyColsInfosInDataset(self):
        for i, chunk_df in enumerate(pd.read_csv(self.dataset_path, 
                                         sep=self.separator,
                                         encoding=self.encoding,
                                         low_memory=self.low_memory,
                                         chunksize=self.chunksize,
                                         on_bad_lines=self.on_bad_lines)):
            self.EmptyColsPerChunks(chunk_df)
            print(f"Chunk {i+1} : Taux de vides identifiés avec succès")
            print("________________________________")
            print(self.columns_emptyness_infos)


    def DeleteEmptyColsFromDataset(self):
        """
        Fonction pour supprimer les collones trop vides par chunk de maniere iteratives et progressive
        """
        def remove_empty_cols(df_):
            """
           Pour le chunk concerné : supprimer les colonnes à exclure. 
           Pour le premier chunk, utiliser write. Pour les suivants, utiliser add.
            """
            df_= df_.drop(columns=self.colonnes_a_supprimer)
            df_.to_csv(f'{self.output_path}/no_empty_col_dataset.csv',
                        mode="w" if first_chunk else 'a', 
                        header=first_chunk, 
                        index=False )



        first_chunk = True

        for i, chunk_df in enumerate(pd.read_csv(self.dataset_path, 
                                         sep=self.separator,
                                         encoding=self.encoding,
                                         low_memory=self.low_memory,
                                         chunksize=self.chunksize,
                                         on_bad_lines=self.on_bad_lines)):
            remove_empty_cols(chunk_df)
            first_chunk = False
            print(f"Chunk {i+1} : Suppression des collones avec succes, ajout du chunk réussi")





    def Pipeline(self):
        self.GetEmptyColsInfosInDataset()
        self.EmptynessInfoToDataset()
        self.StatisticallyIdentifyRealEmptyCols()
        self.DeleteEmptyColsFromDataset()


            
