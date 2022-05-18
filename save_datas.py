import pickle
from pathlib import Path


def write_list_to_file(file_name, hash_alerts):
    with open(file_name, 'wb') as fp:
        pickle.dump(hash_alerts, fp)


def read_list_from_file(file_name):
    hash_alerts = []
    path = Path(file_name)

    if path.is_file():
        with open(file_name, 'rb') as fp:
            hash_alerts = pickle.load(fp)
    return hash_alerts
