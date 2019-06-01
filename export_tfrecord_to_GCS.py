


def export(image, bounds, file_name_prefix):
  task = ee.batch.Export.image.toCloudStorage(
    image=img,
    bucket='geexarray',
    fileNamePrefix=file_name_prefix,
    region=bounds.getInfo()['coordinates'],
    scale=250,
    maxPixels=1E10,
    fileFormat='TFRecord',
      formatOptions={'patchDimensions':[26,26]}
  )

  task.start()

def export_to_tfrecord(image_collection, bounds):
  file_name_prefix = ee.String(image_collection.get("system:id"))
  img = image_collection.toBands()
  export(img, bounds, file_name_prefix)
  