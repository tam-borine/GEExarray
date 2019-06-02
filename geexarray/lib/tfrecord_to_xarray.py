import xarray as xr
import tensorflow as tf
from pathlib import Path
from scipy import stats
import numpy as np
import pandas as pd
from typing import Dict, Tuple
import re

from tensorflow.core.example.feature_pb2 import Feature as tf_Feature

def make_dict_keys_same_length(dict_: Dict) -> Tuple[Dict, int]:
    """remove the keys that don't match the n_pixels
    Note: n_pixels estimated as the modal list
     length for values in the dict
    """
    keys = [k for k in dict_.keys()]
    # get the length of the values as most common value (N PIXELS)
    lengths = [len(dict_[key]) for key in keys]

    # N PIXELS
    n_pixel_estimate = stats.mode(np.array(lengths)).mode[0]

    # pop the keys that don't match
    popped = [
        (key, dict_.pop(key)[:5]) for key in keys
        if len(dict_[key]) != n_pixel_estimate
    ]
    print(f"{popped} keys popped!")

    return dict_, n_pixel_estimate


def find_timestep(string: str) -> str:
    # find the first string pattern matching
    ts_regex = re.compile(r"\d{4}_\d{2}_\d{2}")
    ts = ts_regex.findall(string)

    # return either empty string or the captured year
    ts = ts if ts != [] else ''

    return ts


def dict_to_ds(dict_: Dict) -> xr.Dataset:
    df = pd.DataFrame(dict_)
    ts
    try:
        df = df.set_index(['latitude','longitude', 'time'])
    except KeyError:
        df = df.set_index(['lat','lon', 'time'])

    ds = df.to_xarray()

    return ds


def get_dict_from_tf_feature(data: tf_Feature, idx: int) -> dict:
    # iterate over each key in the image (lat, lon, values)
    out = {}
    for i in range(len(keys)):
        data = result.features.feature[keys[i]]
        out[keys[i]] = np.array(data.float_list.value)

    out, n_pixels = make_dict_keys_same_length(out)
    # parsed_time = pd.to_datetime(find_timestep(string))
    times = [idx for _ in range(n_pixels)]
    out['time'] = times

    return out


def tf_feature_to_dataset(data: tf_Feature, idx: int) -> xr.Dataset:
    out = get_dict_from_tf_feature(data, idx)
    ds = dict_to_ds(out)
    return ds


def tfrecord_to_xarray(file: str) -> List[xr.Dataset]:
    """Turn `tfrecord` datatype into a dictionary of equal length
    lists (pixels).

    """
    ds_timesteps = []
    # iterate over each `example` in the dataset (observation/image)
    for i, example in enumerate(tf.python_io.tf_record_iterator(file)):
        # read as a dict-like object
        result = tf.train.Example.FromString(example)
        keys = [k for k in result.features.feature.keys()]
        data = result.features.feature

        ds = tf_feature_to_dataset(data, i)
        ds_timesteps.append(ds)

    return ds_timesteps


file = '/Users/tommylees/Downloads/EMSR122_01STRYMONAS_01DELINEATION_MONIT03_v1_75000_area_of_interest.tfrecord'

assert Path(file).exists(), f"{file} Does not exist!"

ds_timesteps = tfrecord_to_xarray(file)
out_ds = xr.merge(ds_timesteps)

out = {}
# get one image
i, example = [(i, e) for i, e in enumerate(tf.python_io.tf_record_iterator(file))][0]
# parse the image to some dictionary format
result = tf.train.Example.FromString(example)
# get the keys for that image
keys = [k for k in result.features.feature.keys()]
# get the data for that image
for i in range(len(keys)):
    data = result.features.feature[keys[i]]
    out[keys[i]] = np.array(data.float_list.value)

out = make_dict_keys_same_length(out)



latitude = out['latitude']
longitude = out['longitude']
vv = out['VV']
out.pop('constant')


check_dict_keys_same_length(out)


ds = (
    pd.DataFrame(out)
    .set_index(['latitude','longitude'])
    .to_xarray()
)

#
