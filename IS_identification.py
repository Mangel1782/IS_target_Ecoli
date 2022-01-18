import os
import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_rows', 1000)

from time import time
from datetime import timedelta

from Bio.Blast.Applications import NcbiblastpCommandline as BLAST_CLI


class CatchIS():

    """
    Two paths (directories) are needed:
     - one to loop across the folders with the results in order to read the False Positives
    - the second one, to yield the results (where BLAST should be executed). This second directory needs to contains
    IS databases (fsa, phr, pin, psq, fasta) files.
    """


    def collect_false_positives(main_dir):
        data_place_holder = []
        for item in os.listdir(main_dir):
            genome_name = item + "/"
            path_to_data = main_dir + genome_name
            # print(path_to_data)

            data = pd.read_csv(path_to_data + "false_positives_data.csv",
                               index_col=[0])

            data["annotation"] = data.description.str.split(" ").str[1]
            data["strain"] = item
            data["description"] = item + "_" + data["description"].astype(str)

            # Exclude sequences wrongly labelled
            data = data[~data["annotation"].str.contains("IS", na=False)]
            data_place_holder.append(data)

        df_false_positives_full = pd.concat(data_place_holder)
        df_false_positives_full = df_false_positives_full.replace("phage", "Phage")

        print("Potential False Positives Collected !")
        print("-" * 50)
        print("Data Schemma")
        print("-" * 50)
        print(df_false_positives_full.info())
        print("-" * 50)
        return df_false_positives_full

    def generate_target_fasta(data_false_positives,
                              target_annotation,
                              path_to_data):

        # step 1: Filter by regex interested rows
        dat_annotation_target = data_false_positives[data_false_positives.annotation.str.contains(target_annotation,
                                                                                                  na=False)]
        dat_annotation_target["description"] = dat_annotation_target["description"].replace(' ', '_', regex=True)

        # step 2: Convert values to list
        sequence_name_list = dat_annotation_target.description.tolist()
        sequence_list = dat_annotation_target.sequence.tolist()

        # step 3: Writing as FASTA
        ofile = open(path_to_data + "potential_IS.fasta", "w")
        for i in range(len(sequence_list)):
            ofile.write(">" + sequence_name_list[i] + "\n" + sequence_list[i] + "\n")
        ofile.close()

        print("Potential False Positives were FASTA files now")