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

    def validate_results(self, new_results):
        if not new_results:
            print("Result file cannot be empty")
            exit()
        for result in new_results:
            if result[1] != '' or result[1] != "404":
                if result[1].isalpha():
                    print("Result file contains invalid numbers")
                    exit()
        

    def read_results(self, result_file):
        try:
            with open(result_file, 'r') as file:
                for line in file:
                    algorithm_name, *results = line.strip().split(', ')
                    new_results = [result.split(': ') for result in results]
                    self.validate_results(new_results)
                    self.existing_results.append(Result(algorithm_name, new_results))
                
        except FileNotFoundError:
            print("Result file not found.")
            exit()

    def print_Data(self,print_file,print_mode):
        row_width = []

        max_column_widths = [max(len(str(item)) for item in col) for col in zip(*print_file)]

        for row in print_file:
            formatted_row = "{:<{width}}  ".format(row[0], width=max_column_widths[0]) + "{:<{width}}  ".format(row[1], width=max_column_widths[1]) + "  ".join("{:>{width}}".format(item, width=width) for item, width in zip(row[2:], max_column_widths[2:]))
            row_width.append(len(formatted_row))
        frame_width = max(row_width)

        print("-" * frame_width)
        row_count=1
        for row in print_file:
            if print_mode == 0:
                formatted_row = "{:<{width}}  ".format(row[0], width=max_column_widths[0]) + "{:<{width}}  ".format(row[1], width=max_column_widths[1]) + "  ".join("{:>{width}}".format(item, width=width) for item, width in zip(row[2:], max_column_widths[2:]))
            else:
                formatted_row = "{:<{width}}  ".format(row[0], width=max_column_widths[0]) + "{:<{width}}  ".format(row[1], width=max_column_widths[1]) + "{:<{width}}  ".format(row[2], width=max_column_widths[2]) + "  ".join("{:>{width}}".format(item, width=width) for item, width in zip(row[3:], max_column_widths[3:]))
            print(formatted_row)
            if row_count == 1:
                print("-" * frame_width)
            row_count += 1
        print("-" * frame_width)

    def display_results(self):
        nonexistent_results = 0
        ongoing_results = 0
        algorithm_len = 0
        datasets = []
        print_file = []

        print("RESULTS")
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
                if i[1] == '':
                    row.append("XX")
                    nonexistent_results += 1
                elif i[1] == "404":
                    row.append("--")
                    ongoing_results += 1
                else:
                    row.append(i[1])
            row.insert(0,"|")
            row.append("|")
            print_file.append(row)

        self.print_Data(print_file,0)
        print("\nRESULTS SUMMARY")
        print(f"There are {algorithm_len} algorithms and {len(datasets)} datasets.")
        print(f"The number of nonexistent results is {nonexistent_results} and on-going results is {ongoing_results}.")

    def validate_datasetID(self, id, weight):
        if id.startswith('D'):
            try:
                int(id[1:-2])
            except ValueError:
                print("The dataset ID doesn't have 2 integer numbers in the middle")
                exit()
            if id.endswith('S'):
                if int(weight) != 1:
                    print(f"Complexity weight should be 1 for simple dataset {id}.")
                    exit()
            elif id.endswith('A'):
                if int(weight) > 5:
                    print(f"Complexity weight should be 1 for simple dataset {id}.")
                    exit()
            else:
                print("The dataset ID doesn't end with either S or A")
                exit()
        else:
            print("The dataset ID doesn't start with letter D")
            exit()

    def read_datasets(self, dataset_file):
        try:
            with open(dataset_file, 'r') as file:
                for line in file:
                    id, name, weight, num_data_points, source = line.strip().split(', ')
                    self.validate_datasetID(id, weight)
                    self.existing_datasets.append(Dataset(id, name, int(weight), int(num_data_points), source))
        except FileNotFoundError:
            print(f"Dataset file does not exist")
            exit()

    def display_datasets(self):
        print_file = []
        print("\n\n\nDATASET INFORMATION")
        #print("-" * (102))
        header = ["|","DatasetID","Name","Type","Weight","Ndata","Source","Average","Range","Nfail","|"]
        print_file.append(header)
        #print("-" * (102))
        
        fail_dict = {}
        average_dict = {}

        for dataset in self.existing_datasets:
            average_result = 0
            count = 0
            nfail = 0
            range_list = []
            
            row = [dataset.get_id()]
            row.append(dataset.get_name())
            row.append(dataset.get_id()[-1])
            row.append(str(dataset.get_complexity_weight()))
            row.append(str(dataset.get_num_data_points()))
            row.append(dataset.get_source())
            for result in self.existing_results:
                for i in result.get_results():
                    if i[0] == dataset.get_id():
                        if i[1] == '':
                            nfail += 1
                        elif i[1] != '404':
                            average_result += float(i[1])
                            count += 1
                            range_list.append(i[1])
            fail_dict.update({dataset.get_name() : nfail})
            average_dict.update({dataset.get_name() : round(average_result/count,1)})
            row.append(str(round(average_result/count,1)))
            row.append(str(f"{min(range_list)}  -  {max(range_list)}"))
            row.append(str(nfail))
            row.insert(0,"|")
            row.append("|")
            print_file.append(row)

        self.print_Data(print_file,1)

        #https://www.entechin.com/how-to-find-the-max-value-in-a-dictionary-in-python/
        max_fail = max(fail_dict, key=fail_dict.get)
        min_average = min(average_dict, key=average_dict.get)

        print("\nDATASETS SUMMARY")
        print(f"The most difficult dataset is {min_average} with an average of {average_dict[min_average]}.")
        print(f"The dataset with the most failures is {max_fail} with the number of failures being {fail_dict[max_fail]}.")

    def read_algorithms(self, algorithm_file):
        try:
            with open(algorithm_file, 'r') as file:
                for line in file:
                    name, type, year, *authors = line.strip().split(', ')
                    self.existing_algorithms.append(Algorithm(name, type, year, authors))
        except FileNotFoundError:
            print(f"Algorithm file does not exist")
            exit()

    def display_algorithms(self):
        print_file = []
        print("\n\n\nALGORITHM INFORMATION")
        #print("-" * (102))
        header = ["|","Name","Type","Year","Authors","Average","NFail","FailDataset","Ongoing","|"]
        print_file.append(header)
        #print("-" * (102))

        fail_dict = {}
        average_dict = {}
        
        for algorithm in self.existing_algorithms:  
            average_result = 0
            count = 0
            nfail = 0
            ongoing = 0
            range_list = []  
            faildataset = ''       
            row = [algorithm.get_algorithm_name()]
            row.append(algorithm.get_algorithm_type())
            row.append(algorithm.get_algorithm_year())
            row.append("-".join(algorithm.authors))
            for result in self.existing_results:
                if result.get_algorithm_name() == algorithm.get_algorithm_name():
                    for i in result.get_results(): 
                        if i[1] == '':
                            nfail += 1
                            faildataset = i[0]
                        elif i[1] == '404':
                            ongoing += 1
                        else:
                            average_result += float(i[1])
                            count += 1
                            range_list.append(i[1])
            fail_dict.update({algorithm.get_algorithm_name() : nfail})
            average_dict.update({algorithm.get_algorithm_name() : round(average_result/count,1)})
            row.append(str(round(average_result/count,1)))
            row.append(str(nfail))
            row.append(str(faildataset))
            row.append(str(ongoing))
            row.insert(0,"|")
            row.append("|")
            print_file.append(row)

        self.print_Data(print_file,0)

        #https://www.entechin.com/how-to-find-the-max-value-in-a-dictionary-in-python/
        min_fail = min(fail_dict, key=fail_dict.get)
        max_average = max(average_dict, key=average_dict.get)

        print("\nALGORITHM SUMMARY")
        print(f"The best algorithm is {max_average} with an average result of {average_dict[max_average]}.")
        print(f"The algorithm with the least failures is {min_fail} with the number of failures being {fail_dict[min_fail]}.")

class Operations:

    def execute(self):
        import sys

        records = Records()

        #if len(sys.argv) < 2 or len(sys.argv) > 4:
        #    if len(sys.argv) < 2:
        #        print("Usage: python your_script.py result_file_name")
        #    else:
        #        print("Usage: python your_script.py result_file_name dataset_file_name algorithm_file_name")
        #        exit()
        #if len(sys.argv) == 2:
        #    result_file = sys.argv[1]
        #    records = Records()
        #records.read_results(result_file)
        #records.display_results()
        #if len(sys.argv) == 3:
        #    result_file = sys.argv[1]
        #    dataset_file = sys.argv[2]
        #    records = Records()
        records.read_results("results.txt")
        records.read_datasets("datasets.txt")
        records.display_results()
        records.display_datasets()
        #if len(sys.argv) == 4:
        #    algorithm_file = sys.argv[3]
        records.read_algorithms("algorithms.txt")
        records.display_algorithms()

operation = Operations()
operation.execute()