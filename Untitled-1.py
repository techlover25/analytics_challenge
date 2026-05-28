import sys
import os
print("Hello world!")

class Records:
    def __init__(self):
        self.existing_algorithms = []
        self.existing_datasets = []
        self.existing_results = []
        self.write_file = [] # Creating this list to capture all the data that has to be written on the reports file

    def validate_results(self, algorithm_name, new_results):
        counter = 0 

        # Below code is for verifying if the results for each algorithm has atleast 1 completed result.
        # If it does not, the program fails later, while calculating average
        for check_result in new_results:
            if check_result[1] != '' and check_result[1] != '404':
                counter += 1

        if counter == 0:
            print(f"Algorithm {algorithm_name} is still in progress or does not contain completed results")
            exit()
            
        for result in new_results:
            if result[1] != '' and result[1] != '404':
                try:
                    float(result[1])#[1]
                except:
                    #Checking if the result section of the results file has any data non float data. If yes, print message and exit the program
                    print("Result file contains invalid numbers")
                    exit()
            

    def read_results(self, result_file):
        try:
            if os.path.getsize(result_file) == 0:#[2]
                # Check if the result file is empty. If yes, print message and exit the program
                print("Result file is empty!")
                exit() 
            with open(result_file, 'r') as file:
                for line in file:
                    fields_from_line = line.split(',')
                    algorithm_name = fields_from_line[0].strip()
                    results = fields_from_line[1:]
                    new_results = [result.split(':') for result in results]
                    stripped_results = [[element.strip() for element in inner_list] for inner_list in new_results]
                    self.validate_results(algorithm_name, stripped_results)
                    self.existing_results.append(Result(algorithm_name, stripped_results))  
        except FileNotFoundError:
            # If the results file is not found, print message and exit the program
            print("Result file not found.")
            exit()

    # Priting the table information and also storing data for file write
    def print_data(self,print_file,print_mode):
        row_width = []

        max_column_widths = [max(len(str(item)) for item in col) for col in zip(*print_file)]

        # Below code is used for measuring the frame width of the table. Used for inserting '-' (hyphens)
        for row in print_file:
            formatted_row = "{:<{width}}  ".format(row[0], width=max_column_widths[0]) + "{:<{width}}  ".format(row[1], width=max_column_widths[1]) + "  ".join("{:>{width}}".format(item, width=width) for item, width in zip(row[2:], max_column_widths[2:]))
            row_width.append(len(formatted_row))
        frame_width = max(row_width)

        print("-" * frame_width)
        self.write_file.append("-" * frame_width+"\n")
        row_count=1
        for row in print_file:
            # Using print mode 0, when I have to left align 1 column, i.e, Algorithms or Names
            if print_mode == 0:
                formatted_row = "{:<{width}}  ".format(row[0], width=max_column_widths[0]) + "{:<{width}}  ".format(row[1], width=max_column_widths[1]) + "  ".join("{:>{width}}".format(item, width=width) for item, width in zip(row[2:], max_column_widths[2:]))
            # Using print mode 1, when I have to left align 2 columns, i.e, Dataset ID as well as Name for the dataset class
            else:
                formatted_row = "{:<{width}}  ".format(row[0], width=max_column_widths[0]) + "{:<{width}}  ".format(row[1], width=max_column_widths[1]) + "{:<{width}}  ".format(row[2], width=max_column_widths[2]) + "  ".join("{:>{width}}".format(item, width=width) for item, width in zip(row[3:], max_column_widths[3:]))
            print(formatted_row)
            self.write_file.append(formatted_row+"\n")
            if row_count == 1:
                print("-" * frame_width)
                self.write_file.append("-" * frame_width+"\n")
            row_count += 1
        print("-" * frame_width)
        self.write_file.append("-" * frame_width +"\n")

    def display_results(self):
        nonexistent_results = 0
        ongoing_results = 0
        algorithm_len = 0
        datasets = []
        print_file = []

        print("RESULTS")
        self.write_file.append("RESULTS\n")   

        for dataset in self.existing_results:
            for j in dataset.get_results():
                datasets.append(j[0])
        datasets = set(datasets)
        datasets = sorted(list(datasets))
        header = ["|","Algorithm"] + datasets + ["|"]
        print_file.append(header)
        
        for result in self.existing_results:
            algorithm_len += 1
            row = [result.get_algorithm_name()]
            for i in result.get_results():
                # If no result is found, inserting 'XX' in the table
                if i[1] == '':
                    row.append("XX")
                    nonexistent_results += 1
                # If result is still ongoing, inserting '--' in the table
                elif i[1] == "404":
                    row.append("--")
                    ongoing_results += 1
                else:
                    row.append(round(float(i[1]),1))
            # Appending '|' at the end and beginning of the file for formatting
            row.insert(0,"|")
            row.append("|")
            print_file.append(row)

        self.print_data(print_file,0)
        print("\nRESULTS SUMMARY")
        print(f"There are {algorithm_len} algorithms and {len(datasets)} datasets.")
        print(f"The number of nonexistent results is {nonexistent_results} and on-going results is {ongoing_results}.")
        
        self.write_file.append("\nRESULTS SUMMARY\n")
        self.write_file.append(f"There are {algorithm_len} algorithms and {len(datasets)} datasets.\n")
        self.write_file.append(f"The number of nonexistent results is {nonexistent_results} and on-going results is {ongoing_results}.\n")

    def validate_datasetID(self, id, weight):
        if id.startswith('D'):
            try:
                #Checking if dataset id in the file is of correct format. Otherwise displaying message and exiting the program
                int(id[1:-1])
            except ValueError:
                print("The dataset ID doesn't have 2 integer numbers in the middle")
                exit()
            # Checking if the complexity of the simple dataset is 1. Otherwise displaying message and exiting the program
            if id.endswith('S'):
                if int(weight) != 1:
                    print(f"Complexity weight should be 1 for simple dataset {id}.")
                    exit()
            elif id.endswith('A'):
            # Checking if the complexity of the advanced dataset is more than 5. If yes, displaying message and exiting the program
                if int(weight) > 5:
                    print(f"Complexity weight cannot be greater than 5 for advanced dataset {id}.")
                    exit()
            else:
                # Exiting the program as the dataset ID has last character other than 'S' and 'A'
                print("The dataset ID doesn't end with either S or A")
                exit()
        else:
            # Exiting the program as the dataset ID doesn't start with 'D'
            print("The dataset ID doesn't start with letter D")
            exit()

    def read_datasets(self, dataset_file):
        try:
            ## Check if the datasets file is empty. If yes, print message and exit the program
            if os.path.getsize(dataset_file) == 0:#[2]
                print("Dataset file is empty!")
                exit()             
            with open(dataset_file, 'r') as file:
                for line in file:
                    fields_from_line = line.split(',')
                    id = fields_from_line[0].strip()
                    name = fields_from_line[1].strip()
                    weight = fields_from_line[2].strip()
                    num_data_points = fields_from_line[3].strip()
                    source = fields_from_line[4].strip()
                    self.validate_datasetID(id, weight)
                    self.existing_datasets.append(Dataset(id, name, int(weight), int(num_data_points), source))
        # If the datasets file is not found, print message and exit the program
        except FileNotFoundError:
            print(f"Dataset file does not exist")
            exit()

    def display_simple_datasets(self):
        print_file = []
        print("\n\n\nSIMPLE DATASET INFORMATION")
        self.write_file.append("\n\n\nSIMPLE DATASET INFORMATION\n")
        header = ["|","DatasetID","Name","Type","Weight","Ndata","Source","Average","Range","Nfail","|"]
        print_file.append(header)
        
        fail_dict = {}
        average_dict = {}

        for dataset in self.existing_datasets:
            average_result = 0
            count = 0
            nfail = 0
            range_list = []

            if dataset.get_id()[-1] == 'S':
            
                average_result, count, nfail, range_list  = dataset.compute(self.existing_results, average_result, count, nfail, range_list)
                row = [dataset.get_id()]

                row.append(dataset.get_name()+'')
                row.append(dataset.get_id()[-1])
                row.append(str(dataset.get_complexity_weight()))
                row.append(str(dataset.get_num_data_points()))
                row.append(dataset.get_source())
                fail_dict.update({dataset.get_name() : nfail})
                average_dict.update({dataset.get_name() : round(average_result/count,1)})
                row.append(str(round(average_result/count,1)))
                row.append(str(f"{min(range_list)}  -  {max(range_list)}"))
                row.append(str(nfail))
                row.insert(0,"|")
                row.append("|")
                print_file.append(row)

        # Sorting the dataset based on the Average, without the header row [4]
        print_desc = sorted(print_file[1:], key=lambda x: float(x[7]), reverse= True)

        # Adding the header row back to the sorted dataset
        print_desc.insert(0, print_file[0])

        self.print_data(print_desc,1)

        max_fail = max(fail_dict, key=fail_dict.get)#[3]
        min_average = min(average_dict, key=average_dict.get)

        print("\nSIMPLE DATASETS SUMMARY")
        print(f"The most difficult dataset is {min_average} with an average of {average_dict[min_average]}.")
        print(f"The dataset with the most failures is {max_fail} with the number of failures being {fail_dict[max_fail]}.")
        self.write_file.append("\nSIMPLE DATASETS SUMMARY\n")
        self.write_file.append(f"The most difficult dataset is {min_average} with an average of {average_dict[min_average]}.\n")
        self.write_file.append(f"The dataset with the most failures is {max_fail} with the number of failures being {fail_dict[max_fail]}.\n")   

    def display_adv_datasets(self):
        print_file = []
        print("\n\n\nADVANCED DATASET INFORMATION")
        self.write_file.append("\n\n\nADVANCED DATASET INFORMATION\n")
        header = ["|","DatasetID","Name","Type","Weight","Ndata","Source","Average","Range","Nfail","|"]
        print_file.append(header)
        
        fail_dict = {}
        average_dict = {}

        for dataset in self.existing_datasets:
            average_result = 0
            count = 0
            nfail = 0
            range_list = []

            if dataset.get_id()[-1] == 'A':            
                average_result, count, nfail, range_list  = dataset.compute(self.existing_results, average_result, count, nfail, range_list)
                row = [dataset.get_id()]

                row.append(dataset.get_name()+'')
                row.append(dataset.get_id()[-1])
                row.append(str(dataset.get_complexity_weight()))
                row.append(str(dataset.get_num_data_points()))
                row.append(dataset.get_source())
                fail_dict.update({dataset.get_name() : nfail})
                average_dict.update({dataset.get_name() : round(average_result/count,1)})
                row.append(str(round(average_result/count,1)))
                row.append(str(f"{min(range_list)}  -  {max(range_list)}"))
                row.append(str(nfail))
                row.insert(0,"|")
                row.append("|")
                print_file.append(row)

        # Sorting the dataset based on the Average, without the header row [4]
        print_desc = sorted(print_file[1:], key=lambda x: float(x[7]), reverse= True)

        # Adding the header row back to the sorted dataset
        print_desc.insert(0, print_file[0])

        self.print_data(print_desc,1)

        max_fail = max(fail_dict, key=fail_dict.get)#[3]
        min_average = min(average_dict, key=average_dict.get)

        print("\nADVANCED DATASETS SUMMARY")
        print(f"The most difficult dataset is {min_average} with an average of {average_dict[min_average]}.")
        print(f"The dataset with the most failures is {max_fail} with the number of failures being {fail_dict[max_fail]}.")
        self.write_file.append("\nADVANCED DATASETS SUMMARY\n")
        self.write_file.append(f"The most difficult dataset is {min_average} with an average of {average_dict[min_average]}.\n")
        self.write_file.append(f"The dataset with the most failures is {max_fail} with the number of failures being {fail_dict[max_fail]}.\n")     

    def read_algorithms(self, algorithm_file):
        try:
            # Check if the algorithms file is empty. If yes, print message and exit the program
            if os.path.getsize(algorithm_file) == 0:#[2]
                print("Algorithm file is empty!")
                exit() 
            with open(algorithm_file, 'r') as file:
                for line in file:
                    fields_from_line = line.split(',')
                    name = fields_from_line[0].strip()
                    type = fields_from_line[1].strip()
                    year = fields_from_line[2].strip()
                    authors = fields_from_line[3:]
                    stripped_authors = [author.strip() for author in authors]
                    if type == 'DL':
                        self.existing_algorithms.append(DLAlgorithm(name, type, year, stripped_authors))
                    elif type == 'ML':
                        self.existing_algorithms.append(MLAlgorithm(name, type, year, stripped_authors))
                    else:
                        print("The algorithm file can support only DL and ML algorithms")
                        exit()
        except FileNotFoundError:
            # If the algorithms file is not found, print message and exit the program
            print(f"Algorithm file does not exist")
            exit()

    def display_MLalgorithms(self):
        print_file = []
        print("\n\n\nML ALGORITHM INFORMATION")
        self.write_file.append("\n\n\nML ALGORITHM INFORMATION\n")     
        header = ["|","Name","Type","Year","Authors","Average", "Score", "NFail","FailDataset","Ongoing","|"]
        print_file.append(header)

        fail_dict = {}
        average_dict = {}
        
        for algorithm in self.existing_algorithms:  
            average_result = 0
            count = 0
            nfail = 0
            ongoing = 0
            success = 1
            faildataset = []
            score_dict = {}   
            
            if algorithm.get_algorithm_type() == 'ML':
                average_result, count, nfail, ongoing, faildataset, success  = algorithm.compute_ML(self.existing_results, average_result, count, nfail, ongoing, faildataset)
            
                fail_dict.update({algorithm.get_algorithm_name() : nfail})
                average_dict.update({algorithm.get_algorithm_name() : round(average_result/count,1)})
                score_dict = algorithm.get_score(self.existing_results)

                if int(success) == 0:
                    row = [algorithm.get_algorithm_name() + ' (!)']
                else:
                    row = [algorithm.get_algorithm_name()]
                row.append(algorithm.get_algorithm_type())
                row.append(algorithm.get_algorithm_year())
                row.append("-".join(algorithm.authors))
                row.append(str(round(average_result/count,1)))
                row.append(score_dict[algorithm.get_algorithm_name()])
                row.append(str(nfail))
                row.append(", ".join(faildataset))
                row.append(str(ongoing))
                row.insert(0,"|")
                row.append("|")
                print_file.append(row)

        # Sorting the dataset based on the Score, without the header row [4]
        print_desc = sorted(print_file[1:], key=lambda x: float(x[6]), reverse= True)

        # Adding the header row back to the sorted algorithms
        print_desc.insert(0, print_file[0])

        self.print_data(print_desc,0)

        min_fail = min(fail_dict, key=fail_dict.get)#[3]
        max_average = max(average_dict, key=average_dict.get)

        print("\nML ALGORITHM SUMMARY")
        print(f"The best algorithm is {max_average} with an average result of {average_dict[max_average]}.")
        print(f"The algorithm with the least failures is {min_fail} with the number of failures being {fail_dict[min_fail]}.")
        self.write_file.append("\nML ALGORITHM SUMMARY\n")
        self.write_file.append(f"The best algorithm is {max_average} with an average result of {average_dict[max_average]}.\n")
        self.write_file.append(f"The algorithm with the least failures is {min_fail} with the number of failures being {fail_dict[min_fail]}.\n")

    def display_DLalgorithms(self):
        print_file = []
        print("\n\n\nDL ALGORITHM INFORMATION")
        self.write_file.append("\n\n\nDL ALGORITHM INFORMATION\n")      
        header = ["|","Name","Type","Year","Authors","Average", "Score", "NFail","FailDataset","Ongoing","|"]
        print_file.append(header)

        fail_dict = {}
        average_dict = {}
        
        for algorithm in self.existing_algorithms:  
            average_result = 0
            count = 0
            nfail = 0
            ongoing = 0
            success = 1
            faildataset = []
            score_dict = {}   
            
            if algorithm.get_algorithm_type() == 'DL':
                average_result, count, nfail, ongoing, faildataset, success  = algorithm.compute_DL(self.existing_results, average_result, count, nfail, ongoing, faildataset)

                fail_dict.update({algorithm.get_algorithm_name() : nfail})
                average_dict.update({algorithm.get_algorithm_name() : round(average_result/count,1)})
                score_dict = algorithm.get_score(self.existing_results)

                if int(success) == 0:
                    row = [algorithm.get_algorithm_name() + ' (!)']
                else:
                    row = [algorithm.get_algorithm_name()]
                row.append(algorithm.get_algorithm_type())
                row.append(algorithm.get_algorithm_year())
                row.append("-".join(algorithm.authors))
                row.append(str(round(average_result/count,1)))
                row.append(score_dict[algorithm.get_algorithm_name()])
                row.append(str(nfail))
                row.append(", ".join(faildataset))
                row.append(str(ongoing))
                row.insert(0,"|")
                row.append("|")
                print_file.append(row)

        # Sorting the dataset based on the Score, without the header row [4]
        print_desc = sorted(print_file[1:], key=lambda x: float(x[6]), reverse= True)

        # Adding the header row back to the sorted algorithms
        print_desc.insert(0, print_file[0])

        self.print_data(print_desc,0)

        min_fail = min(fail_dict, key=fail_dict.get)#[3]
        max_average = max(average_dict, key=average_dict.get)

        print("\nDL ALGORITHM SUMMARY")
        print(f"The best algorithm is {max_average} with an average result of {average_dict[max_average]}.")
        print(f"The algorithm with the least failures is {min_fail} with the number of failures being {fail_dict[min_fail]}.")
        self.write_file.append("\nDL ALGORITHM SUMMARY\n")
        self.write_file.append(f"The best algorithm is {max_average} with an average result of {average_dict[max_average]}.\n")
        self.write_file.append(f"The algorithm with the least failures is {min_fail} with the number of failures being {fail_dict[min_fail]}.\n")

    # Below method is used for writing the report file
    def write_into_file(self):
        # Try-catch block is used to determine if the 'reports.txt' file already exists
        # If exists, we read the data from the previous report and append that below along with the new report
        # If does not exists, we create a new 'reports.txt' file
        try:
            file = open('reports.txt', 'r')
            previous_data = file.read()
            file.close()

            self.write_file = self.write_file + list("\n") + list(previous_data)
            f = open("reports.txt", "w")
            current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")#[6]
            f.write(f"This report is generated on {current_time}\n")
            f.writelines(self.write_file)
            f.close()

        except FileNotFoundError:
            f = open("reports.txt", "x")
            current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")#[6]
            f.write(f"This report is generated on {current_time}\n")
            f.writelines(self.write_file)
            f.close()

