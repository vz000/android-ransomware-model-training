
class static_classify():
    def __init__(self, inputFile: str, n : int):
        self.inputFile = inputFile
        self.static_detectors = []
        self.permission_list = []
        self.n = n
        self.result_apk_tags = []
        self.__fetchDetectors__()
        self.__fetchPermissionList__()

    def __fetchDetectors__(self) -> None:
        with open('./out/static-detectors.csv','r') as readData:
            for row in readData:
                static_detectors = row.split(",")
                break
        self.static_detectors = [int(x) for x in static_detectors]

    def __fetchPermissionList__(self) -> None:
        with open('./out/ransomware/static.csv','r') as list:
            for row in list:
                if "\n" in row:
                    row = row.rstrip()
                self.permission_list.append(row)

    def classify(self) -> list:
        with open(self.inputFile) as permissions:
            for row in permissions:
                if len(row) > 0:
                    input_app = []
                    permission = row.split(",")
                    start = 0
                    n_local_ngrams = 0
                    r = 4
                    while n_local_ngrams < r:
                        n_gram = permission[start:start+3]
                        clean_list = []
                        if len(n_gram) >= self.n:
                            for word in n_gram:
                                if word in self.permission_list:
                                    exp = self.permission_list.index(word.rstrip())
                                    clean_list.append(2**exp)
                                else:
                                    clean_list.append(0)
                            n_gram = sum(clean_list)
                            input_app.append(n_gram)
                            start += 1
                            n_local_ngrams += 1
                        else:
                            break
                
                    result = 0
                    for detector in self.static_detectors:
                        if detector in input_app:
                            result = 1
                            break

                    if result > 0:
                        self.result_apk_tags.append({
                            'name': permission[-1].rstrip(),
                            'static': 1,
                            'dynamic': 0
                        })
                    else:
                        self.result_apk_tags.append({
                            'name': permission[-1].rstrip(),
                            'static': 0,
                            'dynamic': 0
                        })
        
        return self.result_apk_tags
