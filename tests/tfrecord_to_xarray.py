import xarray as xr
import tensorflow as tf
from pathlib import Path

def get_values(file):
  data = []
  for example in tf.python_io.tf_record_iterator(file, options=options):
    result = tf.train.Example.FromString(example)
    is_flooded_example = get_value_from_Example(result, 'constant') == 1.0
    data.append([get_value_from_Example(result, f) for f in features])
  return data

file = '/Users/tommylees/Downloads/EMSR122_01STRYMONAS_01DELINEATION_MONIT03_v1_75000_area_of_interest.tfrecord'
options = tf.python_io.TFRecordOptions(tf.python_io.TFRecordCompressionType.GZIP)


Path(file).exists()

for example in tf.python_io.tf_record_iterator(file):
    result = tf.train.Example.FromString(example)
    value = get_value_from_Example(result, 'constant')
    print(value)

for example in tf.python_io.tf_record_iterator(file):
    result = tf.train.Example.FromString(example)
