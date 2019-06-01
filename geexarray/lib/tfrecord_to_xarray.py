import xarray as xr
import tensorflow as tf
from pathlib import Path

def get_value_from_Example(example, feature_name):
    return float(
        example.features.feature[feature_name].float_list.value[0]
    )


def get_values(file):
  data = []
  for example in tf.python_io.tf_record_iterator(file, options=options):
    result = tf.train.Example.FromString(example)
    is_flooded_example = get_value_from_Example(result, 'constant') == 1.0
    data.append([get_value_from_Example(result, f) for f in features])
  return data







file = '/Users/tommylees/Downloads/EMSR122_01STRYMONAS_01DELINEATION_MONIT03_v1_75000_area_of_interest.tfrecord'
options = tf.python_io.TFRecordOptions(tf.python_io.TFRecordCompressionType.GZIP)

assert Path(file).exists(), f"{file} Does not exist!"

for example in tf.python_io.tf_record_iterator(file, options=options):
    result = tf.train.Example.FromString(example)
    data = result.features.feature
    print(type(data))
    break


out = {}
# get one image
example = [e for e in tf.python_io.tf_record_iterator(file)][0]
# parse the image to some dictionary format
result = tf.train.Example.FromString(example)
# get tje keys for that image
keys = [k for k in result.features.feature.keys()]
# get the data for that image
for i in range(len(keys)):
    data = result.features.feature[keys[i]]
    out[keys[i]] = np.array(data.float_list.value)

latitude = out['latitude']
longitude = out['longitude']
vv = out['VV']
out.pop('constant')


from scipy import stats

def make_dict_keys_same_length(dict_):
    """remove the keys that don't match the n_pixels (messes up our later function)"""
    keys = [k for k in dict_.keys()]
    # get the length of the values as most common value (N PIXELS)
    lengths = [len(dict_[key]) for key in keys]

    # N PIXELS
    n_pixel_estimate = stats.mode(np.array(lengths)).mode[0]

    # pop the keys that don't match
    [
        dict_.pop(key) for key in keys
        if len(dict_[key]) != n_pixel_estimate
    ]

    return dict_


check_dict_keys_same_length(out)


ds = (
    pd.DataFrame(out)
    .set_index(['latitude','longitude'])
    .to_xarray()
)

#
