import os
import pandas as pd
import gzip

class  processGenomes():


    def run_fasta(self,
                  path_to_data):

        genome_file = os.listdir(path_to_data)
        input = gzip.GzipFile(path_to_data + '/' + genome_file[0], 'rb')
        s = input.read()
        input.close()
        output = open(path_to_data + '/' + genome_file[0] + ".faa", 'wb')
        output.write(s)
        output.close()
        print("file unziped")

        # return output

        files = os.listdir(path_to_data)
        fasta_file = [i for i in files if i.endswith('.faa')][0]
        file_name = path_to_data + fasta_file

        output_file = file_name
        out_lines = []
        temp_line = ''

        with open(file_name, 'r') as fp:
            for line in fp:
                if line.startswith('>'):
                    out_lines.append(temp_line)
                    temp_line = line.strip() + '\t'
                else:
                    temp_line += line.strip()

        with open(output_file, 'w') as fp_out:
            fp_out.write('\n'.join(out_lines))
        print("Fasta Processed DONE !")

        return output_file

    def create_dataframe_from_fasta(self,
                                    input_fasta,
                                    work_path,
                                    save_dataframe=False):
        # Step 2: generate a dataframe from Fasta file
        genome_reference = pd.read_csv(input_fasta,
                                       sep='\t',
                                       names=["description", "sequence"])

        genome_reference["description"] = genome_reference["description"].str.replace(r"[>]", "")
        genome_reference["description"] = genome_reference["description"].str.split("\s+\[").str[0]
        genome_reference = genome_reference[["description", "sequence"]]
        genome_reference["description"] = genome_reference.description.str.replace(r"[>]", "")
        if save_dataframe:
            genome_reference.to_csv(work_path + "input_genome.csv")

        return genome_reference

    def add_target(self,
                   input_sequence,
                   work_path,
                   save_dataframe=False,
                   create_summary=False):
        l = []
        for row in input_sequence.description:
            if "transposa" in row:
                l.append(1)
            elif "transposase" in row:
                l.append(1)
            elif "Transposase" in row:
                l.append(1)
            elif "Insertion" in row:
                l.append(1)
            elif "insertion" in row:
                l.append(1)
            elif "CRISPR-associated" in row:
                l.append(0)
            elif "iron-sulfur cluster insertion protein ErpA" in row:
                l.append(0)
            elif "membrane protein insertion efficiency factor YidD" in row:
                l.append(0)
            else:
                l.append(0)

        input_sequence["target"] = l
        print("dependent variable added !")

        if save_dataframe:
            input_sequence.to_csv(work_path + "input_genome.csv")

        if create_summary:
            print("class distribution")
            print(input_sequence["target"].value_counts())

        return input_sequence

    def orchestrator(self,
                     main_dir,
                     save_dataframe=False,
                     create_summary=False):

        try:
            for item in os.listdir(main_dir):
                genome_name = item + "/"
                print("processing genome: " + genome_name + "--" * 10)

                # path_to_data = main_dir + genome_name

                fasta_file_processed = self.run_fasta(path_to_data=main_dir + genome_name)

                genome_reference = self.create_dataframe_from_fasta(input_fasta=fasta_file_processed,
                                                                    work_path=main_dir + genome_name,
                                                                    save_dataframe=save_dataframe)
                sequences_with_class = self.add_target(input_sequence=genome_reference,
                                                       work_path=main_dir + genome_name,
                                                       save_dataframe=save_dataframe,
                                                       create_summary=create_summary)

                print("done !")
        except OSError:
            print("genome is already unzipped !")