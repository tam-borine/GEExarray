from geexarray.lib.export_tfrecord_to_GCS import export_to_tfrecord
from geexarray.lib.tfrecord_to_xarray import 

def to_xarray(collection,bounds):
    export_to_tfrecord(collection,bounds)
    #when it is done.
    