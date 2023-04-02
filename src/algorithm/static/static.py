import csv
import os

# To simulate the real case. Normal apps are stored inside of /data/app/
# TODO: Handle apk deletion when data cannot be read by aapt by rust main.
def parse_permissions(datadir_name):
    datalist = os.listdir(datadir_name)
    for aapt_out in datalist:
        with open(datadir_name + aapt_out,"r", newline='') as out:
            apk_permissions = []
            for data in out:
                if "uses-permission:" in data:
                    permission = data.split(" ")[1].split("=")[1][1:-3].split(".")[-1]
                    apk_permissions.append(permission)

            with open('../../../out/permissions.csv', 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(apk_permissions)

parse_permissions("../../../out/")