from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="frappymongodataset",
      version="1.3.2",
      description="Store Implementation for Data Sets in MongoDB",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/ilfrich/frappy-py-mongo-dataset-store",
      author="Peter Ilfrich",
      author_email="das-peter@gmx.de",
      packages=[
          "frappymongodataset"
      ],
      install_requires=[
            "pbu",
            "numpy",
            "Pillow",
            "pandas",
      ],
      tests_require=[
          "pytest",
      ],
      zip_safe=False)
