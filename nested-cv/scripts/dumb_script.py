
import yaml
import itertools as it

config = yaml.load(open("config.yaml", "r"))

MODEL_FAMILIES = config["model_families"]

def get_model_strs(family):

    member_items = MODEL_FAMILIES[family].items()
    member_names = [n for (n,v) in member_items]
    member_values = [v for (n,v) in member_items]
    print(member_items)
    result = []

    for i, model in enumerate(member_values):
        model_items = model.items()
        param_names = [n for (n,p) in model_items]
        param_vecs = [p for (n,p) in model_items]
        print(param_names)
        print(param_vecs)

        for grid_point in it.product(*param_vecs):
            pairs = zip(param_names, grid_point)
            pairs = ["{}={}".format(p[0], p[1]) for p in pairs]
            result.append(member_names[i] + "::" + "::".join(pairs))
    return result

print(get_model_strs("trees"))
