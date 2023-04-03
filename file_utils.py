""" Functions to read and write data. """
import json
import pandas as pd


def read_file(file_path, mode='r', filetype='generic'):
    """ Open and read a file. """
    with open(file_path, mode) as file_obj:
        if filetype == 'generic':
            return file_obj.read()
        if filetype == 'json':
            return json.load(file_obj)


def store_file(filepath, content, mode='w'):
    """  """
    with open(filepath, mode) as file:
        file.write(content)


def insert_dicts_to_csv(dict_list, csv_path):
    """ Insert a list of Python dictionaries to a csv using the Pandas module. """
    df = pd.DataFrame.from_dict(dict_list)
    df.to_csv(csv_path)


def insert_dict_to_json(dict_list, json_path):
    """ Insert a list of python dictionaries into a json file. """
    with open(json_path, 'w') as json_file_obj:
        json.dump(dict_list, json_file_obj)
