import scanpy
import h5py
import numpy as np
import scipy
import os
import json
import pandas as pd
import uuid
import time
import shutil
import zipfile
from pandas.api.types import is_numeric_dtype

def copy_dataset(source, dest, name, chunk_size=16*1024):
    dataset = dest.create_dataset(name, shape=source[name].shape, dtype=source[name].dtype)
    i = 0
    while i + chunk_size <= source[name].shape[0]:
        dataset[i:i+chunk_size] = source[name][i:i+chunk_size]
        i += chunk_size

    if i < source[name].shape[0]:
        dataset[i:] = source[name][i:]


def generate_uuid(remove_hyphen=True):
    res = str(uuid.uuid4())
    if remove_hyphen == True:
        res = res.replace("-", "")
    return res

def get_barcodes(scanpy_obj):
    return scanpy_obj.obs_names

def get_features(scanpy_obj):
    return scanpy_obj.var_names

def get_raw_features(scanpy_obj):
    return scanpy_obj.raw.var.index

def get_raw_from_rawX(scanpy_obj):
    M = scanpy_obj.raw.X[:][:].tocsr()
    barcodes = get_barcodes(scanpy_obj)
    features = get_raw_features(scanpy_obj)
    return M, barcodes, features

def get_raw_from_layers(scanpy_obj, raw_key):
    M = scanpy_obj.layers[raw_key].tocsr()
    barcodes = get_barcodes(scanpy_obj)
    features = get_features(scanpy_obj)
    return M, barcodes, features

def get_raw_data(scanpy_obj, raw_key):
    if raw_key == "auto":
        try:
            res = get_raw_from_rawX(scanpy_obj)
        except Exception as e:
            print("--->Error when reading \"raw.X\": ", e)
            print("--->Trying possible keys")
            candidate_keys = ["counts", "raw"]
            for key in candidate_keys:
                try:
                    res = get_raw_from_layers(scanpy_obj, key)
                except:
                    continue
                print("--->Found raw data in /layers/%s" % key)
                return res
            raise Exception("Raw data not found")
    elif raw_key == "raw.X":
        res = get_raw_from_rawX(scanpy_obj)
    else:
        res = get_raw_from_layers(scanpy_obj, raw_key)
    return res

def get_normalized_data(scanpy_obj, raw_data, raw_barcodes, raw_features):
    M = scanpy_obj.X[:][:].tocsc()
    norm_barcodes = scanpy_obj.obs.index
    norm_features = scanpy_obj.var.index
    if (raw_data is None) or (M.shape == raw_data.shape):
        return M, norm_barcodes, norm_features
    else:
        return raw_data.tocsc(), raw_barcodes, raw_features

def encode_strings(strings, encode_format="utf8"):
    return [x.encode(encode_format) for x in strings]

def write_matrix(scanpy_obj, dest_hdf5, raw_key):
    try:
        raw_M, barcodes, features = get_raw_data(scanpy_obj, raw_key)
    except Exception as e:
        print("--->Cannot read raw data: %s" % str(e))
        raw_M = barcodes = features = None

    norm_M, barcodes, features = get_normalized_data(scanpy_obj, raw_M,
                                                        barcodes,
                                                        features)

    if raw_M is None:
        has_raw = False
        print("--->Using normalized data as raw data")
        raw_M = norm_M.tocsr()
    else:
        has_raw = True

    print("--->Writing group \"bioturing\"")
    bioturing_group = dest_hdf5.create_group("bioturing")
    bioturing_group.create_dataset("barcodes",
                                    data=encode_strings(barcodes))
    bioturing_group.create_dataset("features",
                                    data=encode_strings(features))
    bioturing_group.create_dataset("data", data=raw_M.data)
    bioturing_group.create_dataset("indices", data=raw_M.indices)
    bioturing_group.create_dataset("indptr", data=raw_M.indptr)
    bioturing_group.create_dataset("feature_type", data=["RNA".encode("utf8")] * len(features))
    bioturing_group.create_dataset("shape", data=[len(features), len(barcodes)])

    if has_raw:
        print("--->Writing group \"countsT\"")
        raw_M_T = raw_M.tocsc()
        countsT_group = dest_hdf5.create_group("countsT")
        countsT_group.create_dataset("barcodes",
                                        data=encode_strings(features))
        countsT_group.create_dataset("features",
                                        data=encode_strings(barcodes))
        countsT_group.create_dataset("data", data=raw_M_T.data)
        countsT_group.create_dataset("indices", data=raw_M_T.indices)
        countsT_group.create_dataset("indptr", data=raw_M_T.indptr)
        countsT_group.create_dataset("shape", data=[len(barcodes), len(features)])
    else:
        print("--->Raw data is not available, ignoring \"countsT\"")

    print("--->Writing group \"normalizedT\"")
    normalizedT_group = dest_hdf5.create_group("normalizedT")
    normalizedT_group.create_dataset("barcodes",
                                    data=encode_strings(features))
    normalizedT_group.create_dataset("features",
                                    data=encode_strings(barcodes))
    normalizedT_group.create_dataset("data", data=norm_M.data)
    normalizedT_group.create_dataset("indices", data=norm_M.indices)
    normalizedT_group.create_dataset("indptr", data=norm_M.indptr)
    normalizedT_group.create_dataset("shape", data=[len(barcodes), len(features)])

    print("--->Writing group \"colsum\"")
    norm_M = norm_M.tocsr()
    n_cells = len(barcodes)
    sum_lognorm = np.array([0.0] * n_cells)
    if has_raw:
        sum_log = np.array([0.0] * n_cells)
        sum_raw = np.array([0.0] * n_cells)

    for i in range(n_cells):
        l, r = raw_M.indptr[i:i+2]
        sum_lognorm[i] = np.sum(norm_M.data[l:r])
        if has_raw:
            sum_raw[i] = np.sum(raw_M.data[l:r])
            sum_log[i] = np.sum(np.log2(raw_M.data[l:r] + 1))

    colsum_group = dest_hdf5.create_group("colsum")
    colsum_group.create_dataset("lognorm", data=sum_lognorm)
    if has_raw:
        colsum_group.create_dataset("log", data=sum_log)
        colsum_group.create_dataset("raw", data=sum_raw)
    return barcodes, features, has_raw

