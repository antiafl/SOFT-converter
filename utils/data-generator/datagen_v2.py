from random import randint  
import GEOparse
import numpy as np
import pandas as pd

class SubsetInfo:
    # The init method or constructor
    def __init__(self, type, values):
        # Instance Variable
        self.type = type
        self.values = values
     
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


def create_CSV_from_SOFT(fff):
    gds = GEOparse.get_GEO(filepath=fff)
    df = gds.table
    dfCols = df.columns
    # print(df.head(n=2))
    for col in dfCols:
        vals = df[col]
        # print(vals)
        if not valsNotNumeric(vals):
            print(f'{col} => NO NUMBERS\n')
        print(f'{col} => numbers\n')

def get_subsetInfo_inList(subsetInfo_obj, subsetInfo_list):
    obj_in_list = False
    for obj in subsetInfo_list:
        if obj.type
        print(obj.name, obj.roll, sep=' ')
    return is_in_list

def getClassFromData(fff):
    geo_file = GEOparse.get_GEO(filepath="/home/antinux/TFM/Fast-mRMR/Fast-mRMR-master/fast-mRMR/examples/GDS3795_full.soft.gz")
    geo_subsets = geo_file.subsets
    subset_list = []
    subset_types_list = ()
    for i in geo_subsets: 
        print(i)
        subset = geo_subsets.get(i)
        print(subset.metadata)
        Subset_i = SubsetInfo(subset.metadata['type'], subset_metadata['description'])
        if subset_list.
        subset_list.append(Subset_i)
        for k,v in subset.metadata:
            current_subset_type_value = ''
            if k=='type'& v not in subset_types_list:
                subset_types_list.append(v)
                current_subset_type_value = v
            if k=='description':
                subset_dictionary_values
        subset_metadata = subset.metadata
        print(subset_metadata.get('type'))
        # obter todos os tipos de subsets
        # diferenciar entre os tipos cales son os que teñen varias descripcións diferentes
        # asignar para cada descripción dun tipo un nº que representará a class
        # presentar como opcións ao usuario os tipos + descripcións
        # recoller selección do usuario
        # construir os datos para esa elección 


getClassFromData("/home/antinux/TFM/Fast-mRMR/Fast-mRMR-master/fast-mRMR/examples/GDS3244_full.soft.gz")
getClassFromData("/home/antinux/TFM/Fast-mRMR/Fast-mRMR-master/fast-mRMR/examples/GDS3795_full.soft.gz")
getClassFromData("/home/antinux/TFM/Fast-mRMR/Fast-mRMR-master/fast-mRMR/examples/GDS5037_full.soft.gz")
# create_CSV_from_SOFT("/home/antinux/TFM/Fast-mRMR/Fast-mRMR-master/fast-mRMR/examples/GDS3795_full.soft.gz")