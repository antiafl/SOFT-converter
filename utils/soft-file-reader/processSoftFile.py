import sys
import os
import argparse
import GEOparse
from time import sleep
import numpy as np
import pandas as pd

class SubsetInfo:
    # The init method or constructor
    def __init__(self, subsets_list, type, descriptions_list, option):
        # Instance Variable
        self.subsets_list = subsets_list
        self.type = type
        self.descriptions_list = descriptions_list
        self.option = option

    def __repr__(self):
        return str(self)

    # Adds an instance variable
    def setsubsets_list(self, subsets_list):
        self.subsets_list = subsets_list

    # Retrieves instance variable
    def getsubsets_list(self):
        return self.subsets_list

    # Adds an instance variable
    def settype(self, type):
        self.type = type

    # Retrieves instance variable
    def gettype(self):
        return self.type

    # Adds an instance variable
    def setdescriptions_list(self, descriptions_list):
        self.descriptions_list = descriptions_list

    # Retrieves instance variable
    def getdescriptions_list(self):
        return self.descriptions_list

    # Adds an instance variable
    def setoption(self, option):
        self.option = option

    # Retrieves instance variable
    def getoption(self):
        return self.option

def get_subsetInfo_by_type(type, subsetInfo_list):
    obj_in_list = None
    obj_index_in_list = 0
    for index, obj in enumerate(subsetInfo_list):
        if obj.gettype() == type:
            obj_in_list = obj
            obj_index_in_list = index
    return obj_in_list, obj_index_in_list

def add_to_list(item, list):
    list.append(item)
    return list

def create_SubsetInfo_objs_from_subsets(geo_subsets):
    subset_type_list = []
    subsetInfo_obj_list = []
    subsetInfo_option_value = 0
    for gs_name in geo_subsets:
        subset = geo_subsets.get(gs_name)
        gs_type = subset.metadata['type'][0]
        gs_description = subset.metadata['description'][0]
        if (gs_type not in subset_type_list):
            # add new subset type to list
            subset_type_list.append(gs_type)
            # create & add new SubsetInfo object with name, type, description & option
            New_SubsetInfo_obj = SubsetInfo([gs_name], gs_type, [gs_description], subsetInfo_option_value)
            subsetInfo_option_value += 1
            subsetInfo_obj_list.append(New_SubsetInfo_obj)
        else:
            # get object by type, get existing descriptions, add new description & modify in list
            SubsetInfo_obj, subsetInfo_index = get_subsetInfo_by_type(gs_type, subsetInfo_obj_list)
            # subsetInfo_obj_descriptions_list = SubsetInfo_obj.getdescriptions_list()
            # subsetInfo_obj_descriptions_list.append(gs_description)
            subsetInfo_subsets_list = add_to_list(gs_name, SubsetInfo_obj.getsubsets_list())
            SubsetInfo_obj.setsubsets_list(subsetInfo_subsets_list)
            subsetInfo_descriptions_list = add_to_list(gs_description, SubsetInfo_obj.getdescriptions_list())
            SubsetInfo_obj.setdescriptions_list(subsetInfo_descriptions_list)
            subsetInfo_obj_list[subsetInfo_index] = SubsetInfo_obj
    return subsetInfo_obj_list

def prompt_info_to_select_option(input_file, subsetInfo_list, options_list):
    print('-'*200+'\n')
    print("\nThe subsets in input file ("+input_file+") contain the following types and descriptions.\n")
    for si in subsetInfo_list:
        print(f"\t Option {si.option}: "+si.type)
        print(f"\t\t descriptions: {si.descriptions_list}\n")
        print(f"\t\t subsets: {si.subsets_list}\n")
    selected_option = -1
    while (selected_option not in options_list):
        input_option = input(f"\nSelect an option from the following {options_list}: \n")
        try:
            selected_option = int(input_option)
        except:
            print(f"**ERROR: Option must be one of the following numbers {options_list}**")
    print('-'*200+'\n')
    return selected_option

