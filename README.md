# SOFT-converter

Welcome to the SOFT-converter wiki :)

This repository contains a tool to convert a SOFT file into a CSV file for feature selection purposes.

The code is arranged in the 4 main following blocks:
1. *Open/read SOFT file to obtain all types and descriptions*
2. *Present obtained types and descriptions to user as different options to select from*
3. *Extract from SOFT file only relevant data according to the user selected option*
4. *Export data to CSV*

## Execution

This tool has been implemented using Python 3.

Follow these steps to execute the SOFT converter:
* cd SOFT-converter/code
* python3 processSoftFile.py -f ../examples/soft-files/GDS_file.soft.gz

Is important to note this tool can use as input both a SOFT file with any of these two extensions: '.soft.gz' or '.soft', or the accesion number of the desired GEO dataset using the option -a instead.

The tool outputs a CSV file, it is possible to specify the name of the output file using the -o option followed by the desired output name, with or without the '.csv' extension.

## User input

During the execution the tool will prompt the user with different options to choose from. These options reflect the different ways the data from a dataset is organized and the different classes correspon with the data. Once the user has input an option the execution will continue with the selected option.