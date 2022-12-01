# IS_target
Machine Learning estimator for bacterial insertion sequences predictions on Escherichia coli.



## This software has the capability to identify bacterial insertion sequences. 

The software architecture may be divided in three general instances

#### 1- Genome scraper
Under this stage the input is a CSV file downloaded from https://www.ncbi.nlm.nih.gov/genome/browse/#!/prokaryotes/167/
This file has the following schema:
genome
strain name and
 link to download. 

Furthermore, the file is used as a template and the script iterates over each row (each genome) downloading it to a local directory.



#### 2-Processing Genomes
Each genome is then processed from the  .gz extension to a readable CSV. The resultant  CSV file is defined by  the following schema : 
amino acid sequence 
annotation

#### 3-Classification
On this step a serialized and pre-trained model in pickle format is executed across all the genomes.

#### 4-Report
The last step consists in producing the overall report on the genome
Although a specific report is yielded on each genome strain while the classifier is being executed, a global report is then computed in order to be able to quantify the performance of the classification process.
The global report consists of central tendency measures, median, mean, standard deviation of Accuracy, Sensitivity and Specificity.


# How to execute the software ?
Please, follow the step described below.

#### step 1: to create an environment
$ conda create --  name [env_name] python=3
#### step 2: installing requirements
$ pip install -r requirements.txt
#### step 3: to check environment set up
$ python environment_test.py
#### step 4: executing software via the “orchestrator” module
$ python orchestrator.py 


