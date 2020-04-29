import pandas as pd
from sklearn.model_selection import StratifiedKFold
import numpy as np
import json
import sys


if __name__=="__main__":

    # Get inputs
    y_filename = sys.argv[1]
    outer_splits = int(sys.argv[2])
    inner_splits = int(sys.argv[3])
    split_dir = sys.argv[4]

    # load y-values for generating stratified splits
    y_df = pd.read_csv(y_filename)


    # Make the outer splits!
    outer_skf = StratifiedKFold(n_splits=outer_splits, shuffle=True)
    for i, (train_idx, test_idx) in enumerate(outer_skf.split(np.zeros(y_df.shape[0]), 
                                                              y_df["0"].values)):

        # Store the outer split's train/test indices 
        outer_dict = {"train_idx": y_df["idx"].values[train_idx].tolist(),
                      "test_idx": y_df["idx"].values[test_idx].tolist()
                      }
        with open("{}/{}.json".format(split_dir, i), "w") as f:
            json.dump(outer_dict, f)


        # Make the inner splits!
        inner_y = y_df.loc[train_idx,:]
        inner_skf = StratifiedKFold(n_splits=inner_splits, shuffle=True)
        for j, (inner_train_idx, inner_test_idx) in enumerate(inner_skf.split(np.zeros(inner_y.shape[0]),
                                                                              inner_y["0"].values)):

            # Store the inner split's train/test indices
            inner_dict = {"train_idx": inner_y["idx"].values[inner_train_idx].tolist(),
                          "test_idx": inner_y["idx"].values[inner_test_idx].tolist()
                         }
            with open("{}/{}/{}.json".format(split_dir, i, j), "w") as f:
                json.dump(inner_dict, f)

