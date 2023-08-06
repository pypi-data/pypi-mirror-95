import setuptools, os, glob
from dbbs_mod_collection import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

def list_mod_files():
    here = os.path.dirname(__file__)
    path = os.path.join(here, "dbbs_mod_collection", "mod", "*")
    mods = glob.glob(path)
    return [os.path.relpath(m, here) for m in mods]

setuptools.setup(
     name='dbbs_mod_collection',
     version=__version__,
     author="Robin De Schepper",
     author_email="robingilbert.deschepper@unipv.it",
     description="Glia package of NEURON models",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/dbbs-lab/glia",
     license='GPLv3',
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
     include_package_data=True,
     data_files=[
         ('mod', list_mod_files())
     ],
     entry_points={
      'glia.package': ['dbbs_mod_collection = dbbs_mod_collection']
     },
     install_requires=[
      "nrn-glia>=0.1.1"
     ]
 )
