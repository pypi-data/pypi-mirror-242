import io
import os
import re

from setuptools import find_packages
from setuptools import setup
import versioneer

exec(open('nectar_msi/_version.py').read())

def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


setup(
    version=__version__,
    name="nectar_msi",
    url="https://gitlab.npl.co.uk/nice-msi/nectar",
    license="GNU Lesser General Public License v3.0",
    author="Ariadna Gonzalez-Fernandez",
    author_email="ariadna.gonzalez@npl.co.uk",
    description="NECTAR_MSI (NoisE CorrecTion AlgoRithm) a python package for noise determination and correction in MSI.",
    long_description=read("README.md"),
    packages=find_packages(exclude=("tests",)),
    install_requires=['numpy', 'matplotlib', 'pyimzml', 'h5py', 'scipy', 'pandas', 'scikit-learn', 'tqdm'],
    extras_require={"dev": ["pre-commit", "tox", "sphinx", "sphinx_rtd_theme", 'jupyter']},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
