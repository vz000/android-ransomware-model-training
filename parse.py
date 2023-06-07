import os
import csv

class parse_static_data:
    def __init__(self,datadir_name: str, type: str, phase: str) -> None:
        self.datadir_name = datadir_name
        self.type = type
        self.phase = phase
        self.apk_tags = []
        self.__get_data_from_apk__()
        self.__parse_permissions__()

    def __get_data_from_apk__(self) -> None:
        in_folder = "./data/"+self.type+"/static/"+self.phase+"/"
        print("Analyzing packages under /data/{}/static/{}/".format(self.type,self.phase))
        packages = os.listdir(in_folder)
        base_out_dir_name = "./out/"+ self.type
        out_dir_names = [base_out_dir_name,base_out_dir_name+"/static/",base_out_dir_name+"/static/"+ self.phase]
        if not os.path.isdir(base_out_dir_name):
            for dir_names in out_dir_names:
                os.mkdir(dir_names)
        if self.phase == "classify":
            os.mkdir(out_dir_names[2])
        
        package_num = 0
        for package in packages:
            if ".apk" in package:
                os.system("aapt dump permissions " + in_folder + package + " > " + out_dir_names[2] +"/aapt_output"+str(package_num)+".txt")
                package_num += 1

    def __parse_permissions__(self) -> None:
        datalist = os.listdir(self.datadir_name)
        for aapt_out in datalist:
            with open(self.datadir_name + aapt_out,"r", newline='') as out:
                apk_permissions = []
                apk_name = []
                for data in out:
                    if "package" in data and self.phase == "classify":
                        try:
                            apk_name.append(data.rstrip().split(' ')[1])
                        except:
                            apk_name.append("")
                    if "uses-permission:" in data or "permission:" in data:
                        try:
                            permission = data.split(" ")[1].split("=")[1][1:-3].split(".")[-1]
                            apk_permissions.append(permission)
                        except:
                            permission = apk_permissions.append("")
                try:
                    if self.phase == "classify":
                        apk_permissions.append(apk_name[0])
                except:
                    pass
                file_name = "./out/"+self.type+"/static/"+self.phase+"/permissions.csv"
                with open(file_name, 'a+', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(apk_permissions)

class parse_dynamic_data:
    def __init__(self, data_type : str, phase : str) -> None:
        self.data_type = data_type
        self.parsed = []
        self.file_names = []
        self.phase = phase
        self.__parse_logs__()

    def __parse_logs__(self) -> None:
        folderName = "./data/"+self.data_type+"/dynamic/"+self.phase+"/"
        fileList = os.listdir(folderName)
        for dataFile in fileList:
            fileName = folderName + dataFile
            with open(fileName) as file:
                line = file.readlines()
                log = []
                cropCalls = line[:3000]
                for call in cropCalls:
                    parseLine = call.split("(") # get only the call name. Returns a list of the calls
                    log.append(parseLine[0])
                self.parsed.append(log)
                if self.phase == "classify":
                    self.file_names.append(dataFile)
    
    def log_file_names(self) -> list:
        return self.file_names

    def parsed_logs(self) -> list:
        return self.parsed

def parse_freq_data(data_type : str) -> list:
    parsed_values = []
    with open('syscalls-freq-'+data_type+'.csv',"r") as freq:
        for row in freq:
            calls = []
            get_values = [row.split('"')[1],row.split('"')[3]]
            sequence = get_values[0][1:-1].split(",")
            freq_range = [int(f) for f in get_values[1][1:-1].split(",")]
            calls.append(sequence[0][1:-1])
            for i in range(1, len(sequence)):
                calls.append(sequence[i][2:-1])
            parsed_values.append([calls,freq_range])
    return parsed_values