"""landsat-foorprint setup."""

from setuptools import setup, find_packages

with open("landsat_footprint/__init__.py") as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            break


with open("README.md") as f:
    readme = f.read()

# Runtime requirements.
inst_reqs = ["click", "rasterio[s3]", "rio-tiler~=1.1", "rio_toa", "shapely"]

extra_reqs = {"test": ["pytest", "pytest-cov", "pre-commit", "mock"]}


setup(
    name="landsat_footprint",
    version=version,
    description=u"Skeleton of a python AWS Lambda function",
    long_description=readme,
    python_requires=">=3",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="AWS-Lambda Python",
    author=u"",
    author_email="",
    url="",
    license="BSD",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
    entry_points={"console_scripts": ["l8foot = landsat_footprint.scripts.cli:l8"]},
)
