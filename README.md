
# TensorImageSearch
Automate the extraction of tensorflow image recognition data for use in e-discovery software or SQLITE database files

# Pre-requisites

Tensorflow models repo cloned as per:
https://www.tensorflow.org/tutorials/image_recognition

ImageClassify_LoadFile.py from this repo should be run from the same directory as the classify_image.py script from the tensorflow models repo.

Uses python 3

# Setup

Create a source directory with the image files that are to be classified.  The script will recurse through sub-directories.

Create a blank output directory.

Change the default source and output directories specified in the script, to your source and output directories.

# Output

The script will create:
i)A load file in concordance .dat format with the following fields: DOCID, Name, Path, TopPrediction, TopPredictionScore, ITEM_PATH, TEXT_PATH
ii)A native directory containing copies of the native files, named by DOCID(a uniquely allocated sequential number)
iii)A text directory containing the results of the tensorflow image classification for each native file.  These text files are named by DOCID
iv)A SQLITE database file called imageclassify.db, which contains one table that lists the files, and one that lists separate rows for each prediction relating to the files.  

# Use

The concordance load file can be used to load the native image files, and associated prediction text into a e-discovery tool, to keyword search alongside other file types such as docx, emails etc.  So for example, if one of the tensorflow image classify predictions was cheetah, if the files were loaded into an e-discovery tool using the concordance load file generated from this script, then the image file associated with the prediction cheetah would be returned in the e-discovery result set for keyword cheetah.  The concordance load file also lists the top prediction and score as separate metadata fields, so you can search across e.g. top prediction contains 'x' in the e-discovery tool.

The SQLITE database file can be used as a standalone file for searching through all predictions for a set of files. The tables are structured as follows:

CREATE TABLE FilesTable(DOCID, Name, OrigPath, NewPath)

CREATE TABLE FilePredictionTable(DOCID, Prediction, Score NUMERIC)