def get_columnList_classList_from_subsets_samples_names(geo_subsets, subsetInfo_list, option, index):
    subset_name_list = subsetInfo_list[option].getsubsets_list()
    # index = 'ID_REF'
    column_values_list = [index]
    class_value = 0
    class_values_list = []
    for gs_name in subset_name_list:
        # get column names from all subsets that correspond with the option selected by the user
        subset = geo_subsets.get(gs_name)
        gs_samples = subset.metadata['sample_id'][0].split(',')
        column_values_list += gs_samples
        row_subset_samples = [class_value] * len(gs_samples)
        class_values_list +=  (row_subset_samples)
        class_value += 1
    return column_values_list, class_values_list

def create_df_from_geo_df(index_values, df, class_values):
    # index: id array (first column of geo df)
    # df: data
    # dictionary:
    #   {
    #       GeneId_1: [values for geneId_1 contained in row 1],
    #       ...,
    #       GeneId_N: [values for geneId_N contained in row N],
    #       Class: [class values]
    #   }
    dictionary = {}
    dictionary["Class"] = class_values
    n = len(index_values)
    for i in range(0, n):
        key = index_values[i]
        row = df.iloc[i]
        dictionary[key] = row.values
        j = i + 1
        # print progress processing rows
        if (j) % (600) == 0:
            sys.stdout.write("\r\tProcessed %d rows out of %d" % (j, n))
            sys.stdout.write("\r")
            sys.stdout.flush()
            sleep(0.25)
    print(f"\r\tAll {n} rows processed\n")
    print("\tNew dataframe:")
    return pd.DataFrame.from_dict(dictionary)

def get_table_data(geo_file, subsetInfo_list, option):
    print("SOFT FILE PROCESSING STARTING...\n")
    # df: dataframe with all original data
    df = geo_file.table
    # get subset samples names (actual columns) and class values for each sample using the option selected by the user in order to get only the needed data in next step
    my_columns, row_class = get_columnList_classList_from_subsets_samples_names(geo_file.subsets, subsetInfo_list, option, index=df.columns[0])
    # df_index: first column that contains all unique ids that will be used as column names
    df_index = df[my_columns[0]].tolist()
    df_data = df[my_columns[1: ]]
    new_df = create_df_from_geo_df(index_values=df_index, df=df_data, class_values=row_class)
    print(new_df)
    print("\n--SOFT FILE PROCESSING FINISHED--\n")
    return new_df

def export_df_to_CSV(df, file_name):
    print('-'*200+'\n')
    csv_file_name = file_name+".csv"
    print("EXPORTING New Dataframe to CSV...\n")
    # df.to_csv(csv_file_name, encoding='utf-8')
    df.to_csv(csv_file_name, index=False)
    cwd = os.getcwd()
    print(f"\tNew dataframe has been saved to file {csv_file_name} in {cwd}\n")
    print("--EXPORTING FINISHED--\n")

if __name__ == '__main__':
    # PARSE INPUT ARGS
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file",help="Required: Input File with extension '.soft.gz'")
    parser.add_argument("-o","--output",help="Optional: Name for CSV Output File")
    args = parser.parse_args()
    if args.file and args.file.endswith('.soft.gz'):
        print("Input OK")
    else:
        print("\tUse --help for more info\n")
        sys.exit()

    # GET GEO FILE & SUBSETS
    geo_file = GEOparse.get_GEO(filepath=args.file, silent=True)
    # GET TYPES WITH DESCRIPTIONS, SUBSETS & OPTIONS
    subsetInfo_list = create_SubsetInfo_objs_from_subsets(geo_file.subsets)
    types_options_list = list(map(lambda x: x.option, subsetInfo_list))
    # GET TYPE TO USE FOR CLASS
    user_selected_option = prompt_info_to_select_option(args.file, subsetInfo_list, types_options_list)
    # GET DATA USING SELECTED OPTION
    new_df = get_table_data(geo_file, subsetInfo_list, user_selected_option)
    # EXPORT DATA TO CSV
    file_name = geo_file.name
    if args.output:
        file_name = args.output
    export_df_to_CSV(new_df, file_name)
