import pickle


def load_pickle_file(path):
    with open(path, "rb") as f:
        data = pickle.load(f)
    return data
