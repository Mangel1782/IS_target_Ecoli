from genome_scraper import genomeScraper
from process_genomes import processGenomes
from classifier import runClassifier
from global_report import overallReport

if __name__ == "__main__":

   # main_dir = "/home/mike/Documents/Genomes_execution/Genomes/E_coli/run_2021_02_15/"

    main_dir = "/home/mike/Documents/Genomes_execution/Genomes/E_coli/run_2022_01_16/"

    genome_bank_file = "/home/mike/Documents/Genomes_execution/FTP_downloads/prokaryotes_12_20_2020.csv"
    path_to_model = "/home/mike/Documents/Genomes_execution/model_saved/estimator_p.sav"

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
                                 path_to_model = path_to_model,
                                 accuracy=True)

    OR = overallReport.compute_summary(path_to_data = main_dir)


