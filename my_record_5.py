# Name : Kaustubh Kulpe
# Student ID : s3957275
# I have attempted part HD of the assignment. In the HD part, point 2 and 3 for displaying dataset and algorithms, I was not able to sort them based on average and score column respectively.
# One particular challenge was implementing the code for obtaining the scores on the algorithm tables. It was difficult to get the index of the top 1,2,3 algorithms for each dataset. After 
# spending a lot of time, I was able to implement it. But the code didn't feel like object-oriented. 
# Another issue was while reading the results file, if the result for the last dataset is null, the program fail with an error.
 
import sys
import os

class Algorithm:
    def __init__(self, name, type, year, authors = []):
        self.name = name
        self.type = type
        self.year = year
        self.authors = authors

    def get_algorithm_name(self):
        return self.name
    
    def get_algorithm_type(self):
        return self.type

    def get_algorithm_year(self):
        return self.year

    def get_algorithm_authors(self):
        return self.authors

    def get_score(self, results):
        algorithm_list = []
        result_data = []
        
        for result in results:
            algorithm_list.append(result.get_algorithm_name())
            for i in result.get_results():
                if i[1] == '' or i[1] == '404':
                    result_data.append([i[0],float(0)])
                else:
                    result_data.append([i[0], float(i[1])])
                
        # Creating a dictionary to store the unique lists for each dataset_id
        unique_datasets = {}

        for entry in result_data:
            dataset_id, result = entry

            if dataset_id in unique_datasets:
                unique_datasets[dataset_id].append(result)
            else:
                unique_datasets[dataset_id] = [result]

        ranked_indices = []

        for results in unique_datasets.values():
            sorted_results = sorted(enumerate(results, 0), key=lambda x: x[1], reverse=True)
            rank_indices = []
    
            # Getting the indices for first, second, and third
            for i, rank in enumerate(sorted_results):
                rank_indices.append(int(rank[0]))
                if i >= 2:
                    break
            ranked_indices.append(rank_indices)
    
        score_list = []

        for rank in ranked_indices:
            for j in range(len(rank)):
                if j == 0:
                    score_list.append([algorithm_list[rank[j]],3])
                elif j == 1:
                    score_list.append([algorithm_list[rank[j]],2])
                elif j == 2:
                    score_list.append([algorithm_list[rank[j]],1])

        # Creating a dictionary to store the sum of scores for each algorithm
        algorithm_scores = {}

        # Iterating through the list and updating the scores for each algorithm
        for algorithm, score in score_list:
            if algorithm in algorithm_scores:
                algorithm_scores[algorithm] += score
            else:
                algorithm_scores[algorithm] = score

        return algorithm_scores


    # Computing the average sum, number of dataset:count, number of failures, ongoing and failed datasets
    def compute(self, results, average_result, count, nfail, ongoing, faildataset):
        successadvanceddataset = 0
        failedsimpledataset = 0
        for result in results:
            if result.get_algorithm_name() == self.get_algorithm_name():
                for i in result.get_results():
                    if i[1] == '':
                        if i[0].endswith('S'):
                            failedsimpledataset += 1
                        nfail += 1
                        faildataset.append(i[0])
                    elif i[1] == '404':
                        ongoing += 1
                        successadvanceddataset += 1
                    else:
                        if i[0].endswith('A'):
                            successadvanceddataset += 1
                        average_result += round(float(i[1]),1)
                        count += 1
        return average_result, count, nfail, ongoing, faildataset, successadvanceddataset, failedsimpledataset
    
class MLAlgorithm(Algorithm):
    def __init__(self, name, type, year, authors = []):
        super().__init__(name, type, year, authors)

    # Computing the average sum, number of dataset:count, number of failures, ongoing and failed datasets
    def compute_ML(self, result, average_result, count, nfail, ongoing, faildataset):
        average_result, count, nfail, ongoing, faildataset, successadvanceddataset, failedsimpledataset = self.compute(result, average_result, count, nfail, ongoing, faildataset)
        if successadvanceddataset > 0 and failedsimpledataset == 0:
            success = 1
        else: 
            success = 0
        return average_result, count, nfail, ongoing, faildataset, success

