import sys
from dynamic.classify.dynamic_classify import dynamic_classify
from static.classify.static_classify import static_classify
from static.train.static_detectors import *
from static.train.static_ngram import *
from static.train.static_stats import *
from dynamic.train.dynamic_frequencies import *
from parse import *
from results import get_results

sample_types = ["ransomware","goodware"]
methods = ["static","dynamic"]
phases = ["train","classify"]

n = 3

results = []
if sys.argv[1] in methods and sys.argv[2] in phases:
    if sys.argv[1] == "static": 
        for sample_type in sample_types:
                datadir = './out/'+sample_type+'/'+sys.argv[1]+'/'+sys.argv[2]+'/'
                parsed_static = parse_static_data(datadir,sample_type,sys.argv[2])

        if sys.argv[2] == "train":
            folder = "./out/ransomware/static/"
            stats = permissions_stats("ransomware")
            out_stats_file = stats.get_output_file()
            perm_ngram = permissions_ngram(folder+"train/permissions.csv",out_stats_file,n)
            ngram = perm_ngram.get_draft_detectors()
            permission_list = perm_ngram.get_permission_list()
            detectors = static_detectors(n, ngram, permission_list, 5)
            detectors.fit()

        elif sys.argv[2] == "classify":
            for sample_type in sample_types:
                classify = static_classify('./out/'+sample_type+'/static/classify/permissions.csv',n)
                results.append(classify.classify())
            print(get_results(results))

    elif sys.argv[1] == "dynamic":
        if sys.argv[2] == "train":
            parsed_out = parse_dynamic_data("ransomware",sys.argv[2])
            dynamic_frequencies("ransomware",parsed_out.parsed_logs())
            parsed_out = parse_dynamic_data("goodware",sys.argv[2])
            dynamic_frequencies("goodware",parsed_out.parsed_logs())
            
        elif sys.argv[2] == "classify":
            results = []
            list_num = 0
            get_freq_list = [parse_freq_data("ransomware"),parse_freq_data("goodware")]
            for sample_type in sample_types:
                parsed_out = parse_dynamic_data(sample_type,sys.argv[2])
                get_names_list = parsed_out.log_file_names()
                results.append(dynamic_classify(parsed_out.parsed_logs(), get_freq_list, get_names_list))
            print(get_results(results))
                
else:
    print("Error.")
