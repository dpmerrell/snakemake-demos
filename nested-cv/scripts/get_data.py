from sklearn.datasets import load_digits
import pandas as pd
import sys

if __name__=="__main__":

    X_outfile = sys.argv[1]
    y_outfile = sys.argv[2]

    dataset = load_digits()
    
    X = dataset["data"]
    y = dataset["target"]
    
    print(X.shape)
    print(y.shape)

    X_df = pd.DataFrame(data=X)
    X_df.index.rename("idx", inplace=True)

    y_df = pd.DataFrame(data=y)
    y_df.index.rename("idx", inplace=True)

    X_df.to_csv(X_outfile, sep=",")
    y_df.to_csv(y_outfile, sep=",")
