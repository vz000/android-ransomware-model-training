import os
import math
import pandas as pd
import csv

out_file = 'logs-ransomware.csv' # format

class dynamic_model:
    def __init__(self, data_type: str, n = 3):
        self.data_type = data_type
        self.n = n
        self.parsed_logs = []
        self.unique_ngrams = []
        self.__parse_logs__() # parse logs to get call name only
        self.__unique_ngrams__() # fetch unique ngrams
        self.ransomware_top_calls = 'ransomware-call-stats.csv'
        data_calls = 'logsRW.csv'

    def __parse_logs__(self) -> None:
        folderName = "./data/"+self.data_type+"/dynamic/"
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
                self.parsed_logs.append(log)

    def __unique_ngrams__(self) -> None:
        for logs in self.parsed_logs:
            end = len(logs) - 1
            start = 0
            while start < end:
                n_gram = logs[start:start+self.n]
                if n_gram not in self.unique_ngrams:
                    self.unique_ngrams.append(n_gram)
                start += 1

    def syscall_stats(self):
        def top_syscalls(self) -> None:
            df_calls = pd.DataFrame({'CallSeq':[],'Times':[]})
            for logs in self.parsed_logs:
                end = len(logs) - 1
                start = 0
                while start < end:
                    n_gram = logs[start:start+self.n]
                    if len(n_gram) == self.n:
                        if n_gram not in self.unique_ngrams:
                            start = start + self.n
                        else:
                            start += 1
                        df_calls = calls_count(df_calls, n_gram)
                    else:
                        break

            df_calls = df_calls.sort_values(by=['Times'],ascending=False)
            df_calls['CallSeq'].head(50).to_csv(self.ransomware_top_calls, index=False, header=False) # NSA
        
        def calls_count(df_calls, n_gram: list) -> None:
            n_gram = ','.join(n_gram)
            n_gram = n_gram.rstrip()
            call_empty = df_calls[df_calls['CallSeq']==n_gram]
            if call_empty.empty:
                df_calls = pd.concat([df_calls,pd.DataFrame({'CallSeq':[n_gram],'Times':1})], ignore_index=True)
            else:
                index = df_calls.index[df_calls['CallSeq'] == n_gram][0]
                df_calls.at[index,'Times'] = df_calls.at[index,'Times'] + 1
            return df_calls
        
        top_syscalls(self)

    def syscall_frequencies(self) -> None:
        def sequence_stats(values: list) -> tuple:
            z_ = 1.28 # 0.89973 Source: https://www.math.arizona.edu/~rsims/ma464/standardnormaltable.pdf
            n_ = len(values)
            x_ = math.floor(sum(values)/n_)
            de_ = math.floor(math.sqrt(sum([pow(x-x_,2) for x in values])/n_))
            de_n = de_/math.sqrt(n_)
            ci_l = x_ - z_ * de_n
            ci_u = x_ + z_ * de_n
            return (math.floor(ci_l),math.floor(ci_u),x_)

        call_final_freq = []
        for calls in self.parsed_logs:
            with open(self.ransomware_top_calls) as top_sequence:
                calls_row = []
                for raw_sequence in top_sequence:
                    sequence = raw_sequence[1:len(raw_sequence)-2].split(',') # Pandas adds some annoying preceding and ending "
                    start = 0
                    step = self.n
                    match = 0
                    # Calls are 3000 long, but in case it changes, keep the length of the current array.
                    while start < len(calls):
                        ngram = calls[start:start+step]
                        if sequence == ngram:
                            match += 1
                            start = start + step
                        else:
                            start += 1
                        if match > 0: # 1/3000 match doesn't make sense. To be tested.
                            calls_row.append((sequence,match))
                    if len(calls_row) > 0:
                        call_final_freq.append(calls_row)

        #print(len(call_final_freq)) # Ransomware: 431/500 were useful for the dynamic stage
        end_stats = []
        with open(self.ransomware_top_calls) as top_sequences:
            for raw_sequence in top_sequences:
                sequence = raw_sequence[1:len(raw_sequence)-2].split(',')
                sequence_values = []
                for file_freq in call_final_freq:
                    for seq in file_freq:
                        if sequence in seq:
                            sequence_values.append(seq[1])
                            break
                if len(sequence_values) > 0:
                    end_stats.append([sequence,sequence_stats(sequence_values)])
                else:
                    end_stats.append([sequence,(0,0,0)])

        with open('syscalls-freq.csv','w', newline='') as out_file:
            writer = csv.writer(out_file)
            for stat in end_stats:
                writer.writerow(stat)