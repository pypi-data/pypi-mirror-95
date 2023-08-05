import re
from itertools import chain
from os import path

from setuptools import find_packages, setup

name = "pyslab"
here = path.abspath(path.dirname(__file__))

# get package version
with open(path.join(here, name, "__init__.py"), encoding="utf-8") as f:
    result = re.search(r'__version__ = ["\']([^"\']+)', f.read())
    if not result:
        raise ValueError("Can't find the version in pyslab/__init__.py")
    version = result.group(1)

# get the dependencies and installs
with open("requirements.txt", "r", encoding="utf-8") as f:
    requires = [x.strip() for x in f if x.strip()]

# get test dependencies and installs
with open("test_requirements.txt", "r", encoding="utf-8") as f:
    test_requires = [x.strip() for x in f if x.strip() and not x.startswith("-r")]

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()

extras_require = {}

setup(
    name=name,
    version=version,
    license="Apache Software License (Apache 2.0)",
    description="Play Your Sudoku Like A Boss",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/benhorsburgh/pyslab",
    python_requires=">=3.8",
    author="Ben Horsburgh",
    packages=find_packages(exclude=["docs*", "tests*", "tools*"]),
    include_package_data=True,
    tests_require=test_requires,
    install_requires=requires,
    keywords="Sudoku",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent"
    ],
    extras_require=extras_require,
)