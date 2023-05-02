def dynamic_classify(parsed_logs: list, freq_list: list, name_list: list) -> list:
    i_names_list = 0
    app_match = []
    good_sequences_name = [s[0] for s in freq_list[1]]
    good_freq = [s[1] for s in freq_list[1]]
    rw_sequences_name = [r[0] for r in freq_list[0]]
    rw_freq = [r[1] for r in freq_list[0]]
    for calls in parsed_logs:
        sequences_match = 0
        s_num = 0
        for top_sequences in rw_sequences_name:
            start = 0
            match = 0
            good_match = 0
            rw_range = list(range(rw_freq[s_num][0],rw_freq[s_num][1]+1))
            while start < len(calls):
                ngram = calls[start:start+6]
                if top_sequences == ngram:
                    match += 1
                elif ngram == good_sequences_name[s_num]:
                    good_match += 1
                start += 1

            if good_match < 1:
                if (top_sequences not in good_sequences_name):
                    if match in rw_range:
                        sequences_match += 1
                else:
                    range_index = good_sequences_name.index(top_sequences)
                    gw_range = list(range(good_freq[range_index][0],good_freq[range_index][1]+1))
                    if (match in rw_range) and (match not in gw_range):
                        sequences_match += 1
            
            if good_match > 30 and good_match < 110:
                sequences_match -= 1
            s_num += 1

        if sequences_match > 0:
            result = 1
        else:
            result = 0
        app_match.append({
                'name':name_list[i_names_list],
                'static':0,
                'dynamic':result})
        i_names_list += 1
    
    return app_match