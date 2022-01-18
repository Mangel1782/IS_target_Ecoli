import os
import glob
import shutil
import pandas as pd
pd.set_option("display.max_columns", None)
import urllib
import urllib.request

#from urllib import request
import time

from time import time
from datetime import timedelta




class genomeScraper():

    @staticmethod
    def process_genome_sheet(file_name):

        data = pd.read_csv(file_name)
        # select relevant columns
        data = data[["Strain", "GenBank FTP"]]

        # remove Duplicates rows
        data = data.dropna(inplace=False)
        # Create a column where scpaper will be iterate then
        data['id_raw'] = range(1, len(data) + 1)
        data['fasta_sequence'] = data['GenBank FTP']
        data['fasta_sequence'] = data["GenBank FTP"].str.split("/").str[-1]
        data['fasta_sequence'] = data['GenBank FTP'] + "/" + data['fasta_sequence'] + "_protein.faa.gz"

        # remove parenthesis
        data['Strain'] = data['Strain'].str.replace(r"\([^()]*\)", "")
        # remove apostrophes
        data['Strain'] = data['Strain'].str.replace(r"[\"\',]", '')

        data = data.head(50)

        return data

    def genome_scrapper(self,
                        target_directory,
                        genome_sheet_file):

        if len(os.listdir(target_directory)) == 0:
            t0 = time()
            data = genome_sheet_file

            for row in data.itertuples():
                genome_link = row.fasta_sequence
                genome_name = row.Strain
                print("downloading " + genome_name)
                try:
                    data = urllib.request.urlretrieve(genome_link, target_directory + genome_name + ".gz")
                except:
                    pass

            time_elapsed = time() - t0
            time_computed = str(timedelta(seconds=time_elapsed))
            print(time_computed)

            main_dir = target_directory

            os.chdir(main_dir)
            for file in glob.glob("*.gz"):
                final_destination = main_dir + file.replace(" ", "_").replace(".gz", "")
                os.mkdir(final_destination)
                # print(final_destination)
                shutil.move(file, final_destination)

            return time_computed
        else:
            print("Genomes were already downloaded")

    def orchestrator(self,
                     file_name,
                     target_directory):

        data_clean = self.process_genome_sheet(file_name=file_name)

        genomes = self.genome_scrapper(target_directory=target_directory,
                                       genome_sheet_file=data_clean)

        return genomes
