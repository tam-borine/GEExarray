import ee

def get_scale(name):
  common_scales = {
    'MODIS': 250,
    'LANDSAT': 30,
    'S1_GRD': 10
  }
  for k in common_scales.keys():
    if k in name:
      return common_scales[k]
  assert "not a recognised image type"


def _wait(task):
  while task.status()['state'] == 'RUNNING':
    print('Running...')
    # Perhaps task.cancel() at some point.
    time.sleep(60)


def export(image, bounds, bucket_name, file_name_prefix, max_pixels=1E10, dims=[26,26]):
  task = ee.batch.Export.image.toCloudStorage(
    image=image,
    bucket=bucket_name,
    fileNamePrefix=file_name_prefix,
    region=bounds.getInfo()['coordinates'],
    scale=get_scale(file_name_prefix),
    maxPixels=max_pixels,
    fileFormat='TFRecord',
      formatOptions={'patchDimensions': dims}
  )

  task.start()
  return task

def export_to_tfrecord(image_collection, bounds, bucket_name):
  file_name_prefix = ee.String(image_collection.get("system:id")).getInfo()
  # convert the ImageCollection (dims,bands,times) to bands
  img = image_collection.toBands()
  task = export(img, bounds, bucket_name, file_name_prefix)
  _wait(task)