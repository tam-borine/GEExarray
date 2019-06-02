import os, sys, time

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)

from google.cloud import storage

from GEExarray.lib.export_tfrecord_to_GCS import export_to_tfrecord

# from geexarray.lib.tfrecord_to_xarray import

class GEEXarray:

    def __init__(self, bucket_name="geexarray", timeout=600):
        # we need gcloud_creds for authenticating to GCS, TODO tell user to specify in docs
        """ Create a new converter """
        self.bucket = bucket_name

    def to_xarray(self, collection, bounds):
        export_to_tfrecord(collection, bounds, self.bucket)
