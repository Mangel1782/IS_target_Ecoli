import os
import pandas as pd
from time import time
from datetime import timedelta
import pickle
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score


class runClassifier():

    def read_genome_to_classify(self,
                                path_to_data):

        target_sequence = pd.read_csv(path_to_data)
        return target_sequence

    def deploy_trained_model(self,
                           path_to_model,
                           sequence_to_classify,
                           work_path):

        # load the model
        model = pickle.load(open(path_to_model, 'rb'))
        # Add class
        sequence_to_classify["predicted"] = model.predict(sequence_to_classify.sequence)

        # add probabilites
        probabilities = model.predict_proba(sequence_to_classify.sequence)
        sequence_to_classify["IS_probability"] = probabilities[:, 1]

        # add anotation
        sequence_to_classify['annotation'] = sequence_to_classify["description"].str.split(" ").str[1]
        sequence_to_classify = sequence_to_classify[[x for x in sequence_to_classify.columns
                                                     if x not in ["Unnamed: 0"]]]
        sequence_to_classify.to_csv(work_path + "raw_result.csv", index=False)

        return sequence_to_classify




    def prediction_summary(self,
                           target_sequence,
                           accuracy=False):

        dat = target_sequence
        print(" Retrieving classification report")
        results = confusion_matrix(dat["target"], dat["predicted"])
        print ('Confusion Matrix :')
        print(results)
        if accuracy:
            print('Accuracy Score :', accuracy_score(dat["target"], dat["predicted"]))
        print('Report : ')
        tn, fp, fn, tp = confusion_matrix(dat["target"],
                                          dat["predicted"]).ravel()
        specificity = tn / (tn + fp)
        print("specificity = " + str(specificity))
        sensitivity = tp / (tp + fn)
        print("sensitivity = " + str(sensitivity))


    def get_false_positives_false_negative(self,
                                           input_raw_result,
                                           work_path):

        false_positives = input_raw_result[(input_raw_result["predicted"] == 1) &
                                           (input_raw_result["target"] == 0)]

        false_negatives = input_raw_result[(input_raw_result["predicted"] == 0) &
                                           (input_raw_result["target"] == 1)]


        false_positives.to_csv(work_path + "false_positives_data.csv")
        print("Putative false positives = {}".format(len(false_positives)))
        false_negatives.to_csv(work_path + "false_negatives_data.csv")
        print("False negatives = {}".format(len(false_negatives)))


    def get_overall_performance(self,
                                target_sequence,
                                work_path):


        accuracy = accuracy_score(target_sequence["target"], target_sequence["predicted"])

        tn, fp, fn, tp = confusion_matrix(target_sequence["target"],
                                              target_sequence["predicted"]).ravel()
        specificity = tn / (tn + fp)
        sensitivity = tp / (tp + fn)

        report_df = pd.DataFrame({"accuracy": accuracy,
                                  "specificity": specificity,
                                  "sensitivity": sensitivity, }, index=[0])

        report_df.to_csv(work_path + "classification_report.csv")



    def executor(self,
                 main_dir,
                 path_to_model,
                 accuracy=False
                 ):

        t0 = time()
        for item in os.listdir(main_dir):
            genome_name = item + "/"
            print("processing genome: " + genome_name + "--" * 10)

            target_sequence = self.read_genome_to_classify(path_to_data=main_dir + genome_name + "input_genome.csv")


            sequence_labelled = self.deploy_trained_model(path_to_model = path_to_model,
                                                          sequence_to_classify = target_sequence,
                                                          work_path=main_dir + genome_name)

            prediction_summary = self.prediction_summary(target_sequence = sequence_labelled,
                                                         accuracy=accuracy)


            get_fp_fn = self.get_false_positives_false_negative(input_raw_result=sequence_labelled,
                                                                work_path=main_dir + genome_name)

            perfomance = self.get_overall_performance(target_sequence = sequence_labelled,
                                                       work_path=main_dir + genome_name)

            #compute_report = self.compute_report(main_dir=main_dir)

        time_elapsed = time() - t0
        time_computed = str(timedelta(seconds=time_elapsed))
        print("-"*60)
        print("Time elapsed  = " + time_computed)
        print("-"*60)




