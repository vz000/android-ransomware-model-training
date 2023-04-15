import pandas as pd

'''
# param dataset_file - Name of the file where the list of permissions are included. Must be a csv.
                       Naming format: permissions-{type}.csv
# param out_file - output from static_stats module
# param n - N-gram size
'''
class permissions_ngram():
    def __init__(self, dataset_file : str, out_file, n : int) -> None:
        self.dataset_file = dataset_file
        self.out_file = out_file
        self.n = n
        self.final_list = []
        self.chunks = []
        self.times = []
        self.__generate_stats()
        self.__draft_detectors()
        
    def __generate_stats(self) -> None:
        file_permissions = self.out_file
        with open(file_permissions,'r') as list:
            for row in list:
                if "\n" in row:
                    row = row.rstrip()
                self.final_list.append(row)

    def __draft_detectors(self) -> None:
        with open(self.dataset_file,'r') as permissions:
            for row in permissions:
                permissions = row.split(",")
                end = len(permissions) - 1 # amount of permissions and end of list
                start = 0
                while start < end:
                    n_gram = permissions[start:start+self.n]
                    first_match = 0
                    clean_list = []
                    if len(n_gram) >= self.n:
                        for word in n_gram:
                            if word in self.final_list:
                                exp = self.final_list.index(word.rstrip())
                                clean_list.append(2**exp)
                                first_match += 1
                            else:
                                clean_list.append(0)
                        n_gram = sum(clean_list)
                    if first_match > 0:
                        if n_gram not in self.chunks:
                            self.chunks.append(n_gram)
                            self.times.append(1)
                        if n_gram in self.chunks:
                            index = self.chunks.index(n_gram)
                            self.times[index] += 1
                        start = start + self.n
                    else:
                        start += 1

    def get_draft_detectors(self) -> list:
        return self.chunks
    
    def get_permission_list(self) -> list:
        return self.final_list

    def get_detector_info(self):
        amount_detector = pd.DataFrame({'Detector':self.chunks,
                                        'Times':self.times})
        amount_detector = amount_detector.sort_values(by=['Times'],ascending=False)
        print(amount_detector.head(20))