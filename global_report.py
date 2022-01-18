import os
import pandas as pd

class overallReport():
    def compute_summary(path_to_data):
        df_list = []
        strain_list = []

        main_dir = path_to_data

        for item in os.listdir(main_dir):
            genome_name = item + "/"
            # print(item)

            strain_list.append(item)

            df = pd.read_csv(main_dir + genome_name + "classification_report.csv")
            df["strain"] = item

            df_list.append(df)

        df = pd.concat(df_list)
        df = df[[c for c in df.columns if c not in ["Unnamed: 0"]]]



        df["accuracy"] = df["accuracy"] * 100
        df["specificity"] = df["specificity"] * 100
        df["sensitivity"] = df["sensitivity"] * 100
        df.to_csv(main_dir + "overall_report.csv")
        print("report saved !")


        print("-"*50)
        print("Descriptive Statistics")
        print("-" *50)
        print(df.describe())
        print("-" *50)
        print("Median accuracy = " + str(df[["accuracy"]].median()))
        print("Median specificity = " + str(df[["specificity"]].median()))
        print("Median sensitivity = " + str(df[["sensitivity"]].median()))
