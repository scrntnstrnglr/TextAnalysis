import json
emotions_count_dict_datetime = {"asdd":1,"dsdsdsd":2,"1233":2323}
with open('allhashtagsjson.json','w') as f:
    json.dump(emotions_count_dict_datetime, f)