class DLAlgorithm(Algorithm):
    def __init__(self, name, type, year, authors = []):
        super().__init__(name, type, year, authors)

    # Computing the average sum, number of dataset:count, number of failures, ongoing and failed datasets    
    def compute_DL(self, result, average_result, count, nfail, ongoing, faildataset):
        average_result, count, nfail, ongoing, faildataset, successadvanceddataset, failedsimpledataset = self.compute(result, average_result, count, nfail, ongoing, faildataset)
        if successadvanceddataset > 1 and failedsimpledataset == 0:
            success = 1
        else: 
            success = 0
        return average_result, count, nfail, ongoing, faildataset, success

class Dataset:
    def __init__(self, id, name, complexity_weight, num_data_points, source):
        self.id = id
        self.name = name
        self.complexity_weight = complexity_weight 
        self.num_data_points = num_data_points
        self.source = source
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_complexity_weight(self):
        return self.complexity_weight
    
    def get_num_data_points(self):
        return self.num_data_points
    
    def get_source(self):
        return self.source

    # Computing the average sum, number of dataset:count, number of failures and the range of results    
    def compute(self, results, average_result, count, nfail, range_list):
        for result in results:
            for i in result.get_results():
                if i[0] == self.get_id():
                    if i[1] == '':
                        nfail += 1
                    elif i[1] != '404':
                        average_result += round(float(i[1]),1)
                        count += 1
                        range_list.append(round(float(i[1]),1))
        return average_result, count, nfail, range_list
    
class Result:
    def __init__(self, name, results = []):
        self.name = name
        self.results = results

    def get_algorithm_name(self):
        return self.name
    
    def get_results(self):
        return self.results

