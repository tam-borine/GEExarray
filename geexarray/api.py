import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from google.cloud import storage

from geexarray.lib.export_tfrecord_to_GCS import export_to_tfrecord

# from geexarray.lib.tfrecord_to_xarray import

class GEEXarray:

    def __init__(self, bucket_name="geexarray", gcloud_creds="/Disso-e55e8b924bcf.json"):
        """ Create a new converter """
        self.bucket = bucket_name
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getcwd()+gcloud_creds

    def __check_upload(self,name):
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket)
        stats = storage.Blob(bucket=bucket, name=name).exists(storage_client)
        return stats

    def to_xarray(self, collection, bounds):
        file_name_prefix = export_to_tfrecord(collection,bounds, self.bucket)
        name = file_name_prefix+"mixer.json"
        # check export is done then call tfrecord to xarray module.
        stats = self.__check_upload(name)
        print(stats, "stats! ")

        
