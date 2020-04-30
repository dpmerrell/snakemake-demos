import json 
from collections import defaultdict
import sys

if __name__=="__main__":

    score_files = sys.argv[1:-1]
    out_file = sys.argv[-1]

    summary = defaultdict(list)

    # Collect all of the scores from the files
    for sf in score_files:
        with open(sf, "r") as f:
            score_dict = json.load(f)

        summary[score_dict["model_str"]].append(score_dict["score"])

    # Compute the mean score for each model
    means = {k: sum(v)/len(v) for (k, v) in summary.items()}

    # Find the model with maximum score
    maximizer = max(means, key=lambda k: means[k])
    max_score = means[maximizer]

    # Save the result
    result = {"model_str": maximizer,
              "aggregated_score": max_score
              }
    with open(out_file, "w") as f:
        json.dump(result, f)