def generate_history_object():
    return {
        "created_by":"bbrowser_format_converter",
        "created_at":time.time() * 1000,
        "hash_id":generate_uuid(),
        "description":"Created by converting scanpy object to bbrowser format"
    }

def is_all_numeric(a):
    try:
        a = [float(x) for x in a]
    except:
        return False
    return True

def convert_to_int(a):
    try:
        return [int(x) for x in a]
    except:
        return None

def convert_to_float(a):
    try:
        return [float(x) for x in a]
    except:
        return None

def add_category_to_first(column, new_category):
    if column.dtype.name != "category":
        raise Exception("Object is not a pandas.Categorical")

    if new_category in column.cat.categories:
        raise Exception("%s is already in categories list" % new_category)

    column = column.copy()
    column = column.cat.add_categories(new_category)
    cat = column.cat.categories.tolist()
    cat = cat[0:-1]
    cat.insert(0, new_category)
    column = column.cat.reorder_categories(cat)
    return column

def write_metadata(scanpy_obj, dest, zobj, replace_missing="Unassigned"):
    print("Writing main/metadata/metalist.json")
    metadata = scanpy_obj.obs.copy()
    for metaname in metadata.columns:
        try:
            metadata[metaname] = pd.to_numeric(metadata[metaname], downcast="float")
        except:
            print("--->Cannot convert %s to numeric, treating as categorical" % metaname)

    content = {}
    all_clusters = {}
    numeric_meta = metadata.select_dtypes(include=["number"]).columns
    category_meta = metadata.select_dtypes(include=["category"]).columns
    for metaname in metadata.columns:
        uid = generate_uuid()

        if metaname in numeric_meta:
            all_clusters[uid] = list(metadata[metaname])
            lengths = 0
            names = "NaN"
            _type = "numeric"
        elif metaname in category_meta:
            if replace_missing not in metadata[metaname].cat.categories:
                metadata[metaname] = add_category_to_first(metadata[metaname],
                                                            new_category=replace_missing)
            metadata[metaname].fillna(replace_missing, inplace=True)

            value_to_index = {}
            for x, y in enumerate(metadata[metaname].cat.categories):
                value_to_index[y] = x
            all_clusters[uid] = [value_to_index[x] for x in metadata[metaname]]
            index, counts = np.unique(all_clusters[uid], return_counts = True)
            lengths = np.array([0] * len(metadata[metaname].cat.categories))
            lengths[index] = counts
            lengths = [x.item() for x in lengths]
            _type = "category"
            names = list(metadata[metaname].cat.categories)
        else:
            print("--->\"%s\" is not numeric or categorical, ignoring" % metaname)
            continue


        content[uid] = {
            "id":uid,
            "name":metaname if metaname != "seurat_clusters" else "Graph-based clusters",
            "clusterLength":lengths,
            "clusterName":names,
            "type":_type,
            "history":[generate_history_object()]
        }

    graph_based_history = generate_history_object()
    graph_based_history["hash_id"] = "graph_based"
    n_cells = scanpy_obj.n_obs
    content["graph_based"] = {
        "id":"graph_based",
        "name":"Graph-based clusters",
        "clusterLength":[0, n_cells],
        "clusterName":["Unassigned", "Cluster 1"],
        "type":"category",
        "history":[graph_based_history]
    }
    with zobj.open(dest + "/main/metadata/metalist.json", "w") as z:
        z.write(json.dumps({"content":content, "version":1}).encode("utf8"))


    for uid in content:
        print("Writing main/metadata/%s.json" % uid, flush=True)
        if uid == "graph_based":
            clusters = [1] * n_cells
        else:
            clusters = all_clusters[uid]
        obj = {
            "id":content[uid]["id"],
            "name":content[uid]["name"],
            "clusters":clusters,
            "clusterName":content[uid]["clusterName"],
            "clusterLength":content[uid]["clusterLength"],
            "history":content[uid]["history"],
            "type":[content[uid]["type"]]
        }
        with zobj.open(dest + ("/main/metadata/%s.json" % uid), "w") as z:
            z.write(json.dumps(obj).encode("utf8"))

