import os
import gzip
import json
import codecs
import pickle
import numpy as np
from scipy import sparse
import random


def makedirs(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_to_json(data, output_filename, indent=2, sort_keys=True):
    with codecs.open(output_filename, 'w') as output_file:
        json.dump(data, output_file, indent=indent, sort_keys=sort_keys)


def read_json(input_filename):
    with codecs.open(input_filename) as input_file:
        data = json.load(input_file)
    return data


def read_jsonlist(input_filename):
    data = []
    if input_filename[-3:] == '.gz':
        with gzip.open(input_filename, 'rt') as input_file:
            for l_i, line in enumerate(input_file):
                data.append(json.loads(line))
    else:
        with codecs.open(input_filename) as input_file:
            for line in input_file:
                data.append(json.loads(line))
    return data

def read_jsonlist_random_sample(input_filename, percent, totalfiles):
    data = []
    if input_filename[-3:] == '.gz':
        with gzip.open(input_filename, 'rt') as input_file:
            for l_i, line in enumerate(input_file):
                data.append(json.loads(line))
    else:
        with codecs.open(input_filename) as input_file:
            nsamples = percent * totalfiles
            random.shuffle(input_file)
            # create list of random indecies of length percent * total 
            for i, line in enumerate(input_file):
                if i < nsamples:
                    data.append(json.loads(line))
                else:
                    break
    return data
    

def write_to_jsonlist(list_of_objects, output_filename, sort_keys=True, do_gzip=False):
    if do_gzip:
        with gzip.open(output_filename, 'wt') as output_file:
            for obj in list_of_objects:
                output_file.write(json.dumps(obj, sort_keys=sort_keys) + '\n')
    else:
        with codecs.open(output_filename, 'w') as output_file:
            for obj in list_of_objects:
                output_file.write(json.dumps(obj, sort_keys=sort_keys) + '\n')


def pickle_data(data, output_filename):
    with open(output_filename, 'wb') as outfile:
        pickle.dump(data, outfile, pickle.HIGHEST_PROTOCOL)


def unpickle_data(input_filename):
    with open(input_filename, 'rb') as infile:
        data = pickle.load(infile)
    return data


def read_text_to_list(input_filename, encoding='utf-8'):
    with codecs.open(input_filename, 'r', encoding=encoding) as input_file:
        lines = input_file.readlines()
    return lines


def write_list_to_text(lines, output_filename, add_newlines=True, add_final_newline=False):
    if add_newlines:
        lines = '\n'.join(lines)
        if add_final_newline:
            lines += '\n'
    else:
        lines = ''.join(lines)
        if add_final_newline:
            lines[-1] += '\n'

    with codecs.open(output_filename, 'w', encoding='utf-8') as output_file:
        output_file.writelines(lines)


def save_sparse(sparse_matrix, output_filename):
    assert sparse.issparse(sparse_matrix)
    if sparse.isspmatrix_coo(sparse_matrix):
        coo = sparse_matrix
    else:
        coo = sparse_matrix.tocoo()
    row = coo.row
    col = coo.col
    data = coo.data
    shape = coo.shape
    np.savez(output_filename, row=row, col=col, data=data, shape=shape)


def load_sparse(input_filename):
    npy = np.load(input_filename)
    coo_matrix = sparse.coo_matrix((npy['data'], (npy['row'], npy['col'])), shape=npy['shape'])
    return coo_matrix.tocsc()

def write_documentation(documentation, filename):
    f = open(filename,"w")
    f.write(documentation)
    f.close()
