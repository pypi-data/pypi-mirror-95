import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="platemap",
    version="0.0.2b",
    url="https://github.com/Benedict-Carling/platemap",
    author="Benedict Carling",
    author_email="benedict.carling18@imperial.ac.uk",
    license="MIT",
    description="A package for working with plates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(
        exclude=("tests","docsource")
    ),  # package_data not correctly migrated if "where" arg used.
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires=">=3.7",
    #install_requires=["biopython>=1.78", "python-Levenshtein", "sbol2"],
    #project_urls={
    #    "Documentation": "https://londonbiofoundry.github.io/basicsynbio/index.html",
    #    "Source": "https://github.com/LondonBiofoundry/basicsynbio",
    #},
)