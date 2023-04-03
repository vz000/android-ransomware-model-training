import csv
import sys
import os
from static_stats import permissions_stats
from static_ngram import permissions_ngram
from static_detectors import static_detectors

# To simulate the real case. Normal apps are stored inside of /data/app/
# TODO: Handle apk deletion when data cannot be read by aapt by rust main.

'''
#param step - Either 0 or 1. 0 - train, 1 - classify
#param n - n-gram size
'''
class static_model():
    def __init__(self, step, type: str, n = 3):
        self.step = step
        self.n = n
        self.type = type
        self.folder = "./out/"+self.type+"/"
        if self.step == -1:
            self.parse_permissions(self.folder)
        if self.step == 0:
            self.train_model()

    def train_model(self):
        stats = permissions_stats(self.type)
        out_stats_file = stats.get_output_file()
        perm_ngram = permissions_ngram(self.folder+"permissions.csv",out_stats_file,self.n)
        ngram = perm_ngram.get_draft_detectors()
        permission_list = perm_ngram.get_permission_list()
        detectors = static_detectors(self.n, ngram, permission_list, self.n)
        detectors.fit()

    def parse_permissions(self, datadir_name: str) -> None:
        datalist = os.listdir(datadir_name)
        for aapt_out in datalist:
            with open(datadir_name + aapt_out,"r", newline='') as out:
                apk_permissions = []
                for data in out:
                    if "uses-permission:" in data:
                        permission = data.split(" ")[1].split("=")[1][1:-3].split(".")[-1]
                        apk_permissions.append(permission)
                file_name = "./out/"+self.type+"/permissions.csv"
                with open(file_name, 'a+', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(apk_permissions)

main_static = static_model(int(sys.argv[1]),str(sys.argv[2]))