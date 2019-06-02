import ee
import ssl
import time
from pathlib import Path
import numpy as np

ee.Initialize()

def _export_one_image(img, folder, name, region, scale, crs):
    # export one image from Earth Engine to Google Drive
    # Author: Jiaxuan You, https://github.com/JiaxuanYou
    print(f'Exporting to {folder}/{name}')
    task_dict = {
        'driveFolder': folder,
        'driveFileNamePrefix': name,
        'scale': scale,
        'crs': crs
    }
    if region is not None:
        task_dict.update({
            'region': region
        })
    task = ee.batch.Export.image(img, name, task_dict)
    task.start()
    while task.status()['state'] == 'RUNNING':
        print('Running...')
        # Perhaps task.cancel() at some point.
        time.sleep(10)
    print(f'Done: {task.status()}')


def _append_mask_band(current, previous):
    # Transforms an Image Collection with 1 band per Image into a single Image with items as bands
    # Author: Jamie Vleeshouwer

    # Rename the band
    previous = ee.Image(previous)
    current = current.select([0])
    # Append it to the result (Note: only return current item on first element/iteration)
    return ee.Algorithms.If(ee.Algorithms.IsEqual(previous, None), current, previous.addBands(ee.Image(current)))


def _append_temp_band(current, previous):
    # Transforms an Image Collection with 1 band per Image into a single Image with items as bands
    # Author: Jamie Vleeshouwer

    # Rename the band
    previous = ee.Image(previous)
    current = current.select([0, 4])
    # Append it to the result (Note: only return current item on first element/iteration)
    return ee.Algorithms.If(ee.Algorithms.IsEqual(previous, None), current, previous.addBands(ee.Image(current)))


def _append_im_band(current, previous):
    # Transforms an Image Collection with 1 band per Image into a single Image with items as bands
    # Author: Jamie Vleeshouwer

    # Rename the band
    previous = ee.Image(previous)
    current = current.select([0, 1, 2, 3, 4, 5, 6])
    # Append it to the result (Note: only return current item on first element/iteration)
    return ee.Algorithms.If(ee.Algorithms.IsEqual(previous, None), current, previous.addBands(ee.Image(current)))


def export(
    folder_name, data_type, coordinate_system='EPSG:4326', scale=500,
    export_limit=None, min_img_val=None, max_img_val=None, major_states_only=True,
    check_if_done=False, download_folder=None):
    """ """
    datatype_to_func = {
        'image': _append_im_band,
        'mask': _append_mask_band,
        'temperature': _append_temp_band,
    }
    img = imgcoll.iterate(datatype_to_func[data_type])
    img = ee.Image(img)

    # "clip" the values of the bands
    if min_img_val is not None:
        # passing en ee.Number creates a constant image
        img_min = ee.Image(ee.Number(min_img_val))
        img = img.min(img_min)
    if max_img_val is not None:
        img_max = ee.Image(ee.Number(max_img_val))
        img = img.max(img_max)

    # extact the data for EACH county location
    region = ee.FeatureCollection('ft:1S4EB6319wWW2sWQDPhDvmSBIVrD3iEmCLYB7nMM')
    count = 0
    # make export fname
    for state_id, county_id in np.unique(self.locations[['State ANSI', 'County
    ANSI']].values, axis=0):
        fname = '{}_{}'.format(int(state_id), int(county_id))

    # create the local region
    file_region = region.filterMetadata('StateFips', 'equals', int(state_id))
    file_region = ee.FeatureCollection(file_region).filterMetadata('CntyFips', 'equals', int(county_id))
    file_region = ee.Feature(file_region.first())
    processed_img = img.clip(file_region)

    file_region = None
    while True:
        try:
            self._export_one_image(processed_img, folder_name, fname, file_region, scale, coordinate_system)
        except (ee.ee_exception.EEException, ssl.SSLEOFError):
            print(f'Retrying State {int(state_id)}, County {int(county_id)}')
            time.sleep(10)
            continue
