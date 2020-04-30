
import sys
from sklearn.ensemble import * 
from sklearn.neighbors import * 
from sklearn.metrics import accuracy_score
import pandas as pd
import json


def check_int(x):
    if x.isdigit():
        return int(x)
    else:
        return x


def parse_model_str(model_str):
    pairs = model_str.split("::")
    model = pairs[0]
    pairs = [s.split("=") for s in pairs[1:]]
    pairs = [(p[0], check_int(p[1])) for p in pairs]

    d = {}
    d["params"] = dict(pairs)
    d["ctor"] = model

    return d


def construct_model(model_dict):

    ctor = globals()[model_dict["ctor"]]
    model = ctor(**model_dict["params"])
    
    return model


def get_data(x_file, y_file, split_idx_file):

    X_df = pd.read_csv(x_file)
    X_df.set_index("idx", inplace=True)

    y_df = pd.read_csv(y_file)
    y_df.set_index("idx", inplace=True)


    with open(split_idx_file, "r") as f:
        idx_dict = json.load(f)
    train_idx = idx_dict["train_idx"]
    test_idx = idx_dict["test_idx"]

    X_train = X_df.values[train_idx,:]
    y_train = y_df.values[train_idx,0]

    X_test = X_df.values[test_idx,:]
    y_test = y_df.values[test_idx,0]

    return X_train, y_train, X_test, y_test


if __name__=="__main__":

    x_file = sys.argv[1]
    y_file = sys.argv[2]
    split_idx_file = sys.argv[3]
    model_str = sys.argv[4]
    output_file = sys.argv[5]

    if len(sys.argv) == 7:
        best_file = sys.argv[6]
        with open(best_file, "r") as f:
            d = json.load(f)
            model_str = d["model_str"]

    model_dict = parse_model_str(model_str)
    model = construct_model(model_dict)

    X_train, y_train, X_test, y_test = get_data(x_file, y_file, 
                                                split_idx_file)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)

    results = {"model": model_dict,
               "model_str": model_str,
               "score": acc
               }
    
    with open(output_file, "w") as f:
        json.dump(results, f)

