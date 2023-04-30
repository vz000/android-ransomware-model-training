def get_results_list(obj_tags: list) -> list:
    results = []
    for result in obj_tags:
        if result['static'] == 1 or result['dynamic'] == 1:
            results.append(1)
        else:
            results.append(0)
    return results

def get_results(results: list) -> dict:
    RW = results[0]
    GW = results[1]
    rw_results = get_results_list(RW)
    gw_results = get_results_list(GW)

    TP = rw_results.count(1)
    FN = gw_results.count(1)
    FP = rw_results.count(0)
    TN = gw_results.count(0)
    precision = (TP/(TP+FP))*100
    recall = (TP/(TP+FN))*100
    accuracy = ((TP+TN)/(TP+FP+FN+TN))*100
    return dict(precision = precision, recall = recall, accuracy = accuracy)
