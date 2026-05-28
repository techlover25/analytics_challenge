class Algorithm:
    def __init__(self, name, results = []):
        self.name = name
        self.results = results

    def get_algorithm_name(self):
        return self.name
    
    def get_results(self):
        return self.results

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

    def read_results(self, result_file):
        try:
            with open(result_file, 'r') as file:
                for line in file:
                    algorithm_name, *results = line.strip().split(', ')
                    new_results = [result.split(': ') for result in results]
                    self.existing_results.append(Result(algorithm_name, new_results))
        except FileNotFoundError:
            print("Result file not found.")

    def display_results(self):
        nonexistent_results = 0
        ongoing_results = 0
        algorithm_len = 0
        datasets = []

        
        print("RESULTS")
        for dataset in self.existing_results:
            for j in dataset.get_results():
                datasets.append(j[0])
        datasets = set(datasets)
        datasets = sorted(list(datasets))
        header = ["Algorithm"] + datasets
        print("-" * (43 + 5))
        print("|", "   ".join(header), "|")
        print("-" * (43 + 5))
        
        for result in self.existing_results:
            algorithm_len += 1
            row = [result.get_algorithm_name().ljust(12)]
            for i in result.get_results():
                if i[1] == '':
                    row.append("XX".rjust(5))
                    nonexistent_results += 1
                elif i[1] == "404":
                    row.append("--".rjust(5))
                    ongoing_results += 1
                else:
                    row.append(i[1].rjust(5))

            print("|", " ".join(row), "|")

        print("-" * (43 + 5))
        print("\nRESULTS SUMMARY")
        print(f"There are {algorithm_len} algorithms and {len(datasets)} datasets.")
        print(f"The number of nonexistent results is {nonexistent_results} and on-going results is {ongoing_results}.")

    def read_dataset(self, dataset_file):
        try:
            with open(dataset_file, 'r') as file:
                for line in file:
                    id, name, weight, num_data_points, source = line.strip().split(', ')
                    if id.endswith('S'):
                        if int(weight) == 1:
                            self.existing_datasets.append(Dataset(id, name, int(weight), int(num_data_points), source))
                        else:
                            print(f"Complexity weight should be 1 for simple dataset {id}.")
                            exit()
                    elif id.endswith('A'):
                        if int(weight) > 5:
                            print(f"Complexity weight should be 1 for simple dataset {id}.")
                            exit()
                        else:
                            self.existing_datasets.append(Dataset(id, name, int(weight), int(num_data_points), source))
        except FileNotFoundError:
            print(f"Dataset file does not exist")

    def display_dataset(self):
        print("\n\n\nDATASET INFORMATION")
        print("-" * (102))
        header = ["DatasetID","Name","Type","Weight","Ndata","Source","Average","Range","Nfail"]
        print("|", "      ".join(header), "|")
        print("-" * (102))
        
        fail_dict = {}
        average_dict = {}

        for dataset in self.existing_datasets:
            average_result = 0
            count = 0
            nfail = 0
            range_list = []
            
            row = [dataset.get_id().ljust(12)]
            row.append(dataset.get_name().ljust(12))
            row.append(dataset.get_id()[-1].ljust(12))
            row.append(str(dataset.get_complexity_weight()).ljust(8))
            row.append(str(dataset.get_num_data_points()).ljust(10))
            row.append(dataset.get_source().ljust(12))
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
            row.append(str(round(average_result/count,1)).ljust(10))
            row.append(str(f"{min(range_list)}  -  {max(range_list)}").ljust(15))
            row.append(str(nfail))
            print("|", " ".join(row), "|")

        #https://www.entechin.com/how-to-find-the-max-value-in-a-dictionary-in-python/
        max_fail = max(fail_dict, key=fail_dict.get)
        min_average = min(average_dict, key=average_dict.get)

        print("-" * (102))
        print("\nDATASETS SUMMARY")
        print(f"The most difficult dataset is {min_average} with an average of {average_dict[min_average]}.")
        print(f"The dataset with the most failures is {max_fail} with the number of failures being {fail_dict[max_fail]}.")


if __name__ == "__main__":
    import sys

    #if len(sys.argv) != 2:
    #    print("Usage: python your_script.py result_file_name")
    #else:
    #    result_file_name = sys.argv[1]
    records = Records()
    records.read_results('results.txt')
    records.display_results()
    records.read_dataset('datasets.txt')
    records.display_dataset()