def write_main_folder(scanpy_obj, dest, zobj, raw_data):
    print("Writing main/matrix.hdf5", flush=True)
    tmp_matrix = "." + str(uuid.uuid4())
    with h5py.File(tmp_matrix, "w") as dest_hdf5:
        barcodes, features, has_raw = write_matrix(scanpy_obj, dest_hdf5,
                                                    raw_data)
    print("--->Writing to zip", flush=True)
    zobj.write(tmp_matrix, dest + "/main/matrix.hdf5")
    os.remove(tmp_matrix)

    print("Writing main/barcodes.tsv", flush=True)
    with zobj.open(dest + "/main/barcodes.tsv", "w") as z:
        z.write("\n".join(barcodes).encode("utf8"))

    print("Writing main/genes.tsv", flush=True)
    with zobj.open(dest + "/main/genes.tsv", "w") as z:
        z.write("\n".join(features).encode("utf8"))

    print("Writing main/gene_gallery.json", flush=True)
    obj = {"gene":{"nameArr":[],"geneIDArr":[],"hashID":[],"featureType":"gene"},"version":1,"protein":{"nameArr":[],"geneIDArr":[],"hashID":[],"featureType":"protein"}}
    with zobj.open(dest + "/main/gene_gallery.json", "w") as z:
        z.write(json.dumps(obj).encode("utf8"))
    return has_raw

def write_dimred(scanpy_obj, dest, zobj):
    print("Writing dimred")
    data = {}
    default_dimred = None
    for dimred in scanpy_obj.obsm:
        if isinstance(scanpy_obj.obsm[dimred], np.ndarray) == False:
            print("--->%s is not a numpy.ndarray, ignoring" % dimred)
            continue
        print("--->Writing %s" % dimred)
        matrix = scanpy_obj.obsm[dimred]
        if matrix.shape[1] > 3:
            print("--->%s has more than 3 dimensions, using only the first 3 of them" % dimred)
            matrix = matrix[:, 0:3]
        n_shapes = matrix.shape

        matrix = [list(map(float, x)) for x in matrix]
        dimred_history = generate_history_object()
        coords = {
            "coords":matrix,
            "name":dimred,
            "id":dimred_history["hash_id"],
            "size":list(n_shapes),
            "param":{"omics":"RNA", "dims":len(n_shapes)},
            "history":[dimred_history]
        }
        if default_dimred is None:
            default_dimred = coords["id"]
        data[coords["id"]] = {
            "name":coords["name"],
            "id":coords["id"],
            "size":coords["size"],
            "param":coords["param"],
            "history":coords["history"]
        }
        with zobj.open(dest + "/main/dimred/" + coords["id"], "w") as z:
            z.write(json.dumps(coords).encode("utf8"))
    meta = {
        "data":data,
        "version":1,
        "bbrowser_version":"2.7.38",
        "default":default_dimred,
        "description":"Created by converting scanpy to bbrowser format"
    }
    print("Writing main/dimred/meta", flush=True)
    with zobj.open(dest + "/main/dimred/meta", "w") as z:
        z.write(json.dumps(meta).encode("utf8"))


def write_runinfo(scanpy_obj, dest, study_id, zobj, unit="umi"):
    print("Writing run_info.json", flush=True)
    runinfo_history = generate_history_object()
    runinfo_history["hash_id"] = study_id
    date = time.time() * 1000
    run_info = {
        "species":"human",
        "hash_id":study_id,
        "version":16,
        "n_cell":scanpy_obj.n_obs,
        "modified_date":date,
        "created_date":date,
        "addon":"SingleCell",
        "matrix_type":"single",
        "n_batch":1,
        "platform":"unknown",
        "omics":["RNA"],
        "title":["Created by bbrowser converter"],
        "history":[runinfo_history],
        "unit":unit
    }
    with zobj.open(dest + "/run_info.json", "w") as z:
        z.write(json.dumps(run_info).encode("utf8"))

def format_data(source, output_name, raw_data="auto"):
    scanpy_obj = scanpy.read_h5ad(source, "r")
    zobj = zipfile.ZipFile(output_name, "w")
    study_id = generate_uuid(remove_hyphen=False)
    dest = study_id
    with h5py.File(source, "r") as s:
        has_raw = write_main_folder(scanpy_obj, dest, zobj, raw_data)
        write_metadata(scanpy_obj, dest, zobj)
        write_dimred(scanpy_obj, dest, zobj)
        unit = "umi" if has_raw else "lognorm"
        write_runinfo(scanpy_obj, dest, study_id, zobj, unit)

    return output_name