class Operations:

    # Operation is the main class for this program, which calls the execute method.
    # Here, I have repeated the read and display methods for different inputs because I want to diplay the error message while reading the file itself.
    # Rather than writing on the "reports.txt" file and generating error later.

    def execute(self):

        records = Records()

        if len(sys.argv) < 2 or len(sys.argv) > 4:
            if len(sys.argv) < 2:
                print("Usage: python your_script.py result_file_name")
            else:
                print("Usage: python your_script.py result_file_name dataset_file_name algorithm_file_name")
                exit()
        elif len(sys.argv) == 2:
            result_file = sys.argv[1]
            records.read_results(result_file)
            records.display_results()
            records.write_into_file()
        elif len(sys.argv) == 3:
            result_file = sys.argv[1]
            dataset_file = sys.argv[2]
            records.read_results(result_file)
            records.read_datasets(dataset_file)
            records.display_results()
            records.display_simple_datasets()
            records.display_adv_datasets()
            records.write_into_file()
        elif len(sys.argv) == 4:
            result_file = sys.argv[1]
            dataset_file = sys.argv[2]
            algorithm_file = sys.argv[3]
            records.read_results(result_file)
            records.read_datasets(dataset_file)
            records.read_algorithms(algorithm_file)
            records.display_results()
            records.display_simple_datasets()
            records.display_adv_datasets()
            records.display_MLalgorithms()
            records.display_DLalgorithms()
            records.write_into_file()

operation = Operations()
operation.execute()