class Records:
    def __init__(self):
        self.existing_algorithms = []
        self.existing_datasets = []
        self.existing_results = []
        self.write_file = []

    def validate_results(self, new_results):
        for result in new_results:
            if result[1] != '' and result[1] != "404":
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
                    algorithm_name, *results = line.strip().split(', ')
                    new_results = [result.split(': ') for result in results]
                    self.validate_results(new_results)
                    self.existing_results.append(Result(algorithm_name, new_results))    
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

        f = open("reports.txt", "a")
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
        f.close()

    def display_results(self):
        nonexistent_results = 0
        ongoing_results = 0
        algorithm_len = 0
        datasets = []
        print_file = []

        f = open("reports.txt", "w")
        print("RESULTS")
        self.write_file.append("RESULTS\n")   
        f.close()

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
        
        f = open("reports.txt", "a")
        self.write_file.append("\nRESULTS SUMMARY\n")
        self.write_file.append(f"There are {algorithm_len} algorithms and {len(datasets)} datasets.\n")
        self.write_file.append(f"The number of nonexistent results is {nonexistent_results} and on-going results is {ongoing_results}.\n")
        f.close()

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
                    id, name, weight, num_data_points, source = line.strip().split(', ')
                    self.validate_datasetID(id, weight)
                    self.existing_datasets.append(Dataset(id, name, int(weight), int(num_data_points), source))
        # If the datasets file is not found, print message and exit the program
        except FileNotFoundError:
            print(f"Dataset file does not exist")
            exit()

    def display_simple_datasets(self):
        print_file = []
        f = open("reports.txt", "a")
        print("\n\n\nSIMPLE DATASET INFORMATION")
        self.write_file.append("\n\n\nSIMPLE DATASET INFORMATION\n")
        f.close()
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

        self.print_data(print_file,1)

        max_fail = max(fail_dict, key=fail_dict.get)#[3]
        min_average = min(average_dict, key=average_dict.get)

        f = open("reports.txt", "a")
        print("\nSIMPLE DATASETS SUMMARY")
        print(f"The most difficult dataset is {min_average} with an average of {average_dict[min_average]}.")
        print(f"The dataset with the most failures is {max_fail} with the number of failures being {fail_dict[max_fail]}.")
        self.write_file.append("\nSIMPLE DATASETS SUMMARY\n")
        self.write_file.append(f"The most difficult dataset is {min_average} with an average of {average_dict[min_average]}.\n")
        self.write_file.append(f"The dataset with the most failures is {max_fail} with the number of failures being {fail_dict[max_fail]}.\n")   
        f.close()

    def display_adv_datasets(self):
        print_file = []
        f = open("reports.txt", "a")
        print("\n\n\nADVANCED DATASET INFORMATION")
        self.write_file.append("\n\n\nADVANCED DATASET INFORMATION\n")
        f.close()
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

        self.print_data(print_file,1)

        max_fail = max(fail_dict, key=fail_dict.get)#[3]
        min_average = min(average_dict, key=average_dict.get)

        f = open("reports.txt", "a")
        print("\nADVANCED DATASETS SUMMARY")
        print(f"The most difficult dataset is {min_average} with an average of {average_dict[min_average]}.")
        print(f"The dataset with the most failures is {max_fail} with the number of failures being {fail_dict[max_fail]}.")
        self.write_file.append("\nADVANCED DATASETS SUMMARY\n")
        self.write_file.append(f"The most difficult dataset is {min_average} with an average of {average_dict[min_average]}.\n")
        self.write_file.append(f"The dataset with the most failures is {max_fail} with the number of failures being {fail_dict[max_fail]}.\n")   
        f.close()     

    def read_algorithms(self, algorithm_file):
        try:
            # Check if the algorithms file is empty. If yes, print message and exit the program
            if os.path.getsize(algorithm_file) == 0:#[2]
                print("Algorithm file is empty!")
                exit() 
            with open(algorithm_file, 'r') as file:
                for line in file:
                    name, type, year, *authors = line.strip().split(', ')
                    if type == 'DL':
                        self.existing_algorithms.append(DLAlgorithm(name, type, year, authors))
                    elif type == 'ML':
                        self.existing_algorithms.append(MLAlgorithm(name, type, year, authors))
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
        f = open("reports.txt", "a")
        self.write_file.append("\n\n\nML ALGORITHM INFORMATION\n")
        f.close()        
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

        self.print_data(print_file,0)

        min_fail = min(fail_dict, key=fail_dict.get)#[3]
        max_average = max(average_dict, key=average_dict.get)

        f = open("reports.txt", "a")
        print("\nML ALGORITHM SUMMARY")
        print(f"The best algorithm is {max_average} with an average result of {average_dict[max_average]}.")
        print(f"The algorithm with the least failures is {min_fail} with the number of failures being {fail_dict[min_fail]}.")
        self.write_file.append("\nML ALGORITHM SUMMARY\n")
        self.write_file.append(f"The best algorithm is {max_average} with an average result of {average_dict[max_average]}.\n")
        self.write_file.append(f"The algorithm with the least failures is {min_fail} with the number of failures being {fail_dict[min_fail]}.\n")
        f.close()

    def display_DLalgorithms(self):
        print_file = []
        print("\n\n\nDL ALGORITHM INFORMATION")
        f = open("reports.txt", "a")
        self.write_file.append("\n\n\nDL ALGORITHM INFORMATION\n")
        f.close()        
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

        self.print_data(print_file,0)

        min_fail = min(fail_dict, key=fail_dict.get)#[3]
        max_average = max(average_dict, key=average_dict.get)

        f = open("reports.txt", "a")
        print("\nDL ALGORITHM SUMMARY")
        print(f"The best algorithm is {max_average} with an average result of {average_dict[max_average]}.")
        print(f"The algorithm with the least failures is {min_fail} with the number of failures being {fail_dict[min_fail]}.")
        self.write_file.append("\nDL ALGORITHM SUMMARY\n")
        self.write_file.append(f"The best algorithm is {max_average} with an average result of {average_dict[max_average]}.\n")
        self.write_file.append(f"The algorithm with the least failures is {min_fail} with the number of failures being {fail_dict[min_fail]}.\n")
        f.close()

    def write_into_file(self):
        f = open("abcd.txt", "a")
        print("executed")
        f.writelines(self.write_file)
        f.close()

class Operations:

    def execute(self):
        import sys

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
            print("execute2")
            records.display_results()
            print("execute1")
            records.display_simple_datasets()
            records.display_adv_datasets()
            print("execute")
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


# References
#[1]“Here is how to check if a string is a float in Python,” pythonhow.com.(accessed Oct. 26, 2023) https://pythonhow.com/how/check-if-a-string-is-a-float/.
#[2]“Here is how to check if a text file is empty in Python,” pythonhow.com.(accessed Oct. 27, 2023) https://pythonhow.com/how/check-if-a-text-file-is-empty/.
#[3]Entechin, “How to find the max value in a dictionary in python?,” Entechin, Nov. 12, 2022. (accessed Oct. 28, 2023) https://www.entechin.com/how-to-find-the-max-value-in-a-dictionary-in-python/.
