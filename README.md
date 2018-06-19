# TensorImageSearch
Automate the extraction of tensorflow image recognition data for use in e-discovery software or SQLITE database files

# Pre-requisites

Tensorflow models repo cloned as per:
https://www.tensorflow.org/tutorials/image_recognition

ClassifyImage_LoadFile.py from this repository should be run from the same directory as the classify_image.py script from the tensorflow models repo.

Uses python 3

# Setup

Create a source directory with the image files in that you would like to classify.  The script will recurse through sub-directories.

Create a blank output directory.

Change the default source and output directories specified in the script, to your source and output directories.

