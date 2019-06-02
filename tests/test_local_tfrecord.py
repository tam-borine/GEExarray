import tensorflow as tf
import pandas as pd

from GEExarray.lib.tfrecord_to_xarray import find_timestep


file = '/Users/tommylees/Downloads/EMSR122_01STRYMONAS_01DELINEATION_MONIT03_v1_75000_area_of_interest.tfrecord'

file = '/Users/tommylees/Downloads/MODIS_006_MOD09A100001.tfrecord'

assert Path(file).exists(), f"{file} Does not exist!"

# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
ds_timesteps = tfrecord_to_xarray(file)
out_ds = xr.merge(ds_timesteps)


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
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
    list_of_values = np.array(data.float_list.value)
    if list_of_values.size == 0:
        list_of_values = np.array(data.int64_list.value)

    out[keys[i]] = list_of_values

times = [pd.to_datetime(find_timestep(key)[0], format='%Y_%M_%d') for key in keys]
times = np.unique(times)



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
