import json
import sys
from collections import defaultdict


def get_family_name(file_path):
    spl = file_path.split("/")[-1]
    family = spl.split("_")[0]
    return family


if __name__=="__main__":

    in_files = sys.argv[1:-1]
    out_file = sys.argv[-1]

    results = defaultdict(list)
    
    for in_file in in_files:

        with open(in_file, "r") as f: 
            score_dict = json.load(f)
        family = get_family_name(in_file)

        results[family].append(score_dict["score"])

    with open(out_file, "w") as f:
        json.dump(results, f)


