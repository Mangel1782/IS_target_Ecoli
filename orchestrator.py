from genome_scraper import genomeScraper
from process_genomes import processGenomes
from classifier import runClassifier
from global_report import overallReport
import os


if __name__ == "__main__":

    os.mkdir("genomes_dir")
    main_dir = os.getcwd() + "/genomes_dir/"
    genome_bank_file = os.getcwd() + "/prokaryotes_12_20_2020.csv"
    path_to_model = os.getcwd() +  "/estimator_v0122.sav"


    GS = genomeScraper()
    PG = processGenomes()
    ALG = runClassifier()
    OR = overallReport()

    scrapper = GS.orchestrator(file_name=genome_bank_file,
							   target_directory=main_dir)

    process_genomes = PG.orchestrator(main_dir=main_dir,
                                      save_dataframe=True,
                                      create_summary=True)

    IS_classifier = ALG.executor(main_dir=main_dir,
                                 path_to_model=path_to_model,
                                 accuracy=True)

    OR = overallReport.compute_summary(path_to_data=main_dir)


