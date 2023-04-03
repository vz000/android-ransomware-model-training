import csv
import sys
import os
from static_stats import permissions_stats

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
        if self.step == 0:
            self.__parse_permissions__("./out/" + self.type + "/")
            stats = permissions_stats(self.type)
            out_stats_file = stats.get_output_file()

    def __parse_permissions__(self, datadir_name: str) -> None:
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