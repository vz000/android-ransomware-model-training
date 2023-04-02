import csv
import os

# To simulate the real case. Normal apps are stored inside of /data/app/
# TODO: Handle apk deletion when data cannot be read by aapt by rust main.

'''
#param step - Either 0 or 1. 0 - train, 1 - classify
#param n - n-gram size
'''
class static_model():
    def __init__(self, step = 0, n = 3):
        self.step = step
        self.n = n
        if self.step == 0:
            self.__parse_permissions__("./out/")

    def __parse_permissions__(self, datadir_name: str) -> None:
        datalist = os.listdir(datadir_name)
        for aapt_out in datalist:
            with open(datadir_name + aapt_out,"r", newline='') as out:
                apk_permissions = []
                for data in out:
                    if "uses-permission:" in data:
                        permission = data.split(" ")[1].split("=")[1][1:-3].split(".")[-1]
                        apk_permissions.append(permission)

                # Rust will call and this must be fixed to fit the directory
                with open('./out/permissions.csv', 'a+', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(apk_permissions)

main_static = static_model(0)