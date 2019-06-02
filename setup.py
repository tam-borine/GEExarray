from setuptools import setup

setup(name='geexarray',
      version='0.1',
      description='Convert earth engine collection objects to xarrays',
      url='https://github.com/tam-borine/GEExarray',
      author='Tam Borine and Tommy Lees and Dan Stan',
      author_email='',
      license='MIT',
      packages=['geexarray'],
      install_requires=[
          'earthengine-api',
          'xarray',
          'numpy',
          'pandas',
          'tensorflow',
          'scipy',
        ],
      zip_safe=False)
