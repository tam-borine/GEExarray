import os, sys, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from google.cloud import storage

from geexarray.lib.export_tfrecord_to_GCS import export_to_tfrecord

# from geexarray.lib.tfrecord_to_xarray import

class GEEXarray:

    def __init__(self, bucket_name="geexarray", gcloud_creds="/Disso-e55e8b924bcf.json", timeout=600):
        # we need gcloud_creds for authenticating to GCS, TODO tell user to specify in docs
        """ Create a new converter """
        self.bucket = bucket_name
        self.timeout = timeout
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getcwd()+gcloud_creds

    def __wait_until(somepredicate, timeout, period=5, *args, **kwargs):
        mustend = time.time() + timeout
        while time.time() < mustend:
            if somepredicate(*args, **kwargs): return True
            time.sleep(period)
        return False
        
    def __check_upload(self,name):
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket)
        self.__wait_until(storage.Blob(bucket=bucket, name=name).exists(storage_client), self.timeout)

    def to_xarray(self, collection, bounds):
        file_name_prefix = export_to_tfrecord(collection,bounds, self.bucket)
        name = file_name_prefix+"mixer.json"
        # check export is done then call tfrecord to xarray module.
        # __check_upload(name) # waits 10 mins - DANGER.

        
