import sys
import argparse
import GEOparse
from pprint import pprint
import numpy as np
import pandas as pd

class SubsetInfo:
    # The init method or constructor
    def __init__(self, type, values, option):
        # Instance Variable
        self.type = type
        self.values = values
        self.option = option

    def __repr__(self):
        return str(self)

    # Adds an instance variable
    def settype(self, type):
        self.type = type

    # Retrieves instance variable
    def gettype(self):
        return self.type

    # Adds an instance variable
    def setvalues(self, values):
        self.values = values

    # Retrieves instance variable
    def getvalues(self):
        return self.values

    # Adds an instance variable
    def setoption(self, option):
        self.option = option

    # Retrieves instance variable
    def getoption(self):
        return self.option

# def valsNotNumeric(vals):
#     return type(vals.values[0]) == np.float32 or type(vals.values[0]) == np.float64

# def create_CSV_from_SOFT(fff):
#     gds = GEOparse.get_GEO(filepath=fff)
#     df = gds.table
#     dfCols = df.columns
#     # print(df.head(n=2))
#     for col in dfCols:
#         vals = df[col]
#         # print(vals)
#         if not valsNotNumeric(vals):
#             print(f'{col} => NO NUMBERS\n')
#         print(f'{col} => numbers\n')

def get_subsetInfo_by_type(type, subsetInfo_list):
    obj_in_list = None
    obj_index_in_list = 0
    for index, obj in enumerate(subsetInfo_list):
        if obj.gettype() == type:
            obj_in_list = obj
            obj_index_in_list = index
    return obj_in_list, obj_index_in_list

def get_types_with_descriptions_from_data(fff):
    geo_file = GEOparse.get_GEO(filepath=fff, silent=True)
    geo_subsets = geo_file.subsets
    subset_type_list = []
    subsetInfo_obj_list = []
    subsetInfo_option_value = 0
    for gs in geo_subsets:
        subset = geo_subsets.get(gs)
        gs_type = subset.metadata['type'][0]
        gs_description = subset.metadata['description'][0]
        if (gs_type not in subset_type_list):
            # add new subset type to list
            subset_type_list.append(gs_type)
            # create & add new SubsetInfo object with new type & description
            New_SubsetInfo_obj = SubsetInfo(gs_type, [gs_description], subsetInfo_option_value)
            subsetInfo_option_value += 1
            subsetInfo_obj_list.append(New_SubsetInfo_obj)
        else:
            # get object by type, get existing descriptions, add new description & modify in list
            SubsetInfo_obj, subsetInfo_index = get_subsetInfo_by_type(gs_type, subsetInfo_obj_list)
            subsetInfo_obj_values_list = SubsetInfo_obj.getvalues()
            subsetInfo_obj_values_list.append(gs_description)
            SubsetInfo_obj.setvalues(subsetInfo_obj_values_list)
            subsetInfo_obj_list[subsetInfo_index] = SubsetInfo_obj
    subsetInfo_options_list = map(lambda x: x.option, subsetInfo_obj_list)
    return subsetInfo_obj_list, subsetInfo_options_list

def prompt_info_to_user(input_file, subsetInfo_list, optionsList):
    print('-'*200+'\n')
    print("\nThe subsets in input file ("+input_file+") contain the following types and descriptions.\n")
    for o in options_list:
        print(type(o))
        print(o)
    for si in subsetInfo_list:
        print(f"\t Option {si.option}: "+si.type)
        print(f"\t\t values: {si.values}\n")
    selected_option = -1
    while (selected_option not in optionsList):
        input_option = input("\nSelect a subset type in order to create the input data for Parallel-MRNET:")
        try:
            selected_option = int(input_option)
        except:
            print("Option must be a number")
        print(selected_option in options_list)
        print(type(selected_option))
        print(selected_option)


if __name__ == '__main__':
    # PARSE INPUT ARGS
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file",help="Input File with extension '.soft.gz'")
    # parser.add_argument("-o","--output",help="Output File")
    args = parser.parse_args()
    # if args.file and args.output and args.k and args.features and args.clasS:
    if args.file and args.file.endswith('.soft.gz'):
        print("Input OK")
    else:
        print("Use --help for more info")
        sys.exit()

    # GET DATA
    subsetInfo_list, options_list = get_types_with_descriptions_from_data(args.file)
    # GET CLASS
    prompt_info_to_user(args.file, subsetInfo_list, options_list)

    # gds3244_subsetInfo_list = get_types_with_descriptions_from_data("/home/antinux/TFM/Parallel-MRNET/parallel-MRNET/examples/GDS3244_full.soft.gz")
    # gds3795_subsetInfo_list = get_types_with_descriptions_from_data("/home/antinux/TFM/Parallel-MRNET/parallel-MRNET/examples/GDS3795_full.soft.gz")
    # gds5037_subsetInfo_list = get_types_with_descriptions_from_data("/home/antinux/TFM/Parallel-MRNET/parallel-MRNET/examples/GDS5037_full.soft.gz")

    # prompt_info_to_user(gds3244_subsetInfo_list)
    # create_CSV_from_SOFT("/home/antinux/TFM/Parallel-MRNET/parallel-MRNET/examples/GDS3795_full.soft.gz")