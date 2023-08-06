#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 11:20:42 2019

@author: andreas geiges
"""

import datatoolbox as dt
from datatoolbox import config
from datatoolbox.data_structures import Datatable
from datatoolbox.util import isUnit, yearsColumnsOnly

from collections import defaultdict
import pandas as pd
import os
import time
import pint
import re

tt = time.time()

MAPPING_COLUMNS = list(config.ID_FIELDS) + config.OPTIONAL_META_FIELDS + ['unit','unitTo']
VAR_MAPPING_SHEET = 'variable_mapping'
SPATIAL_MAPPING_SHEET = 'spatial_mapping'



def highlight_column(s, col):
    return ['background-color: #d42a2a' if s.name in col else '' for v in s.index]

class setupStruct(object):
    pass

class sourcesStruct(object):
    
    def __init__(self):
        self.inventory = list()
    def __setitem__(self, name, obj):
        self.__setattr__(name, obj)
        self.inventory.append(name)
        
    def getAll(self):
        return self.inventory
    
    def __str__(self):
        return str([x for x in self.inventory])
    
    
class BaseImportTool():
    
    def __init__(self):
        self.setup = setupStruct()
    
    def loadData(self):
        pass
    
    def loadVariableMapping(self):
        self.mapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET)
    
    def gatherMappedData(self):
        pass
    
    def openMappingFile(self):
        if dt.config.OS == 'Linux':
            os.system('libreoffice ' + self.setup.MAPPING_FILE)
        elif dt.config.OS == 'Darwin':
            os.system('open -a "Microsoft Excel" ' + self.setup.MAPPING_FILE)

    def openRawData(self):
        if dt.config.OS == 'Linux':
            os.system('libreoffice ' + self.setup.DATA_FILE )
        elif dt.config.OS == 'Darwin':
            os.system('open -a "Microsoft Excel" ' + self.setup.DATA_FILE )

    def createSourceMeta(self):
        self.meta = {'SOURCE_ID': self.setup.SOURCE_ID,
                      'collected_by' : config.CRUNCHER,
                      'date': dt.core.getDateString(),
                      'source_url' : self.setup.URL,
                      'licence': self.setup.LICENCE }


    def update(self, updateContent=False):   
        tableList = self.gatherMappedData(updateTables=updateContent)
        dt.commitTables(tableList, f'update {self.__class__.__name__} data', self.meta, update=updateContent)
 

class WDI_2018(BaseImportTool):
    
    def __init__(self):

        self.setup = setupStruct()
        
        self.setup.SOURCE_ID    = "WDI2018"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/WDI2018/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH + 'WDIData.csv'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        self.setup.LICENCE = 'CC BY-4.0'
        self.setup.URL     = 'https://datacatalog.worldbank.org/dataset/world-development-indicators'

        
        self.setup.INDEX_COLUMN_NAME = 'Indicator Code'
        self.setup.SPATIAL_COLUM_NAME = 'Country Code'
        
        self.setup.COLUMNS_TO_DROP = ['Country Name', 'Indicator Name']
        

        
        self.createSourceMeta()
                
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            
            self.createVariableMapping()
        else:
            self.mapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET)
            
        


        
    def createVariableMapping(self):
        
        self.availableSeries = pd.read_csv(self.setup.SOURCE_PATH+ '/WDISeries.csv', index_col=None, header =0)
        print(self.availableSeries.index)
        self.mapping = pd.DataFrame(index=self.availableSeries.index, columns = list(config.REQUIRED_META_FIELDS) + ['unitTo'])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        self.mapping.scenario = 'historic'
        
        self.mapping.to_excel(self.setup.MAPPING_FILE, engine='openpyxl', sheet_name=VAR_MAPPING_SHEET)


    def loadData(self):        
        self.data = pd.read_csv(self.setup.DATA_FILE, index_col = self.setup.INDEX_COLUMN_NAME, header =0) 
    
    def gatherMappedData(self, spatialSubSet = None, updateTables = False):
        
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
        
        indexDataToCollect = self.mapping.index[~pd.isnull(self.mapping['entity'])]
        
        tablesToCommit  = []
        for idx in indexDataToCollect:
            metaDf = self.mapping.loc[idx]
            
            
            print(metaDf[config.REQUIRED_META_FIELDS].isnull().all() == False)
            #print(metaData[self.setup.INDEX_COLUMN_NAME])
            
            
            metaDict = {key : metaDf[key] for key in config.REQUIRED_META_FIELDS.union({'unitTo'})}
#            metaDict['unitTo'] = self.mappingEntity.loc[entity]['unitTo']
            seriesIdx = metaDf['Series Code']
            metaDict['original code'] = metaDf['Series Code']
            metaDict['original name'] = metaDf['Indicator Name']

            if not updateTables:
                if dt.core.DB.tableExist(dt.core._createDatabaseID(metaDict)):
                    continue
                        
            dataframe = self.data.loc[seriesIdx]
            
            if spatialSubSet:
                spatIdx = dataframe[self.setup.SPATIAL_COLUM_NAME].isin(spatialSubSet)
                dataframe = dataframe.loc[spatIdx]
            
            dataframe = dataframe.set_index(self.setup.SPATIAL_COLUM_NAME).drop(self.setup.COLUMNS_TO_DROP, axis=1)
            dataframe= dataframe.dropna(axis=1, how='all')
            
            dataTable = Datatable(dataframe, meta=metaDict)
            
            if not pd.isna(metaDict['unitTo']):
                dataTable = dataTable.convert(metaDict['unitTo'])
                
            tablesToCommit.append(dataTable)
        return tablesToCommit

class WDI_2020(BaseImportTool):
    
    def __init__(self):

        self.setup = setupStruct()
        
        self.setup.SOURCE_ID    = "WDI_2020b"
        self.setup.SOURCE_NAME    = "WDI"
        self.setup.SOURCE_YEAR    = "2020b"
        self.setup.SOURCE_PATH  = os.path.join(config.PATH_TO_DATASHELF, 'rawdata', self.setup.SOURCE_ID)
        self.setup.DATA_FILE    = 'WDIData.csv'
        self.setup.MAPPING_FILE = os.path.join(self.setup.SOURCE_PATH, 'mapping.xlsx')
        self.setup.LICENCE = 'CC BY-4.0'
        self.setup.URL     = 'https://datacatalog.worldbank.org/dataset/world-development-indicators'

        
        self.setup.INDEX_COLUMN_NAME = 'Indicator Code'
        self.setup.SPATIAL_COLUM_NAME = 'Country Code'
        
        self.setup.COLUMNS_TO_DROP = ['Country Name', 'Indicator Name']
        

        
        self.createSourceMeta()
                
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            
            self.createVariableMapping()
            
        else:
            self.mapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET)
        
    

        
    def createVariableMapping(self):
        
        fullFilePath = os.path.join(self.setup.SOURCE_PATH, self.setup.DATA_FILE)
        self.availableSeries = pd.read_csv(fullFilePath, index_col=None, header =0)
        print(self.availableSeries.index)
        self.mapping = pd.DataFrame(index=self.availableSeries.index, columns = list(config.REQUIRED_META_FIELDS) + ['unitTo'])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        self.mapping.scenario = 'Historic'
        
        self.mapping.to_excel(self.setup.MAPPING_FILE, engine='openpyxl', sheet_name=VAR_MAPPING_SHEET)


    def loadData(self):        
        fullFilePath = os.path.join(self.setup.SOURCE_PATH, self.setup.DATA_FILE)
        self.data = pd.read_csv(fullFilePath, index_col = self.setup.INDEX_COLUMN_NAME, header =0) 
    
    def gatherMappedData(self, spatialSubSet = None, updateTables = False):
        
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
        
        indexDataToCollect = self.mapping.index[~pd.isnull(self.mapping['entity'])]
        
        tablesToCommit  = []
        for idx in indexDataToCollect:
            metaDf = self.mapping.loc[idx]
            
            
            print(metaDf[config.REQUIRED_META_FIELDS].isnull().all() == False)
            #print(metaData[self.setup.INDEX_COLUMN_NAME])
            
            metaDf['source_name'] = self.setup.SOURCE_NAME
            metaDf['source_year'] = self.setup.SOURCE_YEAR
            metaDict = {key : metaDf[key] for key in config.REQUIRED_META_FIELDS.union({'category', 'unitTo'})}
#            metaDict['unitTo'] = self.mappingEntity.loc[entity]['unitTo']
            seriesIdx = metaDf['Series Code']
            metaDict['original code'] = metaDf['Series Code']
            metaDict['original name'] = metaDf['Indicator Name']
            
            

            if pd.isnull(metaDict['category']):
                metaDict['category'] = ''
#            if pd.isnull(metaDict['model']):
#                metaDict['model'] = ''
            if not updateTables:
                #print(metaDict)
                if dt.core.DB.tableExist(dt.core._createDatabaseID(metaDict)):
                    continue
                        
            dataframe = self.data.loc[seriesIdx]
            
            if spatialSubSet:
                spatIdx = dataframe[self.setup.SPATIAL_COLUM_NAME].isin(spatialSubSet)
                dataframe = dataframe.loc[spatIdx]
            
            dataframe = dataframe.set_index(self.setup.SPATIAL_COLUM_NAME).drop(self.setup.COLUMNS_TO_DROP, axis=1)
            dataframe= dataframe.dropna(axis=1, how='all')
            
            dataTable = Datatable(dataframe, meta=metaDict)
            
            dataTable.loc['EU28',:] = dataTable.loc['EUU',:]
            
            if not pd.isna(metaDict['unitTo']):
                dataTable = dataTable.convert(metaDict['unitTo'])
                
            tablesToCommit.append(dataTable)
        return tablesToCommit

class IEA_FUEL_2018(BaseImportTool):
    """
    IEA World fuel emissions
    """
    def __init__(self):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "IEA_CO2_FUEL_2018"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/IEA_CO2_FUEL_2018/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH + 'World_CO2_emissions_fuel_2018.csv'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        self.setup.LICENCE = 'restricted'
        self.setup.URL     = 'https://www.iea.org/statistics/co2emissions/'
        
        self.setup.INDEX_COLUMN_NAME = ['FLOW (Mt of CO2)', 'PRODUCT']
        self.setup.SPATIAL_COLUM_NAME = 'COUNTRY'
        self.setup.COLUMNS_TO_DROP = [ 'PRODUCT','FLOW (Mt of CO2)','combined']
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
        else:
            self.mapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET)
            self.spatialMapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=SPATIAL_MAPPING_SHEET)

        self.createSourceMeta()


    def loadData(self):
        self.data = pd.read_csv(self.setup.DATA_FILE, encoding='utf8', engine='python', index_col = None, header =0, na_values=['..','c', 'x', 'nan'])
        self.data['combined'] = self.data[self.setup.INDEX_COLUMN_NAME].apply(lambda x: '_'.join(x), axis=1)
        
        self.data = self.data.set_index(self.data['combined'])#.drop('combined',axis=1)

        
    def createVariableMapping(self):        

        productMapping = {'Total': 'total',
                         'Coal, peat and oil shale': 'coal_peat_oil_shale',
                         'Oil': 'oil',
                         'Natural gas': 'natural_gas',
                         'Other': 'other'}
        
        flowMapping = {'CO2 Fuel combustion': 'Emissions|Fuel|CO2',}
#                     'Electricity and heat production': 'Electricity_and_heat_production',
#                     'Other energy industry own use': 'Other_energy_industry_own_use',
#                     'Manufacturing industries and construction': 'Manufacturing_industries_and_construction',
#                     'Transport': 'Transport',
#                     ' of which: road': 'Road transport',
#                     ' Residential': 'Residential',
#                     ' Commercial and public services': 'Commercial_and_public_services',
#                     ' Agriculture/forestry': 'Agriculture/forestry',
#                     ' Fishing': '_Fishing',
#                     'Memo: International marine bunkers': 'Memo:_International_marine_bunkers',
#                     'Memo: International aviation bunkers': 'Memo:_International_aviation_bunkers',
#                     'Memo: Total final consumption': 'Memo:_Total_final_consumption'}

        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')                
                
        #%%
        
        if not hasattr(self, 'data'):
#            self.data = pd.read_csv(self.setup.DATA_FILE, encoding='utf8', engine='python', index_col = None, header =0, na_values='..')
#            self.data['combined'] = self.data[self.setup.INDEX_COLUMN_NAME].apply(lambda x: '_'.join(x), axis=1)
            self.loadData()
            
        index = self.data['combined'].unique()

        #%%
        # spatial mapping
        self.spatialMapping = dict()
        spatialIDList = self.data[self.setup.SPATIAL_COLUM_NAME].unique()
        from hdx.location.country import Country
        for spatID in spatialIDList:
            ISO_ID = dt.mapp.getSpatialID(spatID)
            ISO_ID = Country.get_iso3_country_code_fuzzy(spatID)[0]
            if ISO_ID is not None:
                self.spatialMapping[spatID] = ISO_ID
            else:
                print('not found: ' + spatID)
                
        # adding regions
        self.spatialMapping['World'] = "World"
        
        dataFrame = pd.DataFrame(data=[],columns = ['alternative'])
        for key, item in self.spatialMapping.items():
            dataFrame.loc[key] = item
        dataFrame.to_excel(writer, sheet_name=SPATIAL_MAPPING_SHEET)
        
        #%%
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = MAPPING_COLUMNS)
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        self.mapping.scenario = 'historic'
        
        self.mapping['flow'] = self.mapping.index
        self.mapping['flow'] = self.mapping['flow'].apply(lambda x: x[0:x.rfind('_')])
        self.mapping['product'] = self.mapping.index
        self.mapping['product'] = self.mapping['product'].apply(lambda x: x[x.rfind('_')+1:])        
        
        for key, value in flowMapping.items():
            mask = self.mapping['flow'].str.match(key)
            for pKey, pValue in productMapping.items():
                pMask = self.mapping['product'].str.match(pKey)
                self.mapping['entity'][mask&pMask] = '_'.join([value, pValue])
                if 'GWh' in key:
                    self.mapping['unit'][mask&pMask] = 'GWh'
                else:
                    self.mapping['unit'][mask&pMask] = 'TJ'
                
        #self.mapping = self.mapping.drop(['product','flow'],axis=1)
        self.mapping.to_excel(writer, sheet_name=VAR_MAPPING_SHEET)
        writer.close() 
    
    def gatherMappedData(self, spatialSubSet = None, updateTables = False):
        
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
        
        indexDataToCollect = self.mapping.index[~pd.isnull(self.mapping['entity'])]
        
        tablesToCommit  = []
        excludedTables = dict()
        excludedTables['empty'] = list()
        excludedTables['erro'] = list()
        excludedTables['exists'] = list()
        for idx in indexDataToCollect:
            metaDf = self.mapping.loc[idx]
            print(idx)
            
            #print(metaDf[config.REQUIRED_META_FIELDS].isnull().all() == False)
            #print(metaData[self.setup.INDEX_COLUMN_NAME])
            
            
            metaDict = {key : metaDf[key] for key in config.REQUIRED_META_FIELDS.union({'unitTo'})} 
            if pd.isna(metaDict['category']):
                metaDict['category'] = ''
            metaDict['original codle'] = idx
            #metaDict['original name'] = metaDf['Indicator Name']
            
            seriesIdx = idx
            
            print(metaDict)
            
            if not updateTables:
                tableID = dt.core._createDatabaseID(metaDict)
                print(tableID)
                if not updateTables:
                    if dt.core.DB.tableExist(tableID):
                        excludedTables['exists'].append(tableID)
                        continue
            
            dataframe = self.data.loc[seriesIdx]
            
            
            newData= list()
            for iRow in range(len(dataframe)):
                if dataframe.COUNTRY.iloc[iRow] in self.spatialMapping.index:
                    newData.append(self.spatialMapping.alternative.loc[dataframe.COUNTRY.iloc[iRow]])
                else:
                    newData.append(pd.np.nan)
            dataframe.loc[:,'COUNTRY'] = newData
           
            if spatialSubSet:
                spatIdx = dataframe[self.setup.SPATIAL_COLUM_NAME].isin(spatialSubSet)
                dataframe = dataframe.loc[spatIdx]
            
            dataframe = dataframe.set_index(self.setup.SPATIAL_COLUM_NAME).drop(self.setup.COLUMNS_TO_DROP, axis=1)
            
            dataframe= dataframe.dropna(axis=1, how='all')
            dataframe= dataframe.loc[~pd.isna(dataframe.index)]
            dataTable = Datatable(dataframe, meta=metaDict)
            
            if not pd.isna(metaDict['unitTo']):
                dataTable = dataTable.convert(metaDict['unitTo'])
                
            tablesToCommit.append(dataTable)
        
        return tablesToCommit, excludedTables



class IEA_FUEL_DETAILED_2019(BaseImportTool):
    """
    IEA World fuel emissions detail version
    """
    def __init__(self):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "IEA_CO2_FUEL_2019"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/IEA_CO2_FUEL_2019/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH + 'WOLRD_CO2_emissions_fuel_2019_detailed.csv'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping_detailed.xlsx'
        self.setup.LICENCE = 'restricted'
        self.setup.URL     = 'https://www.iea.org/statistics/co2emissions/'

        self.setup.INDEX_COLUMN_NAME = ['FLOW (kt of CO2)', 'PRODUCT']
        self.setup.SPATIAL_COLUM_NAME = 'COUNTRY'
        self.setup.COLUMNS_TO_DROP = [ 'PRODUCT','FLOW (kt of CO2)','combined']
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
        else:
            self.mapping = self.loadVariableMapping()
            self.spatialMapping = self.loadSpatialMapping()
            
        self.createSourceMeta()

    def loadVariableMapping(self,):
        mapping = dict()
        
        for variableName in self.setup.INDEX_COLUMN_NAME:
            mapping[variableName] = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=variableName,index_col=0)
            notNullIndex = mapping[variableName].index[~mapping[variableName].isna().mapping]
            mapping[variableName] = mapping[variableName].loc[notNullIndex]
        
        return mapping

    def loadSpatialMapping(self,):
        return pd.read_excel(self.setup.MAPPING_FILE, sheet_name='spatial')
    
    
    def loadData(self):
        self.data = pd.read_csv(self.setup.DATA_FILE, encoding='utf8', engine='python', index_col = None, header =0, na_values=['..','c', 'x', 'nan'])
        self.data['combined'] = self.data[self.setup.INDEX_COLUMN_NAME].apply(lambda x: '_'.join(x), axis=1)
        
        self.data = self.data.set_index(self.data['combined'])#.drop('combined',axis=1)

        
    def createVariableMapping(self):        
        
        # loading data if necessary
        if not hasattr(self, 'data'):        
            self.loadData()
        
        
        import numpy as np
 
        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')       
        
        for column in self.setup.INDEX_COLUMN_NAME:
            #models
            index = self.data.loc[:,column].unique()
        
            self.availableSeries = pd.DataFrame(index=index)
            self.mapping = pd.DataFrame(index=index, columns = ['mapping'])

            self.mapping.to_excel(writer, engine='openpyxl', sheet_name=column)

        #spatial mapping
        column = self.setup.SPATIAL_COLUM_NAME
        
        index = self.data.loc[:,column].unique()
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = ['mapping'])
        
        for region in self.mapping.index:
            coISO = dt.mapp.getSpatialID(region)
            
            if coISO is not None:
                self.mapping.loc[region,'mapping'] = coISO
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='spatial')
        
        writer.close()

    def gatherMappedData(self, spatialSubSet = None, updateTables=False):
    
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        

        # meta data
#        self.loadMetaData()
        
        tablesToCommit  = []
        metaDict = dict()
        metaDict['source'] = self.setup.SOURCE_ID
        excludedTables = dict()
        excludedTables['empty'] = list()
        excludedTables['error'] = list()
        excludedTables['exists'] = list()
        
        for product in self.mapping['PRODUCT'].index:
            mask = self.data['PRODUCT'] == product
            tempDataMo = self.data.loc[mask]
            
            for flow in self.mapping['FLOW (kt of CO2)'].index:
#                metaDict['scenario'] = scenario + '|' + model
                mask = tempDataMo['FLOW (kt of CO2)'] == flow
                tempDataMoSc = tempDataMo.loc[mask]
                
                
                metaDict['entity'] = '|'.join([self.mapping['FLOW (kt of CO2)'].mapping.loc[flow],
                                              self.mapping['PRODUCT'].mapping.loc[product]])
                metaDict['scenario']  = 'historic'
                metaDict['category']  = ''
                
                for key in [ 'unit', 'unitTo']:
                    metaDict[key] = self.mapping['FLOW (kt of CO2)'].loc[flow,key]
                
                print(metaDict)
                tableID = dt.core._createDatabaseID(metaDict)
                #print(tableID)
                if not updateTables:
                    if dt.core.DB.tableExist(tableID):
                        excludedTables['exists'].append(tableID)
                        continue


                    
                if len(tempDataMoSc.index) > 0:

                    dataframe = tempDataMoSc.set_index(self.setup.SPATIAL_COLUM_NAME)
                    if spatialSubSet:
                        spatIdx = dataframe[self.setup.SPATIAL_COLUM_NAME].isin(spatialSubSet)
                        dataframe = tempDataMoSc.loc[spatIdx]
                    
                    dataframe = dataframe.drop(self.setup.COLUMNS_TO_DROP, axis=1)
                    dataframe = dataframe.dropna(axis=1, how='all').astype(float)
        
                    validSpatialRegions = self.spatialMapping.index[~self.spatialMapping.mapping.isnull()]
                    dataframe = dataframe.loc[validSpatialRegions,:]
                    dataframe.index = self.spatialMapping.mapping[~self.spatialMapping.mapping.isnull()]

                    
                    dataTable = Datatable(dataframe, meta=metaDict)
                    # possible required unit conversion
                    if not pd.isna(metaDict['unitTo']):
                        dataTable = dataTable.convert(metaDict['unitTo'])
                    tablesToCommit.append(dataTable)
                else:
                    excludedTables['empty'].append(tableID)

        return tablesToCommit, excludedTables
    
    

class IEA_FUEL_2019(BaseImportTool):
    """
    IEA World fuel emissions
    """
    def __init__(self):
        self.setup = setupStruct()
        self.setup.SOURCE_ID      = "IEA_CO2_FUEL_2019"
        self.setup.SOURCE_NAME    = "IEA_CO2_FUEL"
        self.setup.SOURCE_YEAR    = "2019"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/IEA_CO2_FUEL_2019/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH + 'World_CO2_emissions_fuel_2019.csv'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        self.setup.LICENCE = 'restricted'
        self.setup.URL     = 'https://www.iea.org/statistics/co2emissions/'
        
        self.setup.INDEX_COLUMN_NAME = ['FLOW (kt of CO2)', 'PRODUCT']
        self.setup.SPATIAL_COLUM_NAME = 'COUNTRY'
        self.setup.COLUMNS_TO_DROP = [ 'PRODUCT','FLOW (kt of CO2)','combined']
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
        else:
            self.mapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET)
            self.spatialMapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=SPATIAL_MAPPING_SHEET)

        self.createSourceMeta()


    def loadData(self):
        self.data = pd.read_csv(self.setup.DATA_FILE, encoding='utf8', engine='python', index_col = None, header =0, na_values=['..','c', 'x', 'nan'])
        self.data['combined'] = self.data[self.setup.INDEX_COLUMN_NAME].apply(lambda x: '_'.join(x), axis=1)
        
        self.data = self.data.set_index(self.data['combined'])#.drop('combined',axis=1)

        
    def createVariableMapping(self):        

        productMapping = {'Total': 'Total',
                         'Coal, peat and oil shale': 'Coal_peat_oil_shale',
                         'Oil': 'Oil',
                         'Natural gas': 'Natural_gas',
                         'Other': 'Other'}
        
        entity = "Emissions|CO2|Combustion"
        flowMapping = {'CO2 fuel combustion': 'Total',
                     'Electricity and heat production': 'Electricity&heat',
#                     'Other energy industry own use': 'Other_energy_industry_own_use',
#                     'Manufacturing industries and construction': 'Manufacturing_industries_and_construction',
                      'Transport': 'Transport',
                      ' of which: road': 'Transports|Road',
                      'Residential': 'Residential',}
#                      'Commercial and public services': 'Commercial&public_services',
#                     ' Agriculture/forestry': 'Agriculture/forestry',
#                     ' Fishing': '_Fishing',
#                     'Memo: International marine bunkers': 'Memo:_International_marine_bunkers',
#                     'Memo: International aviation bunkers': 'Memo:_International_aviation_bunkers',
#                     'Memo: Total final consumption': 'Memo:_Total_final_consumption'}

        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')                
                
        #%%
        
        if not hasattr(self, 'data'):
#            self.data = pd.read_csv(self.setup.DATA_FILE, encoding='utf8', engine='python', index_col = None, header =0, na_values='..')
#            self.data['combined'] = self.data[self.setup.INDEX_COLUMN_NAME].apply(lambda x: '_'.join(x), axis=1)
            self.loadData()
            
        index = self.data['combined'].unique()

        #%%
        # spatial mapping
        self.spatialMapping = dict()
        spatialIDList = self.data[self.setup.SPATIAL_COLUM_NAME].unique()
        from hdx.location.country import Country
        for spatID in spatialIDList:
            ISO_ID = dt.mapp.getSpatialID(spatID)
            ISO_ID = Country.get_iso3_country_code_fuzzy(spatID)[0]
            if ISO_ID is not None:
                self.spatialMapping[spatID] = ISO_ID
            else:
                print('not found: ' + spatID)
                
        # adding regions
        self.spatialMapping['World'] = "World"
        
        dataFrame = pd.DataFrame(data=[],columns = ['alternative'])
        for key, item in self.spatialMapping.items():
            dataFrame.loc[key] = item
        dataFrame.to_excel(writer, sheet_name=SPATIAL_MAPPING_SHEET)
        
        #%%
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = MAPPING_COLUMNS)
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        self.mapping.scenario = 'Historic'
        
        self.mapping['flow'] = self.mapping.index
        self.mapping['flow'] = self.mapping['flow'].apply(lambda x: x[0:x.rfind('_')])
        self.mapping['product'] = self.mapping.index
        self.mapping['product'] = self.mapping['product'].apply(lambda x: x[x.rfind('_')+1:])        
        
        for key, value in flowMapping.items():
            mask = self.mapping['flow'].str.match(key)
            for pKey, pValue in productMapping.items():
                pMask = self.mapping['product'].str.match(pKey)
                self.mapping['entity'][mask&pMask] = '|'.join([value, pValue])
                self.mapping['unit'][mask&pMask] = 'kt CO2'
                self.mapping['unitTo'][mask&pMask] = 'Mt CO2'
                
        #self.mapping = self.mapping.drop(['product','flow'],axis=1)
        self.mapping.to_excel(writer, sheet_name=VAR_MAPPING_SHEET)
        writer.close() 
    
    def gatherMappedData(self, spatialSubSet = None, updateTables = False):
        
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
        
        indexDataToCollect = self.mapping.index[~pd.isnull(self.mapping['entity'])]
        
        tablesToCommit  = []
        excludedTables = dict()
        excludedTables['empty'] = list()
        excludedTables['erro'] = list()
        excludedTables['exists'] = list()
        for idx in indexDataToCollect:
            metaDf = self.mapping.loc[idx]
            print(idx)
            
            #print(metaDf[config.REQUIRED_META_FIELDS].isnull().all() == False)
            #print(metaData[self.setup.INDEX_COLUMN_NAME])
            metaDf['source_name'] = self.setup.SOURCE_NAME
            metaDf['source_year'] = self.setup.SOURCE_YEAR
            
            metaDict = {key : metaDf[key] for key in config.REQUIRED_META_FIELDS.union({"unit", "category"})} 
#            if pd.isna(metaDict['category']):
#            metaDict['unit'] = metaDf['unit']
            metaDict['original code'] = idx
            #metaDict['original name'] = metaDf['Indicator Name']
            
            seriesIdx = idx
            
            print(metaDict)
            
            if not updateTables:
                tableID = dt.core._createDatabaseID(metaDict)
                print(tableID)
                if not updateTables:
                    if dt.core.DB.tableExist(tableID):
                        excludedTables['exists'].append(tableID)
                        continue
            
            dataframe = self.data.loc[seriesIdx]
            
            
            newData= list()
            for iRow in range(len(dataframe)):
                if dataframe.COUNTRY.iloc[iRow] in self.spatialMapping.index:
                    newData.append(self.spatialMapping.alternative.loc[dataframe.COUNTRY.iloc[iRow]])
                else:
                    newData.append(pd.np.nan)
            dataframe.loc[:,'COUNTRY'] = newData
           
            if spatialSubSet:
                spatIdx = dataframe[self.setup.SPATIAL_COLUM_NAME].isin(spatialSubSet)
                dataframe = dataframe.loc[spatIdx]
            
            dataframe = dataframe.set_index(self.setup.SPATIAL_COLUM_NAME).drop(self.setup.COLUMNS_TO_DROP, axis=1)
            
            dataframe= dataframe.dropna(axis=1, how='all')
            dataframe= dataframe.loc[~pd.isna(dataframe.index)]
            dataTable = Datatable(dataframe, meta=metaDict)
            
            if not pd.isna(metaDf['unitTo']):
                dataTable = dataTable.convert(metaDf['unitTo'])
                
            tablesToCommit.append(dataTable)
        
        return tablesToCommit, excludedTables

#    def addSpatialMapping(self):
#        #EU
#        mappingToCountries  = dict()
#        EU_countryList = ['AUT', 'BEL', 'BGR', 'CYP', 'CZE', 'DEU', 'DNK', 'ESP', 'EST', 'FIN',
#       'FRA', 'GBR', 'GRC', 'HRV', 'HUN', 'IRL', 'ITA', 'LIE', 'LTU', 'LUX',
#       'LVA', 'MLT', 'NLD', 'POL', 'PRT', 'ROU', 'SVK', 'SVN', 'SWE']
#        self.spatialMapping.loc['Memo: European Union-28'] = 'EU28'
#        mappingToCountries['EU28'] =  EU_countryList
#        
#        LATMER_countryList = ['ABW', 'ARG', 'ATG', 'BHS', 'BLZ', 'BMU', 'BOL', 'BRA', 'BRB', 'COL',
#       'CRI', 'CUB', 'CYM', 'DMA', 'DOM', 'ECU', 'FLK', 'GLP', 'GRD', 'GTM',
#       'GUF', 'GUY', 'HND', 'HTI', 'JAM', 'KNA', 'LCA', 'MSR', 'MTQ', 'NIC',
#       'PAN', 'PER', 'PRI', 'PRY', 'SLV', 'SPM', 'SUR', 'TCA', 'TTO', 'URY',
#       'VCT', 'VEN', 'VGB']
#        self.spatialMapping.loc['Non-OECD Americas'] = 'LATAMER'
#        mappingToCountries['LATAMER'] =  LATMER_countryList
#        
#        AFRICA_countryList = ['AGO', 'BDI', 'BEN', 'BFA', 'BWA', 'CAF', 'CIV', 'CMR', 'COD', 'COG',
#       'COM', 'CPV', 'DJI', 'DZA', 'EGY', 'ERI', 'ESH', 'ETH', 'GAB', 'GHA',
#       'GIN', 'GMB', 'GNB', 'GNQ', 'KEN', 'LBR', 'LBY', 'LSO', 'MAR', 'MDG',
#       'MLI', 'MOZ', 'MRT', 'MUS', 'MWI', 'NAM', 'NER', 'NGA', 'REU', 'RWA',
#       'SDN', 'SEN', 'SLE', 'SOM', 'SSD', 'STP', 'SWZ', 'SYC', 'TCD', 'TGO',
#       'TUN', 'TZA', 'UGA', 'ZAF', 'ZMB', 'ZWE']
#        self.spatialMapping.loc['Africa'] = 'AFRICA' 
#        mappingToCountries['AFRICA'] =  AFRICA_countryList
#         
#        MIDEAST_countryList = ['ARE', 'BHR', 'IRN', 'IRQ', 'JOR', 'KWT', 'LBN', 'OMN', 'QAT', 'SAU',
#       'SYR', 'YEM']
#        self.spatialMapping.loc['Middle East'] = 'MIDEAST'
#        mappingToCountries['MIDEAST'] =  MIDEAST_countryList
#        
#        from hdx.location.country import Country
#        OECDTOT_countryList = [Country.get_iso3_country_code_fuzzy(x)[0] for x in 'Australia, Austria, Belgium, Canada, Chile, the Czech Republic, \
#         Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Iceland, \
#         Ireland, Israel, Italy, Japan, Korea, Latvia, Lithuania , Luxembourg, \
#         Mexico, the Netherlands, New Zealand, Norway, Poland, Portugal, the Slovak Republic, \
#         Slovenia, Spain, Sweden, Switzerland, Turkey, the United Kingdom, United States'.split(',')]
#         
#        self.spatialMapping.loc['Memo: OECD Total'] = 'OECDTOT'
#        mappingToCountries['OECDTOT'] =  OECDTOT_countryList
#        dt.mapp.regions.addRegionToContext('IEA',mappingToCountries)


class IEA_World_Energy_Balance(BaseImportTool):
    """
    IEA World balance data import 
    """
    def __init__(self, year = 2020):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "IEA_WEB_" + str(year)
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/IEA_WEB_' + str(year) +'/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH + 'World_Energy_Balances_' + str(year) +'_clean.csv'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        self.setup.LICENCE = 'restricted'
        self.setup.URL     = 'https://webstore.iea.org/world-energy-balances-' + str(year)
        
        self.setup.INDEX_COLUMN_NAME = ['FLOW', 'PRODUCT']
        self.setup.SPATIAL_COLUM_NAME = 'COUNTRY'
        self.setup.COLUMNS_TO_DROP = [ 'PRODUCT','FLOW','combined']
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
        else:
            self.mapping = self.loadVariableMapping()
            self.spatialMapping = self.loadSpatialMapping()

        self.createSourceMeta()


    def loadData(self):
        self.data = pd.read_csv(self.setup.DATA_FILE, encoding='utf8', engine='python', index_col = None, header =0, na_values=['x','c','..'], sep=';')
        self.data['combined'] = self.data[self.setup.INDEX_COLUMN_NAME].apply(lambda x: '_'.join(x.str.strip()), axis=1)
        
        self.data = self.data.set_index(self.data['combined'])#.drop('combined',axis=1)

    def loadSpatialMapping(self,):
        return pd.read_excel(self.setup.MAPPING_FILE, sheet_name='spatial')
    
    def loadVariableMapping(self,):
        mapping = dict()
        
        for variableName in self.setup.INDEX_COLUMN_NAME:
            mapping[variableName] = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=variableName,index_col=0)
            notNullIndex = mapping[variableName].index[~mapping[variableName].isna().mapping]
            mapping[variableName] = mapping[variableName].loc[notNullIndex]
        
        return mapping
        
    def createVariableMapping(self):        
        
        # loading data if necessary
        if not hasattr(self, 'data'):        
            self.loadData()
        
        
        import numpy as np
 
        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')       
        
        for column in self.setup.INDEX_COLUMN_NAME:
            #models
            index = self.data.loc[:,column].unique()
        
            self.availableSeries = pd.DataFrame(index=index)
            self.mapping = pd.DataFrame(index=index, columns = ['mapping'])

            self.mapping.to_excel(writer, engine='openpyxl', sheet_name=column)

        #spatial mapping
        column = self.setup.SPATIAL_COLUM_NAME
        
        index = self.data.loc[:,column].unique()
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = ['mapping'])
        
        for region in self.mapping.index:
            coISO = dt.mapp.getSpatialID(region)
            
            if coISO is not None:
                self.mapping.loc[region,'mapping'] = coISO
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='spatial')
        
        writer.close()

    def gatherMappedData(self, spatialSubSet = None, updateTables=False):
    
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        

        # meta data
#        self.loadMetaData()
        
        tablesToCommit  = []
        metaDict = dict()
        metaDict['source'] = self.setup.SOURCE_ID
        excludedTables = dict()
        excludedTables['empty'] = list()
        excludedTables['error'] = list()
        excludedTables['exists'] = list()
        
        for product in self.mapping['PRODUCT'].index:
            mask = self.data['PRODUCT'] == product
            tempDataMo = self.data.loc[mask]
            
            for flow in self.mapping['FLOW'].index:
#                metaDict['scenario'] = scenario + '|' + model
                mask = tempDataMo['FLOW'] == flow
                tempDataMoSc = tempDataMo.loc[mask]
                
                
                metaDict['entity'] = '|'.join([self.mapping['FLOW'].mapping.loc[flow],
                                              self.mapping['PRODUCT'].mapping.loc[product]])
                metaDict['scenario']  = 'Historic'
                metaDict['category']  = ''
                
                
                
                print(metaDict)
                metaDict = dt.core._update_meta(metaDict)
                tableID = dt.core._createDatabaseID(metaDict)
                
                
                for key in [ 'unit', 'unitTo']:
                    metaDict[key] = self.mapping['FLOW'].loc[flow,key]
                    
                if not updateTables:
                    if dt.core.DB.tableExist(tableID):
                        excludedTables['exists'].append(tableID)
                        continue


                    
                if len(tempDataMoSc.index) > 0:

                    dataframe = tempDataMoSc.set_index(self.setup.SPATIAL_COLUM_NAME)
                    if spatialSubSet:
                        spatIdx = dataframe[self.setup.SPATIAL_COLUM_NAME].isin(spatialSubSet)
                        dataframe = tempDataMoSc.loc[spatIdx]
                    
                    dataframe = dataframe.drop(self.setup.COLUMNS_TO_DROP, axis=1)
                    dataframe = dataframe.dropna(axis=1, how='all').astype(float)
        
                    validSpatialRegions = self.spatialMapping.index[~self.spatialMapping.mapping.isnull()]
                    dataframe = dataframe.loc[validSpatialRegions,:]
                    dataframe.index = self.spatialMapping.mapping[~self.spatialMapping.mapping.isnull()]

                    
                    dataTable = Datatable(dataframe, meta=metaDict)
                    # possible required unit conversion
                    if not pd.isna(metaDict['unitTo']):
                        dataTable = dataTable.convert(metaDict['unitTo'])
                    tablesToCommit.append(dataTable)
                else:
                    excludedTables['empty'].append(tableID)

        return tablesToCommit, excludedTables
    
class IEA_WEB_2019(BaseImportTool):
    """
    IEA World balance data import 
    """
    def __init__(self):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "IEA_WEB_2019"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/IEA_WEB_2019/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH + 'World_Energy_Balances_2019_clean.csv'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        self.setup.LICENCE = 'restricted'
        self.setup.URL     = 'https://webstore.iea.org/world-energy-balances-2019'
        
        self.setup.INDEX_COLUMN_NAME = ['FLOW', 'PRODUCT']
        self.setup.SPATIAL_COLUM_NAME = 'COUNTRY'
        self.setup.COLUMNS_TO_DROP = [ 'PRODUCT','FLOW','combined']
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
        else:
            self.mapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET)
            self.spatialMapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=SPATIAL_MAPPING_SHEET)

        self.createSourceMeta()


    def loadData(self):
        self.data = pd.read_csv(self.setup.DATA_FILE, encoding='utf8', engine='python', index_col = None, header =0, na_values=['c','..'])
        self.data['combined'] = self.data[self.setup.INDEX_COLUMN_NAME].apply(lambda x: '_'.join(x.str.strip()), axis=1)
        
        self.data = self.data.set_index(self.data['combined'])#.drop('combined',axis=1)

        
    def createVariableMapping(self):        

        productMapping = {"Coal and coal products":"Coal",
            "Peat and peat products":"Peat",
            "Oil shale and oil sands":"Oil",
            "Crude, NGL and feedstocks":"Crude_NGL_feedstocks",
            "Oil products":"Oil_products",
            "Natural gas":"Gas",
            "Nuclear":"Nuclear",
            "Hydro":"Hydro",
            "Geothermal":"Geothermal",
            "Solar/wind/other":"Solar_wind_other",
            "Biofuels and waste":"Bio_fuel_waste",
            "Heat production from non-specified combustible fuels":"Heat_non_spec_combustible_fuels",
            "Electricity":"Electricity",
            "Heat":"Heat",
            "Total":"Total energy",
            "Memo: Renewables":"renewables",
            "Memo: Coal, peat and oil shale":"coal_peat_oil",
            "Memo: Primary and secondary oil":"1st_2nd_oil",
            "Memo: Geothermal, solar/wind/other, heat, electricity":"geo_solar_wind_other_heat_electrity"}
        
        flowMapping = {
                "Production":"Production",
                "Imports":"Imports",
                "Exports":"Exports",
                "International marine bunkers":"Marine_bunkers",
                "International aviation bunkers":"Aviation_bunkers",
                "Stock changes":"Stock_changes",
                "Total primary energy supply":"Total_PE_supply",
                "Transfers":"Transfers",
#                Statistical differences
#                Main activity producer electricity plants (transf.)
#                Autoproducer electricity plants (transf.)
#                Main activity producer CHP plants (transf.)
#                Autoproducer CHP plants (transf.)
#                Main activity producer heat plants (transf.)
#                Autoproducer heat plants (transf.)
#                Heat pumps (transf.)
#                Electric boilers (transf.)
#                Chemical heat for electricity production (transf.)
#                Blast furnaces (transf.)
#                Gas works (transf.)
#                Coke ovens (transf.)
#                Patent fuel plants (transf.)
#                BKB/peat briquette plants (transf.)
#                Oil refineries (transf.)
#                Petrochemical plants (transf.)
#                Liquefaction plants (transf.)
#                Other transformation
#                Energy industry own use
                "Losses":"Losses",
                "Total final consumption":"Total_consumption",
#                Industry
#                Iron and steel
#                Chemical and petrochemical
#                Non-ferrous metals
#                Non-metallic minerals
#                Transport equipment
#                Machinery
#                Mining and quarrying
#                Food and tobacco
#                Paper, pulp and printing 
#                Wood and wood products
#                Construction
#                Textile and leather
#                Non-specified (industry)
#                Transport
#                World aviation bunkers
                "Domestic aviation":"Domestic_aviation",
                "Road": "Tranpsport|Road", 
                "Rail": "Tranpsport|Rail",
#                Pipeline transport
#                World marine bunkers
                "Domestic navigation":"Domestic_marine",
#                Non-specified (transport)
#                Other
#                Residential
#                Commercial and public services
#                Agriculture/forestry
#                Fishing
#                Non-specified (other)
#                Non-energy use
#                Non-energy use industry/transformation/energy
#                Non-energy use in transport
#                Non-energy use in other
#                   Memo: Non-energy use in industry
#                   Memo: Non-energy use in iron and steel
#                   Memo: Non-energy use in chemical/petrochemical
#                   Memo: Non-energy use in non-ferrous metals
#                   Memo: Non-energy use in non-metallic minerals
#                   Memo: Non-energy use in transport equipment
#                   Memo: Non-energy use in machinery
#                   Memo: Non-energy use in mining and quarrying
#                   Memo: Non-energy use in food/beverages/tobacco
#                   Memo: Non-energy use in paper/pulp and printing
#                   Memo: Non-energy use in wood and wood products
#                   Memo: Non-energy use in construction
#                   Memo: Non-energy use in textiles and leather
#                   Memo: Non-energy use in non-specified industry
                "Electricity output (GWh)":"Electricity_output",
#                Electricity output (GWh)-main activity producer electricity plants
#                Electricity output (GWh)-autoproducer electricity plants
#                Electricity output (GWh)-main activity producer CHP plants
#                Electricity output (GWh)-autoproducer CHP plants
                "Heat output":"Heat_output",
#                Heat output-main activity producer CHP plants
#                Heat output-autoproducer CHP plants
#                Heat output-main activity producer heat plants
#                Heat output-autoproducer heat plants
#                 Memo: Efficiency of electricity only plants (main and auto) (%)
#                 Memo: Efficiency of electricity and heat plants (%)                
                }

        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')                
                
        #%%
        
        if not hasattr(self, 'data'):
#            self.data = pd.read_csv(self.setup.DATA_FILE, encoding='utf8', engine='python', index_col = None, header =0, na_values='..')
#            self.data['combined'] = self.data[self.setup.INDEX_COLUMN_NAME].apply(lambda x: '_'.join(x), axis=1)
            self.loadData()
            
        index = self.data['combined'].unique()

        #%%
        # spatial mapping
        self.spatialMapping = dict()
        spatialIDList = self.data[self.setup.SPATIAL_COLUM_NAME].unique()
        for spatID in spatialIDList:
            ISO_ID = dt.mapp.getSpatialID(spatID)
            if ISO_ID is not None:
                self.spatialMapping[spatID] = ISO_ID
            else:
                print('not found: ' + spatID)
                
        # adding regions
        self.spatialMapping['World'] = "World"
        
        dataFrame = pd.DataFrame(data=[],columns = ['alternative'])
        for key, item in self.spatialMapping.items():
            dataFrame.loc[key] = item
        dataFrame.to_excel(writer, sheet_name=SPATIAL_MAPPING_SHEET)
        
        #%%
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = MAPPING_COLUMNS)
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        self.mapping.scenario = 'historic'
        
        self.mapping['flow'] = self.mapping.index
        self.mapping['flow'] = self.mapping['flow'].apply(lambda x: x[0:x.rfind('_')])
        self.mapping['product'] = self.mapping.index
        self.mapping['product'] = self.mapping['product'].apply(lambda x: x[x.rfind('_')+1:])        
        
        for key, value in flowMapping.items():
            mask = self.mapping['flow'].str.match(key)
            for pKey, pValue in productMapping.items():
                pMask = self.mapping['product'].str.match(pKey)
                self.mapping['entity'][mask&pMask] = '_'.join([value, pValue])
                if 'GWh' in key:
                    self.mapping['unit'][mask&pMask] = 'GWh'
                else:
                    self.mapping['unit'][mask&pMask] = 'TJ'
                
        #self.mapping = self.mapping.drop(['product','flow'],axis=1)
        self.mapping.to_excel(writer, sheet_name=VAR_MAPPING_SHEET)
        writer.close() 
    
    def gatherMappedData(self, spatialSubSet = None, updateTables = False):
        
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
        
        indexDataToCollect = self.mapping.index[~pd.isnull(self.mapping['entity'])]
        
        tablesToCommit  = []
        excludedTables = dict()
        excludedTables['empty'] = list()
        excludedTables['error'] = list()
        excludedTables['exists'] = list()
        for idx in indexDataToCollect:
            metaDf = self.mapping.loc[idx]
            print(idx)
            
            #print(metaDf[config.REQUIRED_META_FIELDS].isnull().all() == False)
            #print(metaData[self.setup.INDEX_COLUMN_NAME])
            
            #print(metaDf)
            metaDict = {key : metaDf[key] for key in config.REQUIRED_META_FIELDS.union({'unitTo'})} 
            #print(metaDict)
            if pd.isnull(metaDict['category']):
                metaDict['category'] = ''
            metaDict['original code'] = idx
            #metaDict['original name'] = metaDf['Indicator Name']
            
            seriesIdx = idx
            
            print(metaDict)
            
            if not updateTables:
                tableID = dt.core._createDatabaseID(metaDict)
                print(tableID)
                if not updateTables:
                    if dt.core.DB.tableExist(tableID):
                        excludedTables['exists'].append(tableID)
                        continue
            
            try:
                dataframe = self.data.loc[seriesIdx]
            except:
                print(seriesIdx)
#                dsf
            newData= list()
            for iRow in range(len(dataframe)):
                if dataframe.COUNTRY.iloc[iRow] in self.spatialMapping.index:
                    newData.append(self.spatialMapping.alternative.loc[dataframe.COUNTRY.iloc[iRow]])
                else:
                    newData.append(pd.np.nan)
            dataframe.loc[:,'COUNTRY'] = newData
           
            if spatialSubSet:
                spatIdx = dataframe[self.setup.SPATIAL_COLUM_NAME].isin(spatialSubSet)
                dataframe = dataframe.loc[spatIdx]
            
            dataframe = dataframe.set_index(self.setup.SPATIAL_COLUM_NAME).drop(self.setup.COLUMNS_TO_DROP, axis=1)
            
            dataframe= dataframe.dropna(axis=1, how='all')
            dataframe= dataframe.loc[~pd.isna(dataframe.index)]
            dataTable = Datatable(dataframe, meta=metaDict)
            
            if not pd.isna(metaDict['unitTo']):
                dataTable = dataTable.convert(metaDict['unitTo'])
                
            tablesToCommit.append(dataTable)
        
        return tablesToCommit, excludedTables

    def addSpatialMapping(self):
        #EU
        mappingToCountries  = dict()
        EU_countryList = ['AUT', 'BEL', 'BGR', 'CYP', 'CZE', 'DEU', 'DNK', 'ESP', 'EST', 'FIN',
       'FRA', 'GBR', 'GRC', 'HRV', 'HUN', 'IRL', 'ITA', 'LIE', 'LTU', 'LUX',
       'LVA', 'MLT', 'NLD', 'POL', 'PRT', 'ROU', 'SVK', 'SVN', 'SWE']
        self.spatialMapping.loc['Memo: European Union-28'] = 'EU28'
        mappingToCountries['EU28'] =  EU_countryList
        
        LATMER_countryList = ['ABW', 'ARG', 'ATG', 'BHS', 'BLZ', 'BMU', 'BOL', 'BRA', 'BRB', 'COL',
       'CRI', 'CUB', 'CYM', 'DMA', 'DOM', 'ECU', 'FLK', 'GLP', 'GRD', 'GTM',
       'GUF', 'GUY', 'HND', 'HTI', 'JAM', 'KNA', 'LCA', 'MSR', 'MTQ', 'NIC',
       'PAN', 'PER', 'PRI', 'PRY', 'SLV', 'SPM', 'SUR', 'TCA', 'TTO', 'URY',
       'VCT', 'VEN', 'VGB']
        self.spatialMapping.loc['Non-OECD Americas'] = 'LATAMER'
        mappingToCountries['LATAMER'] =  LATMER_countryList
        
        AFRICA_countryList = ['AGO', 'BDI', 'BEN', 'BFA', 'BWA', 'CAF', 'CIV', 'CMR', 'COD', 'COG',
       'COM', 'CPV', 'DJI', 'DZA', 'EGY', 'ERI', 'ESH', 'ETH', 'GAB', 'GHA',
       'GIN', 'GMB', 'GNB', 'GNQ', 'KEN', 'LBR', 'LBY', 'LSO', 'MAR', 'MDG',
       'MLI', 'MOZ', 'MRT', 'MUS', 'MWI', 'NAM', 'NER', 'NGA', 'REU', 'RWA',
       'SDN', 'SEN', 'SLE', 'SOM', 'SSD', 'STP', 'SWZ', 'SYC', 'TCD', 'TGO',
       'TUN', 'TZA', 'UGA', 'ZAF', 'ZMB', 'ZWE']
        self.spatialMapping.loc['Africa'] = 'AFRICA' 
        mappingToCountries['AFRICA'] =  AFRICA_countryList
         
        MIDEAST_countryList = ['ARE', 'BHR', 'IRN', 'IRQ', 'JOR', 'KWT', 'LBN', 'OMN', 'QAT', 'SAU',
       'SYR', 'YEM']
        self.spatialMapping.loc['Middle East'] = 'MIDEAST'
        mappingToCountries['MIDEAST'] =  MIDEAST_countryList
        
        from hdx.location.country import Country
        OECDTOT_countryList = [Country.get_iso3_country_code_fuzzy(x)[0] for x in 'Australia, Austria, Belgium, Canada, Chile, the Czech Republic, \
         Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Iceland, \
         Ireland, Israel, Italy, Japan, Korea, Latvia, Lithuania , Luxembourg, \
         Mexico, the Netherlands, New Zealand, Norway, Poland, Portugal, the Slovak Republic, \
         Slovenia, Spain, Sweden, Switzerland, Turkey, the United Kingdom, United States'.split(',')]
         
        self.spatialMapping.loc['Memo: OECD Total'] = 'OECDTOT'
        mappingToCountries['OECDTOT'] =  OECDTOT_countryList
        dt.mapp.regions.addRegionToContext('IEA',mappingToCountries)


class IEA_WEB_2018(BaseImportTool):
    """
    IEA World balance data import 
    """
    def __init__(self):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "IEA_WEB_2018"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/IEA_WEB_2018/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH + 'World_Energy_Balances_2018_clean.csv'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        self.setup.LICENCE = 'restricted'
        self.setup.URL     = 'https://webstore.iea.org/world-energy-balances-2018'
        
        self.setup.INDEX_COLUMN_NAME = ['FLOW', 'PRODUCT']
        self.setup.SPATIAL_COLUM_NAME = 'COUNTRY'
        self.setup.COLUMNS_TO_DROP = [ 'PRODUCT','FLOW','combined']
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
        else:
            self.mapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET)
            self.spatialMapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=SPATIAL_MAPPING_SHEET)

        self.createSourceMeta()


    def loadData(self):
        self.data = pd.read_csv(self.setup.DATA_FILE, encoding='utf8', engine='python', index_col = None, header =0, na_values='c')
        self.data['combined'] = self.data[self.setup.INDEX_COLUMN_NAME].apply(lambda x: '_'.join(x), axis=1)
        
        self.data = self.data.set_index(self.data['combined'])#.drop('combined',axis=1)

        
    def createVariableMapping(self):        

        productMapping = {"Coal and coal products":"Coal",
            "Peat and peat products":"Peat",
            "Oil shale and oil sands":"Oil",
            "Crude, NGL and feedstocks":"Crude_NGL_feedstocks",
            "Oil products":"Oil_products",
            "Natural gas":"Gas",
            "Nuclear":"Nuclear",
            "Hydro":"Hydro",
            "Geothermal":"Geothermal",
            "Solar/wind/other":"Solar_wind_other",
            "Biofuels and waste":"Bio_fuel_waste",
            "Heat production from non-specified combustible fuels":"Heat_non_spec_combustible_fuels",
            "Electricity":"Electricity",
            "Heat":"Heat",
            "Total":"Total energy",
            "Memo: Renewables":"renewables",
            "Memo: Coal, peat and oil shale":"coal_peat_oil",
            "Memo: Primary and secondary oil":"1st_2nd_oil",
            "Memo: Geothermal, solar/wind/other, heat, electricity":"geo_solar_wind_other_heat_electrity"}
        
        flowMapping = {
                "Production":"Production",
                "Imports":"Imports",
                "Exports":"Exports",
                "International marine bunkers":"Marine_bunkers",
                "International aviation bunkers":"Aviation_bunkers",
                "Stock changes":"Stock_changes",
                "Total primary energy supply":"Total_PE_supply",
                "Transfers":"Transfers",
#                Statistical differences
#                Main activity producer electricity plants (transf.)
#                Autoproducer electricity plants (transf.)
#                Main activity producer CHP plants (transf.)
#                Autoproducer CHP plants (transf.)
#                Main activity producer heat plants (transf.)
#                Autoproducer heat plants (transf.)
#                Heat pumps (transf.)
#                Electric boilers (transf.)
#                Chemical heat for electricity production (transf.)
#                Blast furnaces (transf.)
#                Gas works (transf.)
#                Coke ovens (transf.)
#                Patent fuel plants (transf.)
#                BKB/peat briquette plants (transf.)
#                Oil refineries (transf.)
#                Petrochemical plants (transf.)
#                Liquefaction plants (transf.)
#                Other transformation
#                Energy industry own use
                "Losses":"Losses",
                "Total final consumption":"Total_consumption",
#                Industry
#                Iron and steel
#                Chemical and petrochemical
#                Non-ferrous metals
#                Non-metallic minerals
#                Transport equipment
#                Machinery
#                Mining and quarrying
#                Food and tobacco
#                Paper, pulp and printing 
#                Wood and wood products
#                Construction
#                Textile and leather
#                Non-specified (industry)
#                Transport
#                World aviation bunkers
                "Domestic aviation":"Domestic_aviation",
#                Road
#                Rail
#                Pipeline transport
#                World marine bunkers
                "Domestic navigation":"Domestic_marine",
#                Non-specified (transport)
#                Other
#                Residential
#                Commercial and public services
#                Agriculture/forestry
#                Fishing
#                Non-specified (other)
#                Non-energy use
#                Non-energy use industry/transformation/energy
#                Non-energy use in transport
#                Non-energy use in other
#                   Memo: Non-energy use in industry
#                   Memo: Non-energy use in iron and steel
#                   Memo: Non-energy use in chemical/petrochemical
#                   Memo: Non-energy use in non-ferrous metals
#                   Memo: Non-energy use in non-metallic minerals
#                   Memo: Non-energy use in transport equipment
#                   Memo: Non-energy use in machinery
#                   Memo: Non-energy use in mining and quarrying
#                   Memo: Non-energy use in food/beverages/tobacco
#                   Memo: Non-energy use in paper/pulp and printing
#                   Memo: Non-energy use in wood and wood products
#                   Memo: Non-energy use in construction
#                   Memo: Non-energy use in textiles and leather
#                   Memo: Non-energy use in non-specified industry
                "Electricity output (GWh)":"Electricity_output",
#                Electricity output (GWh)-main activity producer electricity plants
#                Electricity output (GWh)-autoproducer electricity plants
#                Electricity output (GWh)-main activity producer CHP plants
#                Electricity output (GWh)-autoproducer CHP plants
                "Heat output":"Heat_output",
#                Heat output-main activity producer CHP plants
#                Heat output-autoproducer CHP plants
#                Heat output-main activity producer heat plants
#                Heat output-autoproducer heat plants
#                 Memo: Efficiency of electricity only plants (main and auto) (%)
#                 Memo: Efficiency of electricity and heat plants (%)                
                }

        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')                
                
        #%%
        
        if not hasattr(self, 'data'):
#            self.data = pd.read_csv(self.setup.DATA_FILE, encoding='utf8', engine='python', index_col = None, header =0, na_values='..')
#            self.data['combined'] = self.data[self.setup.INDEX_COLUMN_NAME].apply(lambda x: '_'.join(x), axis=1)
            self.loadData()
            
        index = self.data['combined'].unique()

        #%%
        # spatial mapping
        self.spatialMapping = dict()
        spatialIDList = self.data[self.setup.SPATIAL_COLUM_NAME].unique()
        for spatID in spatialIDList:
            ISO_ID = dt.mapp.getSpatialID(spatID)
            if ISO_ID is not None:
                self.spatialMapping[spatID] = ISO_ID
            else:
                print('not found: ' + spatID)
                
        # adding regions
        self.spatialMapping['World'] = "World"
        
        dataFrame = pd.DataFrame(data=[],columns = ['alternative'])
        for key, item in self.spatialMapping.items():
            dataFrame.loc[key] = item
        dataFrame.to_excel(writer, sheet_name=SPATIAL_MAPPING_SHEET)
        
        #%%
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = MAPPING_COLUMNS)
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        self.mapping.scenario = 'historic'
        
        self.mapping['flow'] = self.mapping.index
        self.mapping['flow'] = self.mapping['flow'].apply(lambda x: x[0:x.rfind('_')])
        self.mapping['product'] = self.mapping.index
        self.mapping['product'] = self.mapping['product'].apply(lambda x: x[x.rfind('_')+1:])        
        
        for key, value in flowMapping.items():
            mask = self.mapping['flow'].str.match(key)
            for pKey, pValue in productMapping.items():
                pMask = self.mapping['product'].str.match(pKey)
                self.mapping['entity'][mask&pMask] = '_'.join([value, pValue])
                if 'GWh' in key:
                    self.mapping['unit'][mask&pMask] = 'GWh'
                else:
                    self.mapping['unit'][mask&pMask] = 'TJ'
                
        #self.mapping = self.mapping.drop(['product','flow'],axis=1)
        self.mapping.to_excel(writer, sheet_name=VAR_MAPPING_SHEET)
        writer.close() 
    
    def gatherMappedData(self, spatialSubSet = None, updateTables = False):
        
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
        
        indexDataToCollect = self.mapping.index[~pd.isnull(self.mapping['entity'])]
        
        tablesToCommit  = []
        excludedTables = dict()
        excludedTables['empty'] = list()
        excludedTables['erro'] = list()
        excludedTables['exists'] = list()
        for idx in indexDataToCollect:
            metaDf = self.mapping.loc[idx]
            print(idx)
            
            #print(metaDf[config.REQUIRED_META_FIELDS].isnull().all() == False)
            #print(metaData[self.setup.INDEX_COLUMN_NAME])
            
            #print(metaDf)
            metaDict = {key : metaDf[key] for key in config.REQUIRED_META_FIELDS.union({'unitTo'})} 
            #print(metaDict)
            if pd.isnull(metaDict['category']):
                metaDict['category'] = ''
            metaDict['original code'] = idx
            #metaDict['original name'] = metaDf['Indicator Name']
            
            seriesIdx = idx
            
            print(metaDict)
            
            if not updateTables:
                tableID = dt.core._createDatabaseID(metaDict)
                print(tableID)
                if not updateTables:
                    if dt.core.DB.tableExist(tableID):
                        excludedTables['exists'].append(tableID)
                        continue
            
            try:
                dataframe = self.data.loc[seriesIdx]
            except:
                print(seriesIdx)
                dsf
            newData= list()
            for iRow in range(len(dataframe)):
                if dataframe.COUNTRY.iloc[iRow] in self.spatialMapping.index:
                    newData.append(self.spatialMapping.alternative.loc[dataframe.COUNTRY.iloc[iRow]])
                else:
                    newData.append(pd.np.nan)
            dataframe.loc[:,'COUNTRY'] = newData
           
            if spatialSubSet:
                spatIdx = dataframe[self.setup.SPATIAL_COLUM_NAME].isin(spatialSubSet)
                dataframe = dataframe.loc[spatIdx]
            
            dataframe = dataframe.set_index(self.setup.SPATIAL_COLUM_NAME).drop(self.setup.COLUMNS_TO_DROP, axis=1)
            
            dataframe= dataframe.dropna(axis=1, how='all')
            dataframe= dataframe.loc[~pd.isna(dataframe.index)]
            dataTable = Datatable(dataframe, meta=metaDict)
            
            if not pd.isna(metaDict['unitTo']):
                dataTable = dataTable.convert(metaDict['unitTo'])
                
            tablesToCommit.append(dataTable)
        
        return tablesToCommit, excludedTables

    def addSpatialMapping(self):
        #EU
        mappingToCountries  = dict()
        EU_countryList = ['AUT', 'BEL', 'BGR', 'CYP', 'CZE', 'DEU', 'DNK', 'ESP', 'EST', 'FIN',
       'FRA', 'GBR', 'GRC', 'HRV', 'HUN', 'IRL', 'ITA', 'LIE', 'LTU', 'LUX',
       'LVA', 'MLT', 'NLD', 'POL', 'PRT', 'ROU', 'SVK', 'SVN', 'SWE']
        self.spatialMapping.loc['Memo: European Union-28'] = 'EU28'
        mappingToCountries['EU28'] =  EU_countryList
        
        LATMER_countryList = ['ABW', 'ARG', 'ATG', 'BHS', 'BLZ', 'BMU', 'BOL', 'BRA', 'BRB', 'COL',
       'CRI', 'CUB', 'CYM', 'DMA', 'DOM', 'ECU', 'FLK', 'GLP', 'GRD', 'GTM',
       'GUF', 'GUY', 'HND', 'HTI', 'JAM', 'KNA', 'LCA', 'MSR', 'MTQ', 'NIC',
       'PAN', 'PER', 'PRI', 'PRY', 'SLV', 'SPM', 'SUR', 'TCA', 'TTO', 'URY',
       'VCT', 'VEN', 'VGB']
        self.spatialMapping.loc['Non-OECD Americas'] = 'LATAMER'
        mappingToCountries['LATAMER'] =  LATMER_countryList
        
        AFRICA_countryList = ['AGO', 'BDI', 'BEN', 'BFA', 'BWA', 'CAF', 'CIV', 'CMR', 'COD', 'COG',
       'COM', 'CPV', 'DJI', 'DZA', 'EGY', 'ERI', 'ESH', 'ETH', 'GAB', 'GHA',
       'GIN', 'GMB', 'GNB', 'GNQ', 'KEN', 'LBR', 'LBY', 'LSO', 'MAR', 'MDG',
       'MLI', 'MOZ', 'MRT', 'MUS', 'MWI', 'NAM', 'NER', 'NGA', 'REU', 'RWA',
       'SDN', 'SEN', 'SLE', 'SOM', 'SSD', 'STP', 'SWZ', 'SYC', 'TCD', 'TGO',
       'TUN', 'TZA', 'UGA', 'ZAF', 'ZMB', 'ZWE']
        self.spatialMapping.loc['Africa'] = 'AFRICA' 
        mappingToCountries['AFRICA'] =  AFRICA_countryList
         
        MIDEAST_countryList = ['ARE', 'BHR', 'IRN', 'IRQ', 'JOR', 'KWT', 'LBN', 'OMN', 'QAT', 'SAU',
       'SYR', 'YEM']
        self.spatialMapping.loc['Middle East'] = 'MIDEAST'
        mappingToCountries['MIDEAST'] =  MIDEAST_countryList
        
        from hdx.location.country import Country
        OECDTOT_countryList = [Country.get_iso3_country_code_fuzzy(x)[0] for x in 'Australia, Austria, Belgium, Canada, Chile, the Czech Republic, \
         Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Iceland, \
         Ireland, Israel, Italy, Japan, Korea, Latvia, Lithuania , Luxembourg, \
         Mexico, the Netherlands, New Zealand, Norway, Poland, Portugal, the Slovak Republic, \
         Slovenia, Spain, Sweden, Switzerland, Turkey, the United Kingdom, United States'.split(',')]
         
        self.spatialMapping.loc['Memo: OECD Total'] = 'OECDTOT'
        mappingToCountries['OECDTOT'] =  OECDTOT_countryList
        dt.mapp.regions.addRegionToContext('IEA',mappingToCountries)


class IEA2016():

    def __init__(self):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "IEA2016"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/IEA2016/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH + 'IEA2016_energy_balance.csv'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        self.setup.LICENCE = 'restricted'
        self.setup.URL     = 'https://webstore.iea.org/world-energy-balances-2018'
        
        self.setup.INDEX_COLUMN_NAME = ['FLOW', 'PRODUCT']
        self.setup.SPATIAL_COLUM_NAME = 'COUNTRY'
        self.setup.COLUMNS_TO_DROP = ['FLOW', 'PRODUCT']
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
        else:
            self.mapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET)
    
    def loadData(self):
        self.data = pd.read_csv(self.setup.DATA_FILE, encoding="ISO-8859-1", engine='python', index_col = None, header =0, na_values='x')
        self.data['combined'] = self.data[self.setup.INDEX_COLUMN_NAME].apply(lambda x: '_'.join(x), axis=1)
        
        self.data = self.data.set_index(self.data['combined']).drop('combined',axis=1)
        
    def createVariableMapping(self):        

        if not hasattr(self, 'data'):
            self.loadData()            
        
        
        
        index = self.data['combined'].unique()
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = list(config.ID_FIELDS) + ['unitTo'])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        self.mapping.scenario = 'historic'
        
        self.mapping.to_excel(self.setup.MAPPING_FILE, engine='openpyxl', sheet_name=VAR_MAPPING_SHEET)

    def gatherMappedData(self, spatialSubSet = None):
        
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
        
        indexDataToCollect = self.mapping.index[~pd.isnull(self.mapping['entity'])]
        
        tablesToCommit  = []
        for idx in indexDataToCollect:
            metaDf = self.mapping.loc[idx]
            print(idx)
            
            print(metaDf[config.REQUIRED_META_FIELDS].isnull().all() == False)
            #print(metaData[self.setup.INDEX_COLUMN_NAME])
            
            
            metaDict = {key : metaDf[key] for key in config.REQUIRED_META_FIELDS.union({'unitTo'})}
            
            seriesIdx = idx
            
            dataframe = self.data.loc[seriesIdx]
            
            if spatialSubSet:
                spatIdx = dataframe[self.setup.SPATIAL_COLUM_NAME].isin(spatialSubSet)
                dataframe = dataframe.loc[spatIdx]
            
            dataframe = dataframe.set_index(self.setup.SPATIAL_COLUM_NAME).drop(self.setup.COLUMNS_TO_DROP, axis=1)
            dataframe= dataframe.dropna(axis=1, how='all')
            
            dataTable = Datatable(dataframe, meta=metaDict)

            if not pd.isna(metaDict['unitTo']):
                dataTable = dataTable.convert(metaDict['unitTo'])
                
            tablesToCommit.append(dataTable)
        
        return tablesToCommit



        
class ADVANCE_DB(BaseImportTool):
    
    def __init__(self):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "ADVANCE_2016"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/ADVANCE_DB/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH + 'ADVANCE_Synthesis_version101_compare_20190619-143200.csv'
        #self.setup.META_FILE    = self.setup.SOURCE_PATH + 'sr15_metadata_indicators_r1.1.xlsx'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        
        
        self.setup.LICENCE = ' CC-BY 4.0'
        self.setup.URL     = 'https://db1.ene.iiasa.ac.at/ADVANCEDB/dsd?Action=htmlpage&page=about'
        
        self.setup.VARIABLE_COLUMN_NAME = ['VARIABLE']
        self.setup.MODEL_COLUMN_NAME = ['MODEL']
        self.setup.SCENARIO_COLUMN_NAME = ['SCENARIO']

        self.setup.SPATIAL_COLUM_NAME = ['REGION']
        self.setup.COLUMNS_TO_DROP = ["MODEL","SCENARIO","VARIABLE","UNIT"]
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
        else:
            self.loadMapping()

    def loadMapping(self,):
        self.mappingEntity = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET,index_col=0)
        self.mappingEntity = self.mappingEntity.loc[self.mappingEntity.entity.notnull()]
        
        self.mappingModel = pd.read_excel(self.setup.MAPPING_FILE, sheet_name='model_mapping').set_index('model') 
        self.mappingModel = self.mappingModel.loc[self.mappingModel.index.notnull()]
        
        self.mappingScenario = pd.read_excel(self.setup.MAPPING_FILE, sheet_name='scenario_mapping').set_index('scenario') 
        self.mappingScenario = self.mappingScenario.loc[self.mappingScenario.index.notnull()]
            
    def createVariableMapping(self):
        # loading data if necessary
        if not hasattr(self, 'data'):        
            self.loadData()
        
        
        import numpy as np
 
        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')       
        
        #variables
        #index = self.data[self.setup.VARIABLE_COLUMN_NAME].unique()
        self.availableSeries = self.data.drop_duplicates(self.setup.VARIABLE_COLUMN_NAME).set_index(self.setup.VARIABLE_COLUMN_NAME)
        self.mapping = pd.DataFrame(index=self.availableSeries.index, columns = MAPPING_COLUMNS)
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        self.mapping = self.mapping.sort_index()
        self.mapping = self.mapping.loc[:,MAPPING_COLUMNS]
        self.mapping.unit = self.availableSeries.UNIT
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name=VAR_MAPPING_SHEET, index_label="original variable")
        
        #models
        index = np.unique(self.data[self.setup.MODEL_COLUMN_NAME].values)
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = self.setup.MODEL_COLUMN_NAME)
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='model_mapping', index_label="original model")

        # scenarios
        index = np.unique(self.data[self.setup.SCENARIO_COLUMN_NAME].values)
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = self.setup.SCENARIO_COLUMN_NAME)
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        
        
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='scenario_mapping', index_label="original scenario")
        writer.close()

    def loadData(self):
        self.data = pd.read_csv(self.setup.DATA_FILE, index_col = None, header =0)
        
    def gatherMappedData(self, spatialSubSet = None, updateTables=False):
    
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
        self.createSourceMeta()
#        # meta data
#        self.loadMetaData()
        
        tablesToCommit  = []
        metaDict = dict()
        metaDict['source'] = self.setup.SOURCE_ID
        excludedTables = dict()
        excludedTables['empty'] = list()
        excludedTables['erro'] = list()
        excludedTables['exists'] = list()
        for model in self.mappingModel.index:
            mask = self.data['MODEL'] == self.mappingModel.loc[model]['original_model']
            tempDataMo = self.data.loc[mask]
            
            for scenario in self.mappingScenario.index:
                metaDict['scenario'] = scenario + '|' + model
                mask = tempDataMo['SCENARIO'] == self.mappingScenario.loc[scenario]['original_scenario']
                tempDataMoSc = tempDataMo.loc[mask]
                
                
                for entity in self.mappingEntity.index:
                    metaDf =  self.mappingEntity.loc[entity]
                    metaDict['entity'] = self.mappingEntity.loc[entity]['entity']
                    metaDict['model']  = model
                    
                    for key in [ 'category', 'unit', 'unitTo']:
                        metaDict[key] = metaDf[key]
                    if pd.isnull(metaDict['category']):
                        metaDict['category'] = ''
                    tableID = dt.core._createDatabaseID(metaDict)
                    print(tableID)
                    if not updateTables:
                        if dt.core.DB.tableExist(tableID):
                            excludedTables['exists'].append(tableID)
                            continue

                    mask = tempDataMoSc['VARIABLE'] == entity
                    tempDataMoScEn = tempDataMoSc.loc[mask]

                    if len(tempDataMoScEn.index) > 0:

                        dataframe = tempDataMoScEn.set_index(self.setup.SPATIAL_COLUM_NAME)
                        if spatialSubSet:
                            spatIdx = dataframe[self.setup.SPATIAL_COLUM_NAME].isin(spatialSubSet)
                            dataframe = tempDataMoScEn.loc[spatIdx]
                        
                        dataframe = dataframe.drop(self.setup.COLUMNS_TO_DROP, axis=1)
                        dataframe = dataframe.dropna(axis=1, how='all').astype(float)
            
                        
                        dataTable = Datatable(dataframe, meta=metaDict)
                            
                    
                        # possible required unit conversion
                        if not pd.isna(metaDict['unitTo']):
                            dataTable = dataTable.convert(metaDict['unitTo'])
                            
                        tablesToCommit.append(dataTable)
                    else:
                        excludedTables['empty'].append(tableID)

        return tablesToCommit, excludedTables

class AR5_DATABASE(BaseImportTool):
    
    def __init__(self):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "AR5_DB"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/AR5_database/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH + 'ar5_public_version102_compare_compare_20150629-130000.csv'
        #self.setup.META_FILE    = self.setup.SOURCE_PATH + 'sr15_metadata_indicators_r1.1.xlsx'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        
        
        self.setup.LICENCE = ' CC-BY 4.0'
        self.setup.URL     = 'https://db1.ene.iiasa.ac.at/ADVANCEDB/dsd?Action=htmlpage&page=about'
        
        self.setup.VARIABLE_COLUMN_NAME = ['VARIABLE']
        self.setup.MODEL_COLUMN_NAME = ['MODEL']
        self.setup.SCENARIO_COLUMN_NAME = ['SCENARIO']

        self.setup.SPATIAL_COLUM_NAME = ['REGION']
        self.setup.COLUMNS_TO_DROP = ["MODEL","SCENARIO","VARIABLE","UNIT"]
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
        else:
            self.loadMapping()

    def loadMapping(self,):
        self.mappingEntity = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET,index_col=0)
        self.mappingEntity = self.mappingEntity.loc[self.mappingEntity.entity.notnull()]
        
        self.mappingModel = pd.read_excel(self.setup.MAPPING_FILE, sheet_name='model_mapping').set_index('model') 
        self.mappingModel = self.mappingModel.loc[self.mappingModel.index.notnull()]
        
        self.mappingScenario = pd.read_excel(self.setup.MAPPING_FILE, sheet_name='scenario_mapping').set_index('scenario') 
        self.mappingScenario = self.mappingScenario.loc[self.mappingScenario.index.notnull()]
            
    def createVariableMapping(self):
        # loading data if necessary
        if not hasattr(self, 'data'):        
            self.loadData()
        
        
        import numpy as np
 
        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')       
        
        #variables
        #index = self.data[self.setup.VARIABLE_COLUMN_NAME].unique()
        self.availableSeries = self.data.drop_duplicates(self.setup.VARIABLE_COLUMN_NAME).set_index(self.setup.VARIABLE_COLUMN_NAME)
        self.mapping = pd.DataFrame(index=self.availableSeries.index, columns = MAPPING_COLUMNS)
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        self.mapping = self.mapping.sort_index()
        self.mapping = self.mapping.loc[:,MAPPING_COLUMNS]
        self.mapping.unit = self.availableSeries.UNIT
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name=VAR_MAPPING_SHEET, index_label="original variable")
        
        #models
        index = np.unique(self.data[self.setup.MODEL_COLUMN_NAME].values)
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = self.setup.MODEL_COLUMN_NAME)
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='model_mapping', index_label="original model")

        # scenarios
        index = np.unique(self.data[self.setup.SCENARIO_COLUMN_NAME].values)
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = self.setup.SCENARIO_COLUMN_NAME)
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        
        
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='scenario_mapping', index_label="original scenario")
        writer.close()

    def loadData(self):
        self.data = pd.read_csv(self.setup.DATA_FILE, index_col = None, header =0)
        
    def gatherMappedData(self, spatialSubSet = None, updateTables=False):
    
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
        self.createSourceMeta()
#        # meta data
#        self.loadMetaData()
        
        tablesToCommit  = []
        metaDict = dict()
        metaDict['source'] = self.setup.SOURCE_ID
        excludedTables = dict()
        excludedTables['empty'] = list()
        excludedTables['erro'] = list()
        excludedTables['exists'] = list()
        for model in self.mappingModel.index:
            mask = self.data['MODEL'] == self.mappingModel.loc[model]['original_model']
            tempDataMo = self.data.loc[mask]
            
            for scenario in self.mappingScenario.index:
                metaDict['scenario'] = scenario + '|' + model
                mask = tempDataMo['SCENARIO'] == self.mappingScenario.loc[scenario]['original_scenario']
                tempDataMoSc = tempDataMo.loc[mask]
                
                
                for entity in self.mappingEntity.index:
                    metaDf =  self.mappingEntity.loc[entity]
                    metaDict['entity'] = self.mappingEntity.loc[entity]['entity']
                    metaDict['model']  = model
                    metaDict['unitTo'] = self.mappingEntity.loc[entity]['unitTo']
                    
                    for key in [ 'category', 'unit']:
                        metaDict[key] = metaDf[key]
                    metaDict = dt.core._update_meta(metaDict)
                    tableID = dt.core._createDatabaseID(metaDict)
                    print(tableID)
                    if not updateTables:
                        if dt.core.DB.tableExist(tableID):
                            excludedTables['exists'].append(tableID)
                            continue

                    mask = tempDataMoSc['VARIABLE'] == entity
                    tempDataMoScEn = tempDataMoSc.loc[mask]

                    if len(tempDataMoScEn.index) > 0:

                        dataframe = tempDataMoScEn.set_index(self.setup.SPATIAL_COLUM_NAME)
                        if spatialSubSet:
                            spatIdx = dataframe[self.setup.SPATIAL_COLUM_NAME].isin(spatialSubSet)
                            dataframe = tempDataMoScEn.loc[spatIdx]
                        
                        dataframe = dataframe.drop(self.setup.COLUMNS_TO_DROP, axis=1)
                        dataframe = dataframe.dropna(axis=1, how='all').astype(float)
            
                        
                        dataTable = Datatable(dataframe, meta=metaDict)
                            
                    
                        # possible required unit conversion
                        if not pd.isna(metaDict['unitTo']):
                            dataTable = dataTable.convert(metaDict['unitTo'])
                            
                        tablesToCommit.append(dataTable)
                    else:
                        excludedTables['empty'].append(tableID)

        return tablesToCommit, excludedTables

#ä%%
class IAMC15_2019(BaseImportTool):
    
    def __init__(self):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "IAMC15_2019_R2"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/IAMC15_2019b/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH + 'iamc15_scenario_data_all_regions_r2.0.xlsx'
        self.setup.META_FILE    = self.setup.SOURCE_PATH + 'sr15_metadata_indicators_r2.0.xlsx'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        
        
        self.setup.LICENCE = ' CC-BY 4.0'
        self.setup.URL     = 'https://data.ene.iiasa.ac.at/iamc-1.5c-explorer'
        
        self.setup.VARIABLE_COLUMN_NAME = ['Variable']
        self.setup.MODEL_COLUMN_NAME = ['Model']
        self.setup.SCENARIO_COLUMN_NAME = ['Scenario']
        
        self.setup.SPATIAL_COLUM_NAME = ['Region']
        self.setup.COLUMNS_TO_DROP = ['Model', 'Scenario', 'Variable', 'Unit', 'combined']
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
        else:
            self.loadMapping()

        self.metaList = ['climate_category',
                         'baseline',
                         'marker',
                         'project',
                         'median warming at peak (MAGICC6)',
                         'year of peak warming (MAGICC6)',
                         'cumulative CO2 emissions (2016-2100, Gt CO2)',
                         'cumulative CCS (2016-2100, Gt CO2)',
                         'cumulative sequestration land-use (2016-2100, Gt CO2)',
                         'year of netzero CO2 emissions']        

    def loadMapping(self,):
        self.mappingEntity = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET,index_col=0)
        self.mappingEntity = self.mappingEntity.loc[self.mappingEntity.entity.notnull()]
        
        self.mappingModel = pd.read_excel(self.setup.MAPPING_FILE, sheet_name='model_mapping').set_index('model') 
        self.mappingModel = self.mappingModel.loc[self.mappingModel.index.notnull()]
        
        self.mappingScenario = pd.read_excel(self.setup.MAPPING_FILE, sheet_name='scenario_mapping').set_index('scenario') 
        self.mappingScenario = self.mappingScenario.loc[self.mappingScenario.index.notnull()]
        

 
    def createSourceMeta(self):
        self.meta = {'SOURCE_ID': self.setup.SOURCE_ID,
                      'collected_by' : config.CRUNCHER,
                      'date': dt.core.getDateString(),
                      'source_url' : self.setup.URL,
                      'licence': self.setup.LICENCE }
            
    def loadData(self):
        self.data = pd.read_excel(self.setup.DATA_FILE, sheet_name='data',  index_col = None, header =0, na_values='..')
        self.data['combined'] = self.data[['Scenario','Model']].apply(lambda x: '|'.join(x), axis=1)
        self.data['combined'] =  self.data['combined'].apply(lambda x : x.replace(' ','_')).apply(lambda x : x.replace('/','_'))
        
        
    def createVariableMapping(self):        
        
        # loading data if necessary
        if not hasattr(self, 'data'):        
            self.loadData()
        
        
        import numpy as np
 
        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')       
        
        #variables
        #index = self.data[self.setup.VARIABLE_COLUMN_NAME].unique()
        self.availableSeries = self.data.drop_duplicates('Variable').set_index('Variable')['Unit']
        self.mapping = pd.DataFrame(index=self.availableSeries.index, columns = MAPPING_COLUMNS)
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        self.mapping = self.mapping.sort_index()
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name=VAR_MAPPING_SHEET)
        
        #models
        index = np.unique(self.data[self.setup.MODEL_COLUMN_NAME].values)
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = ['model'])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='model_mapping')

        #models
        index = np.unique(self.data[self.setup.SCENARIO_COLUMN_NAME].values)
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = ['model'])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        
        
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='scenario_mapping')
        writer.close()

    def loadMetaData(self):
        # meta data
        self.createSourceMeta()
        self.metaDataDf = pd.read_excel(self.setup.META_FILE, header=0, sheet_name='meta')
        self.metaDataDf['climate_category'] = self.metaDataDf['category']
        self.metaDataDf['combined'] = self.metaDataDf[['scenario','model']].apply(lambda x: '|'.join(x), axis=1)
        self.metaDataDf['combined'] =  self.metaDataDf['combined'].apply(lambda x : x.replace(' ','_')).apply(lambda x : x.replace('/','_'))
        self.metaDataDf = self.metaDataDf.set_index(self.metaDataDf['combined'])
        
    def gatherMappedData(self, spatialSubSet = None, updateTables=False):
 #%%   
        import tqdm
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        

        # meta data
        self.loadMetaData()
        
        tablesToCommit  = []
        metaDict = dict()
        metaDict['source'] = self.setup.SOURCE_ID
        excludedTables = dict()
        excludedTables['empty'] = list()
        excludedTables['error'] = list()
        excludedTables['exists'] = list()
        
        availableCombitions = list(self.data.combined)
#        for scenModel in tqdm.tqdm(self.data.combined.unique()):
#            mask = self.data['combined'] == scenModel
#            tempDataMoSc = self.data.loc[mask,:]
#            metaDict['scenario'] = tempDataMoSc.loc[:,'Scenario'].iloc[0] + '|' + tempDataMoSc.loc[:,'Model'].iloc[0]
#            metaDict['model'] = tempDataMoSc.loc[:,'Model'].iloc[0]
        for model in self.mappingModel.index:
            mask = self.data['Model'] == self.mappingModel.loc[model]['original_model']
            tempDataMo = self.data.loc[mask]
            
            for scenario in self.mappingScenario.index:
                metaDict['scenario'] = scenario + '|' + model
                mask = tempDataMo['Scenario'] == self.mappingScenario.loc[scenario]['original_scenario']
                tempDataMoSc = tempDataMo.loc[mask]
                
                if metaDict['scenario'] not in availableCombitions:
                    continue
                
#            if True: 
                
#                for metaTag in self.metaList:
#                    try:
#                        metaDict[metaTag] = self.metaDataDf.loc[scenModel, metaTag]                                
#                        
#                    except:
#                        pass
                        
                
                for entity in self.mappingEntity.index:
                    metaDf =  self.mappingEntity.loc[entity]
                    metaDict['entity'] = self.mappingEntity.loc[entity]['entity']
                    metaDict['model']  = model
                    
                    for key in [ 'category', 'unit', 'unitTo']:
                        metaDict[key] = metaDf[key]
                    if pd.isna(metaDict['category']):
                        metaDict['category'] = ''
                    #print(metaDict)
                    metaDict = dt.core._update_meta(metaDict)
                    tableID = dt.core._createDatabaseID(metaDict)
                    #print(tableID)
                    if not updateTables:
                        if dt.core.DB.tableExist(tableID):
                            excludedTables['exists'].append(tableID)
                            continue
                    

                    
                    mask = tempDataMoSc['Variable'] == entity
                    tempDataMoScEn = tempDataMoSc.loc[mask]
                    

                    
                    if len(tempDataMoScEn.index) > 0:

                        dataframe = tempDataMoScEn.set_index(self.setup.SPATIAL_COLUM_NAME)
                        if spatialSubSet:
                            spatIdx = dataframe[self.setup.SPATIAL_COLUM_NAME].isin(spatialSubSet)
                            dataframe = tempDataMoScEn.loc[spatIdx]
                        
                        dataframe = dataframe.drop(self.setup.COLUMNS_TO_DROP, axis=1)
                        dataframe = dataframe.dropna(axis=1, how='all').astype(float)
            
                        
                        dataTable = Datatable(dataframe, meta=metaDict)
                        # possible required unit conversion
                        if not pd.isna(metaDict['unitTo']):
                            dataTable = dataTable.convert(metaDict['unitTo'])
                        tablesToCommit.append(dataTable)
                    else:
                        excludedTables['empty'].append(tableID)
                        

        return tablesToCommit, excludedTables

class CDLINKS_2018(BaseImportTool):
    
    def __init__(self):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "CDLINKS_2018"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/CDLINKS_2018/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH + 'cdlinks_public_version101_compare__20181010-142000.csv'
#        self.setup.META_FILE    = self.setup.SOURCE_PATH + 'sr15_metadata_indicators_r2.0.xlsx'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        
        
        self.setup.LICENCE = ' CC-BY 4.0'
        self.setup.URL     = 'https://db1.ene.iiasa.ac.at/CDLINKSDB'
        
        self.setup.VARIABLE_COLUMN_NAME = ['VARIABLE']
        self.setup.MODEL_COLUMN_NAME = ['MODEL']
        self.setup.SCENARIO_COLUMN_NAME = ['SCENARIO']

        self.setup.SPATIAL_COLUM_NAME = ['REGION']
        self.setup.COLUMNS_TO_DROP = ["MODEL","SCENARIO","VARIABLE","UNIT"]
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
        else:
            self.loadMapping()

    def loadMapping(self,):
        self.mappingEntity = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET,index_col=0)
        self.mappingEntity = self.mappingEntity.loc[self.mappingEntity.entity.notnull()]
        
        self.mappingModel = pd.read_excel(self.setup.MAPPING_FILE, sheet_name='model_mapping').set_index('model') 
        self.mappingModel = self.mappingModel.loc[self.mappingModel.index.notnull()]
        
        self.mappingScenario = pd.read_excel(self.setup.MAPPING_FILE, sheet_name='scenario_mapping').set_index('scenario') 
        self.mappingScenario = self.mappingScenario.loc[self.mappingScenario.index.notnull()]
            
    def createVariableMapping(self):
        # loading data if necessary
        if not hasattr(self, 'data'):        
            self.loadData()
        
        
        import numpy as np
 
        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')       
        
        #variables
        #index = self.data[self.setup.VARIABLE_COLUMN_NAME].unique()
        self.availableSeries = self.data.drop_duplicates(self.setup.VARIABLE_COLUMN_NAME).set_index(self.setup.VARIABLE_COLUMN_NAME)
        self.mapping = pd.DataFrame(index=self.availableSeries.index, columns = MAPPING_COLUMNS)
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        self.mapping = self.mapping.sort_index()
        self.mapping = self.mapping.loc[:,MAPPING_COLUMNS]
        self.mapping.unit = self.availableSeries.UNIT
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name=VAR_MAPPING_SHEET, index_label="original variable")
        
        #models
        index = np.unique(self.data[self.setup.MODEL_COLUMN_NAME].values)
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = self.setup.MODEL_COLUMN_NAME)
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='model_mapping', index_label="original model")

        # scenarios
        index = np.unique(self.data[self.setup.SCENARIO_COLUMN_NAME].values)
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = self.setup.SCENARIO_COLUMN_NAME)
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        
        
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='scenario_mapping', index_label="original scenario")
        writer.close()

    def loadData(self):
        self.data = pd.read_csv(self.setup.DATA_FILE, index_col = None, header =0)
        
    def gatherMappedData(self, spatialSubSet = None, updateTables=False):
    
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
        self.createSourceMeta()
#        # meta data
#        self.loadMetaData()
        
        tablesToCommit  = []
        metaDict = dict()
        metaDict['source'] = self.setup.SOURCE_ID
        excludedTables = dict()
        excludedTables['empty'] = list()
        excludedTables['erro'] = list()
        excludedTables['exists'] = list()
        for model in self.mappingModel.index:
            mask = self.data['MODEL'] == self.mappingModel.loc[model]['original model']
            tempDataMo = self.data.loc[mask]
            
            for scenario in self.mappingScenario.index:
                metaDict['scenario'] = scenario + '|' + model
                mask = tempDataMo['SCENARIO'] == self.mappingScenario.loc[scenario]['original scenario']
                tempDataMoSc = tempDataMo.loc[mask]
                
                
                for entity in self.mappingEntity.index:
                    metaDf =  self.mappingEntity.loc[entity]
                    metaDict['entity'] = self.mappingEntity.loc[entity]['entity']
                    metaDict['model']  = model
                    
                    for key in [ 'category', 'unit', 'unitTo']:
                        metaDict[key] = metaDf[key]
                    if pd.isnull(metaDict['category']):
                        metaDict['category'] = ''
                    metaDict = dt.core._update_meta(metaDict)
                    tableID = dt.core._createDatabaseID(metaDict)
                    print(tableID)
                    if not updateTables:
                        if dt.core.DB.tableExist(tableID):
                            excludedTables['exists'].append(tableID)
                            continue

                    mask = tempDataMoSc['VARIABLE'] == entity
                    tempDataMoScEn = tempDataMoSc.loc[mask]

                    if len(tempDataMoScEn.index) > 0:

                        dataframe = tempDataMoScEn.set_index(self.setup.SPATIAL_COLUM_NAME)
                        if spatialSubSet:
                            spatIdx = dataframe[self.setup.SPATIAL_COLUM_NAME].isin(spatialSubSet)
                            dataframe = tempDataMoScEn.loc[spatIdx]
                        
                        dataframe = dataframe.drop(self.setup.COLUMNS_TO_DROP, axis=1)
                        dataframe = dataframe.dropna(axis=1, how='all').astype(float)
            
                        
                        dataTable = Datatable(dataframe, meta=metaDict)
                            
                    
                        # possible required unit conversion
                        if not pd.isna(metaDict['unitTo']):
                            dataTable = dataTable.convert(metaDict['unitTo'])
                            
                        tablesToCommit.append(dataTable)
                    else:
                        excludedTables['empty'].append(tableID)

        return tablesToCommit, excludedTables
#%%
class IAMC_CMIP6(BaseImportTool):
    
    def __init__(self):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "IAMC_CMIP6_2020"
        self.setup.SOURCE_PATH  = os.path.join(config.PATH_TO_DATASHELF, 'rawdata', self.setup.SOURCE_ID)
        self.setup.DATA_FILE    = os.path.join(self.setup.SOURCE_PATH, 'SSP_CMIP6_201811.csv')
#        self.setup.META_FILE    = self.setup.SOURCE_PATH + 'sr15_metadata_indicators_r2.0.xlsx'
        self.setup.MAPPING_FILE = os.path.join(self.setup.SOURCE_PATH,'mapping.xlsx')
        
        
        self.setup.LICENCE = ' CC-BY 4.0'
        self.setup.URL     = 'https://tntcat.iiasa.ac.at/SspDb/dsd?Action=htmlpage&page=50'
        
#        self.setup.VARIABLE_COLUMN_NAME = ['VARIABLE']
#        self.setup.MODEL_COLUMN_NAME = ['MODEL']
#        self.setup.SCENARIO_COLUMN_NAME = ['SCENARIO']

        self.entryMapping = {
                'VARIABLE' : ['entity', 'category', 'unit', 'unitTo'],
                'MODEL' : ['model'],
                'SCENARIO': ['scenario'],
                }
        self.setup.SPATIAL_COLUM_NAME = ['REGION']
        self.setup.COLUMNS_TO_DROP = ["MODEL","SCENARIO","VARIABLE","UNIT"]
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
        else:
            self.loadMapping()

    def loadMapping(self,):
        self.mappingEntity = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET,index_col=0)
        self.mappingEntity = self.mappingEntity.loc[self.mappingEntity.entity.notnull()]
        
        self.mappingModel = pd.read_excel(self.setup.MAPPING_FILE, sheet_name='model_mapping',index_col=0)
        self.mappingModel = self.mappingModel.loc[self.mappingModel.index.notnull()]
        
        self.mappingScenario = pd.read_excel(self.setup.MAPPING_FILE, sheet_name='scenario_mapping',index_col=0)
        self.mappingScenario = self.mappingScenario.loc[self.mappingScenario.index.notnull()]
            
    def createVariableMapping(self):
        # loading data if necessary
        if not hasattr(self, 'data'):        
            self.loadData()
        
        
        import numpy as np
 
        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')       
        
        #variables
        #index = self.data[self.setup.VARIABLE_COLUMN_NAME].unique()
        entry ='VARIABLE'
        self.availableSeries = self.data.drop_duplicates([entry]).set_index(entry)
        self.mapping = pd.DataFrame(index=self.availableSeries.index, columns = self.entryMapping[entry])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        self.mapping = self.mapping.sort_index()
        self.mapping = self.mapping.loc[:,self.entryMapping[entry]]
        
        xx = self.mapping.index.map(lambda x: str(x).replace(' ','_').replace('CMIP6_',''))
        self.mapping.entity = xx.map(lambda x : '|'.join(str(x).split('|')[:2]))
        self.mapping.category = xx.map(lambda x : '|'.join(str(x).split('|')[2:]))
        
        self.mapping.unit = self.availableSeries.UNIT
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name=VAR_MAPPING_SHEET, index_label="original variable")
        
        #models
        entry ='MODEL'
        self.availableSeries = self.data.drop_duplicates([entry]).set_index(entry)
        self.mapping = pd.DataFrame(index=self.availableSeries.index, columns = self.entryMapping[entry])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        self.mapping = self.mapping.sort_index()
        self.mapping = self.mapping.loc[:,self.entryMapping[entry]]
        
        xx = self.mapping.index.map(lambda x: str(x).replace(' ','_').replace('/','_'))
        self.mapping.model = xx
#        self.mapping.category = xx.map(lambda x : '|'.join(str(x).split('|')[2:]))
        
        
#        self.mapping.unit = self.availableSeries.UNIT
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='model_mapping', index_label="original model")
        
        # scenarios
        entry ='SCENARIO'
        self.availableSeries = self.data.drop_duplicates([entry]).set_index(entry)
        self.mapping = pd.DataFrame(index=self.availableSeries.index, columns = self.entryMapping[entry])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        self.mapping = self.mapping.sort_index()
        self.mapping = self.mapping.loc[:,self.entryMapping[entry]]
        xx = self.mapping.index.map(lambda x: str(x).replace(' ','_').replace('/','_').replace('(','').replace(')',''))
        self.mapping.scenario = xx
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='scenario_mapping', index_label="original scenario")
        
        writer.close()

    def loadData(self):
        self.data = pd.read_csv(self.setup.DATA_FILE, index_col = None, header =0)
        
    def gatherMappedData(self, spatialSubSet = None, updateTables=False):
    
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
        self.createSourceMeta()
#        # meta data
#        self.loadMetaData()
        
        tablesToCommit  = []
        metaDict = dict()
        metaDict['source'] = self.setup.SOURCE_ID
        excludedTables = dict()
        excludedTables['empty'] = list()
        excludedTables['erro'] = list()
        excludedTables['exists'] = list()
        
        metaDict =  dict()
        metaDict['source'] = self.setup.SOURCE_ID
        for model in self.mappingModel.index:
            mask = self.data['MODEL'] == model
            metaDict['model'] = self.mappingModel.loc[model,'model']
            tempDataMo = self.data.loc[mask]
            
            for scenario in self.mappingScenario.index:
                metaDict['scenario'] = self.mappingScenario.loc[scenario,'scenario']
                mask = tempDataMo['SCENARIO'] == scenario
                tempDataMoSc = tempDataMo.loc[mask]
                
                
                for entity in self.mappingEntity.index:
                    
                    for key in ['entity', 'category', 'unit', 'unitTo']:
                        metaDict[key] = self.mappingEntity.loc[entity,key]

                    if pd.isnull(metaDict['category']):
                        metaDict['category'] = ''
                    metaDict = dt.core._update_meta(metaDict)
                    tableID = dt.core._createDatabaseID(metaDict)
                    print(tableID)
                    if not updateTables:
                        if dt.core.DB.tableExist(tableID):
                            excludedTables['exists'].append(tableID)
                            continue

                    mask = tempDataMoSc['VARIABLE'] == entity
                    tempDataMoScEn = tempDataMoSc.loc[mask]

                    if len(tempDataMoScEn.index) > 0:

                        dataframe = tempDataMoScEn.set_index(self.setup.SPATIAL_COLUM_NAME)
                        if spatialSubSet:
                            spatIdx = dataframe[self.setup.SPATIAL_COLUM_NAME].isin(spatialSubSet)
                            dataframe = tempDataMoScEn.loc[spatIdx]
                        
                        dataframe = dataframe.drop(self.setup.COLUMNS_TO_DROP, axis=1)
                        dataframe = dataframe.dropna(axis=1, how='all').astype(float)
            
                        
                        dataTable = Datatable(dataframe, meta=metaDict)
                            
                    
                        # possible required unit conversion
                        if not pd.isna(metaDict['unitTo']):
                            dataTable = dataTable.convert(metaDict['unitTo'])
                            
                        if 'unitTo' in dataTable.meta.keys():
                            del dataTable.meta['unitTo']
                        tablesToCommit.append(dataTable)
                    else:
                        excludedTables['empty'].append(tableID)

        return tablesToCommit, excludedTables
#%%
class AIM_SSP_DATA_2019(BaseImportTool):
    
    def __init__(self):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "AIM_SSPx_DATA_2019"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/AIM_SSP_scenarios/'
        self.setup.DATA_FILE    = [self.setup.SOURCE_PATH + '/data/ssp' + str(x) + '.csv' for x in range(1,5)]
        #self.setup.META_FILE    = self.setup.SOURCE_PATH + 'sr15_metadata_indicators_r2.0.xlsx'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        
        
        self.setup.LICENCE = ''
        self.setup.URL     = 'https://github.com/JGCRI/ssp-data'
        
        self.setup.VARIABLE_COLUMN_NAME = ['Variable']
        self.setup.MODEL_COLUMN_NAME = ['model']
        self.setup.SCENARIO_COLUMN_NAME = ['scenario']
        
        self.setup.SPATIAL_COLUM_NAME = 'region'
        self.setup.COLUMNS_TO_DROP = ['model', 'scenario', 'Variable', 'Unit']
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
        else:
            self.loadMapping()
            self.spatialMapping = self.loadSpatialMapping()

    def loadSpatialMapping(self,):
        return pd.read_excel(self.setup.MAPPING_FILE, sheet_name='spatial_mapping')
            

    def loadMapping(self,):
        self.mappingEntity = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET,index_col=0)
        self.mappingEntity = self.mappingEntity.loc[self.mappingEntity.entity.notnull()]
        
        self.mappingModel = pd.read_excel(self.setup.MAPPING_FILE, sheet_name='model_mapping').set_index('model') 
        self.mappingModel = self.mappingModel.loc[self.mappingModel.index.notnull()]
        
        self.mappingScenario = pd.read_excel(self.setup.MAPPING_FILE, sheet_name='scenario_mapping').set_index('scenario') 
        self.mappingScenario = self.mappingScenario.loc[self.mappingScenario.index.notnull()]
        
        
#    def createSourceMeta(self):
#        self.meta = {'SOURCE_ID': self.setup.SOURCE_ID,
#                      'collected_by' : config.CRUNCHER,
#                      'date': dt.core.getDateString(),
#                      'source_url' : self.setup.URL,
#                      'licence': self.setup.LICENCE }
            
    def loadData(self):
        datafiles = list()
        for file in self.setup.DATA_FILE:
            
            datafiles.append(pd.read_csv(file,   index_col = 0, header =0, na_values='..'))
        self.data = pd.concat(datafiles)
        newColumns = [x.replace('X','') for x in self.data.columns]
        self.data.columns = newColumns
        
    def createVariableMapping(self):        
        
        # loading data if necessary
        if not hasattr(self, 'data'):        
            self.loadData()
        
        
        import numpy as np
 
        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')       
        
        #variables
        #index = self.data[self.setup.VARIABLE_COLUMN_NAME].unique()
        self.availableSeries = self.data.drop_duplicates('Variable').set_index('Variable')['Unit']
        self.mapping = pd.DataFrame(index=self.availableSeries.index, columns = MAPPING_COLUMNS)
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        self.mapping = self.mapping.sort_index()
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name=VAR_MAPPING_SHEET)
        
        #models
        index = np.unique(self.data[self.setup.MODEL_COLUMN_NAME].values)
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = ['model'])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='model_mapping')

        #models
        index = np.unique(self.data[self.setup.SCENARIO_COLUMN_NAME].values)
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = ['model'])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        
        
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='scenario_mapping')
        
        
        #spatial mapping
        column = self.setup.SPATIAL_COLUM_NAME
        
        index = self.data.loc[:,column].unique()
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = ['mapping'])
        
        for region in self.mapping.index:
            coISO = dt.mapp.getSpatialID(region)
            
            if coISO is not None:
                self.mapping.loc[region,'mapping'] = coISO
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='spatial')
        
        writer.close()
        
        

#    def loadMetaData(self):
        # meta data
#        self.createSourceMeta()
#        self.metaDataDf = pd.read_excel(self.setup.META_FILE, header=0, sheet_name='meta')
#        self.metaDataDf['combined'] = self.metaDataDf[['model','scenario']].apply(lambda x: '_'.join(x), axis=1)
#        
#        self.metaDataDf = self.metaDataDf.set_index(self.metaDataDf['combined'])
        
    def gatherMappedData(self, spatialSubSet = None, updateTables=False):
    
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        

        # meta data
#        self.loadMetaData()
        
        tablesToCommit  = []
        metaDict = dict()
        metaDict['source'] = self.setup.SOURCE_ID
        excludedTables = dict()
        excludedTables['empty'] = list()
        excludedTables['error'] = list()
        excludedTables['exists'] = list()
        for model in self.mappingModel.index:
            mask = self.data['model'] == self.mappingModel.loc[model]['original_model']
            tempDataMo = self.data.loc[mask]
            
            for scenario in self.mappingScenario.index:
                metaDict['scenario'] = scenario + '|' + model
                mask = tempDataMo['scenario'] == self.mappingScenario.loc[scenario]['original_scenario']
                tempDataMoSc = tempDataMo.loc[mask]
                
                
                for entity in self.mappingEntity.index:
                    metaDf =  self.mappingEntity.loc[entity]
                    metaDict['entity'] = self.mappingEntity.loc[entity]['entity']
                    metaDict['model']  = model

                    for key in [ 'category', 'unit', 'unitTo']:
                        metaDict[key] = metaDf[key]
                    if pd.isna(metaDict['category']):
                        metaDict['category'] = ''
                    #print(metaDict)
                    tableID = dt.core._createDatabaseID(metaDict)
                    #print(tableID)
                    if not updateTables:
                        if dt.core.DB.tableExist(tableID):
                            excludedTables['exists'].append(tableID)
                            continue
                    

                    
                    mask = tempDataMoSc['Variable'] == entity
                    tempDataMoScEn = tempDataMoSc.loc[mask]
                    

                    
                    if len(tempDataMoScEn.index) > 0:

                        dataframe = tempDataMoScEn.set_index(self.setup.SPATIAL_COLUM_NAME)
                        if spatialSubSet:
                            spatIdx = dataframe[self.setup.SPATIAL_COLUM_NAME].isin(spatialSubSet)
                            dataframe = tempDataMoScEn.loc[spatIdx]
                        
                        dataframe = dataframe.drop(self.setup.COLUMNS_TO_DROP, axis=1)
                        dataframe = dataframe.dropna(axis=1, how='all').astype(float)

                        #spatial
                        validSpatialRegions = self.spatialMapping.index[~self.spatialMapping.mapping.isnull()]
                        dataframe = dataframe.loc[validSpatialRegions,:]
                        dataframe.index = self.spatialMapping.mapping[~self.spatialMapping.mapping.isnull()]

                        
                        dataTable = Datatable(dataframe, meta=metaDict)
                        # possible required unit conversion
                        if not pd.isna(metaDict['unitTo']):
                            dataTable = dataTable.convert(metaDict['unitTo'])
                        tablesToCommit.append(dataTable)
                    else:
                        excludedTables['empty'].append(tableID)

        return tablesToCommit, excludedTables
#%%
class IRENA2019(BaseImportTool):
    
    """
    IRENA data import tool
    """
    def __init__(self):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "IRENA_2019"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/IRENA_2019/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH + 'IRENA_RE_electricity_statistics.xlsx'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        self.setup.LICENCE = 'open source'
        self.setup.URL     = 'http://www.irena.org/IRENADocuments/IRENA_RE_electricity_statistics_-_Query_tool.xlsm'
        
#        self.setup.INDEX_COLUMN_NAME = ['FLOW', 'PRODUCT']
#        self.setup.SPATIAL_COLUM_NAME = 'COUNTRY'
#        self.setup.COLUMNS_TO_DROP = [ 'PRODUCT','FLOW','combined']
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
        else:
            self.mapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET)
            self.spatialMapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=SPATIAL_MAPPING_SHEET)

        self.createSourceMeta()


    def loadData(self):
        
        from datatools.io import ExcelReader
        setup = dict()
        setup['filePath']  = self.setup.SOURCE_PATH 
        setup['fileName']  = 'IRENA_RE_electricity_statistics.xlsx'
        
        
        
        self.dataDf = pd.DataFrame([], columns = ['meta','dataDf'])
        
        sheetList = list(range(1,4)) + list(range(6,22))
        for sheetNum in sheetList:
            
            #Capacity
            setup['sheetName'] = str(sheetNum)
            setup['timeColIdx']  = ('B5', 'AL5')
            setup['spaceRowIdx'] = ('A7', 'A198')
            ex = ExcelReader(setup)
            df = ex.gatherData()
            df = df.iloc[:, ~pd.isna(df.columns)]
            df = df.iloc[~pd.isna(df.index),:]
            df.columns = df.columns.astype(int)
            entity = 'Capacity ' + ex.gatherValue('A1')
            unit = ex.gatherValue('A5')
            if "MW" in unit:
                unit = "MW"
            elif "GWh" in unit:
                unit = "GWh"
            
            metaDict = {'unit': unit, 
                        'entity':entity}
            self.dataDf.loc[entity] = [metaDict, df]
        
            #Production
            setup['timeColIdx']  = ('AO5', 'BU5')
            setup['spaceRowIdx'] = ('A7', 'A198')
            ex = ExcelReader(setup)
            df = ex.gatherData()
            df = df.iloc[:, ~pd.isna(df.columns)]
            df = df.iloc[~pd.isna(df.index),:]
            df.columns = df.columns.astype(int)
            entity = 'Production ' + ex.gatherValue('A1')
            unit = ex.gatherValue('A5')
            if "MW" in unit:
                unit = "MW"
            elif "GWh" in unit:
                unit = "GWh"
            
            metaDict = {'unit': unit, 
                        'entity':entity}
            self.dataDf.loc[entity] = [metaDict, df]

        
#        self.data = pd.read_csv(self.setup.DATA_FILE, encoding='utf8', engine='python', index_col = None, header =0, na_values='c')
#        self.data['combined'] = self.data[self.setup.INDEX_COLUMN_NAME].apply(lambda x: '_'.join(x), axis=1)
#        
#        self.data = self.data.set_index(self.data['combined'])#.drop('combined',axis=1)
        
    
          
        
    def createVariableMapping(self):   
        
        
        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy') 
        
        # variable mapping
        self.mapping = pd.DataFrame([], columns= MAPPING_COLUMNS, index = self.dataDf.index.sort_values())
        
        self.mapping.source = self.setup.SOURCE_ID
        self.mapping.scenario = 'historic'
        self.mapping.entity = self.mapping.index.str.split(' ').str.join('_')
        self.mapping.category = ''
        
        for idx in self.mapping.index:
            self.mapping.loc[idx,['unit']] = self.dataDf.loc[idx,['meta']][0]['unit']
        
        self.mapping.to_excel(writer, sheet_name=VAR_MAPPING_SHEET)
        
        # spatial mapping
        self.spatialMapping = dict()
        spatialIDList = list()
        for i in range(len(self.dataDf)):
            spatialIDList = spatialIDList + list(self.dataDf.iloc[i,1].index.unique())
        spatialIDList = list(set(spatialIDList))    
        for spatID in spatialIDList:
            ISO_ID = dt.getCountryISO(spatID)
            if ISO_ID is not None:
                self.spatialMapping[spatID] = ISO_ID
            else:
                print('not found: ' + spatID)
                
        # adding regions
        self.spatialMapping['World'] = "World"
        self.spatialMapping['UK'] = "GBR"
        self.spatialMapping['European Union'] = "EU28"
        
        dataFrame = pd.DataFrame(data=[],columns = ['alternative'])
        for key, item in self.spatialMapping.items():
            dataFrame.loc[key] = item
        dataFrame.to_excel(writer, sheet_name=SPATIAL_MAPPING_SHEET)
        self.spatialMapping = dataFrame
        writer.close()
        
    def gatherMappedData(self, spatialSubSet = None):
        # loading data if necessary
        if not hasattr(self, 'dataDf'):
            self.loadData()        
        
        indexDataToCollect = self.mapping.index[~pd.isnull(self.mapping['entity'])]
        
        tablesToCommit  = []
        for idx in indexDataToCollect:
            metaDf = self.mapping.loc[idx]
            print(idx)
            
            #print(metaDf[config.REQUIRED_META_FIELDS].isnull().all() == False)
            #print(metaData[self.setup.INDEX_COLUMN_NAME])
            
            
            metaDict = {key : metaDf[key] for key in config.REQUIRED_META_FIELDS}           
            
            metaDict['original code'] = idx
            metaDict['unitTo'] = metaDf['unitTo']
            #metaDict['original name'] = metaDf['Indicator Name']
            
            seriesIdx = idx
            
            
            
            
            dataframe = self.dataDf.loc[seriesIdx]['dataDf'].copy()
            dataframe = dataframe.astype(float)
            
            newData= list()
            for iRow in range(len(dataframe)):
                if dataframe.index[iRow] in self.spatialMapping.index:
                    newData.append(self.spatialMapping.alternative.loc[dataframe.index[iRow]])
                else:
                    newData.append(pd.np.nan)
                    print('ignoring: ' + dataframe.index[iRow])
            dataframe.index = newData
           
            if spatialSubSet:
                spatIdx = dataframe.index.isin(spatialSubSet)
                dataframe = dataframe.loc[spatIdx]
            
            
            
            dataframe= dataframe.dropna(axis=1, how='all')
            dataframe= dataframe.loc[~pd.isna(dataframe.index)]
            dataTable = Datatable(dataframe, meta=metaDict)
            # possible required unit conversion
            if not pd.isna(metaDict['unitTo']):
                dataTable = dataTable.convert(metaDict['unitTo'])
            tablesToCommit.append(dataTable)
        
        return tablesToCommit

class SSP_DATA(BaseImportTool):
    def __init__(self):

        self.setup = setupStruct()
        
        self.setup.SOURCE_ID    = "SSP_DB_2013"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/SSP_DB/'
        self.setup.DATA_FILE    = [self.setup.SOURCE_PATH + 'SspDb_country_data_2013-06-12.csv',
                                   self.setup.SOURCE_PATH + 'SspDb_compare_regions_2013-06-12.csv']
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        self.setup.LICENCE = 'open access'
        self.setup.URL     = 'tntcat.iiasa.ac.at/SspWorkDb'

        self.setup.VARIABLE_COLUMN_NAME = ['VARIABLE']
        self.setup.MODEL_COLUMN_NAME = ['MODEL']
        self.setup.SCENARIO_COLUMN_NAME = ['Scenario']

        self.setup.SPATIAL_COLUM_NAME = ['REGION']
        self.setup.COLUMNS_TO_DROP = ["MODEL","SCENARIO","VARIABLE","UNIT"]
        

        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
        else:
            self.loadMapping()
        
        self.createSourceMeta()

    def createSourceMeta(self):
        self.meta = {'SOURCE_ID': self.setup.SOURCE_ID,
                      'collected_by' : config.CRUNCHER,
                      'date': dt.core.getDateString(),
                      'source_url' : self.setup.URL,
                      'licence': self.setup.LICENCE }
        
    def loadMapping(self,):
        self.mappingEntity = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET,index_col=0)
        self.mappingEntity = self.mappingEntity.loc[self.mappingEntity.entity.notnull()]
        
        self.mappingModel = pd.read_excel(self.setup.MAPPING_FILE, sheet_name='model_mapping').set_index('model') 
        self.mappingModel = self.mappingModel.loc[self.mappingModel.index.notnull()]
        
        self.mappingScenario = pd.read_excel(self.setup.MAPPING_FILE, sheet_name='scenario_mapping').set_index('scenario') 
        self.mappingScenario = self.mappingScenario.loc[self.mappingScenario.index.notnull()]



    def loadData(self):
        datafiles = [pd.read_csv(dataFile) for dataFile in self.setup.DATA_FILE]
        self.data = pd.concat(datafiles)


    def createVariableMapping(self):
        
        # loading data if necessary
        if not hasattr(self, 'data'):        
            self.loadData()
        
        
        import numpy as np
 
        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')       
        
        #variables
        #index = self.data[self.setup.VARIABLE_COLUMN_NAME].unique()
        self.availableSeries = self.data.drop_duplicates(self.setup.VARIABLE_COLUMN_NAME).set_index(self.setup.VARIABLE_COLUMN_NAME)
        self.mapping = pd.DataFrame(index=self.availableSeries.index, columns = MAPPING_COLUMNS)
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        self.mapping = self.mapping.sort_index()
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name=VAR_MAPPING_SHEET, index_label="original variable")
        
        #models
        index = np.unique(self.data[self.setup.MODEL_COLUMN_NAME].values)
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = self.setup.MODEL_COLUMN_NAME)
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='model_mapping', index_label="original model")

        # scenarios
        index = np.unique(self.data[self.setup.SCENARIO_COLUMN_NAME].values)
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = self.setup.SCENARIO_COLUMN_NAME)
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping.source = self.setup.SOURCE_ID
        
        
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='scenario_mapping', index_label="original scenario")
        writer.close()


    def gatherMappedData(self, spatialSubSet = None, updateTables=False):
    
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
        self.createSourceMeta()
#        # meta data
#        self.loadMetaData()
        
        tablesToCommit  = []
        metaDict = dict()
        metaDict['source'] = self.setup.SOURCE_ID
        excludedTables = dict()
        excludedTables['empty'] = list()
        excludedTables['erro'] = list()
        excludedTables['exists'] = list()
        for model in self.mappingModel.index:
            mask = self.data['MODEL'] == self.mappingModel.loc[model]['original_model']
            tempDataMo = self.data.loc[mask]
            
            for scenario in self.mappingScenario.index:
                metaDict['scenario'] = scenario
                mask = tempDataMo['SCENARIO'] == self.mappingScenario.loc[scenario]['original_scenario']
                tempDataMoSc = tempDataMo.loc[mask]
                
                
                for entity in self.mappingEntity.index:
                    metaDf =  self.mappingEntity.loc[entity]
                    metaDict['entity'] = self.mappingEntity.loc[entity]['entity']
                    metaDict['model']  = model
                    
                    for key in [ 'category', 'unit', 'unitTo']:
                        metaDict[key] = metaDf[key]
                    
                    metaDict = dt.core._update_meta(metaDict)
                    tableID = dt.core._createDatabaseID(metaDict)
                    print(tableID)
                    if not updateTables:
                        if dt.core.DB.tableExist(tableID):
                            excludedTables['exists'].append(tableID)
                            continue

                    mask = tempDataMoSc['VARIABLE'] == entity
                    tempDataMoScEn = tempDataMoSc.loc[mask]

                    if len(tempDataMoScEn.index) > 0:

                        dataframe = tempDataMoScEn.set_index(self.setup.SPATIAL_COLUM_NAME)
                        if spatialSubSet:
                            spatIdx = dataframe[self.setup.SPATIAL_COLUM_NAME].isin(spatialSubSet)
                            dataframe = tempDataMoScEn.loc[spatIdx]
                        
                        dataframe = dataframe.drop(self.setup.COLUMNS_TO_DROP, axis=1)
                        dataframe = dataframe.dropna(axis=1, how='all').astype(float)
            
                        
                        dataTable = Datatable(dataframe, meta=metaDict)
                        # possible required unit conversion
                        if not pd.isna(metaDict['unitTo']):
                            dataTable = dataTable.convert(metaDict['unitTo'])
                        tablesToCommit.append(dataTable)
                    else:
                        excludedTables['empty'].append(tableID)

        return tablesToCommit, excludedTables

class PRIMAP_DOWNSCALE(BaseImportTool):
    def __init__(self):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "PRIMAP_DOWN_2020"
        self.setup.SOURCE_YEAR  = "2020"
        self.setup.SOURCE_NAME  = "PRIMAP_DOWN"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/PRIMAP_DOWNSCALE/'
        
        csvFiles  = os.listdir(self.setup.SOURCE_PATH)
        csvFiles = [file for file in csvFiles if '.csv' in file]
        self.setup.DATA_FILES    = [os.path.join(self.setup.SOURCE_PATH, x) for x in csvFiles]
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        
        
        self.setup.LICENCE = 'Creative Commons Attribution 4.0 International'
        self.setup.URL     = 'https://zenodo.org/record/3638137#.XxcBWiFR0Wp'
        
        self.entryMapping = {
                'entity' : ['entity','unit', 'unitTo'],
                'source' : ['model', 'downscaling'],
                'scenario': ['scenario'],
                'category': ['category'],
                }
        
        self.setup.SPATIAL_COLUM_NAME = ['country']
        self.setup.COLUMNS_TO_DROP = ["entity","source","scenario","category"]
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
            print("no mapping file found")
        else:
            self.mapping = dict()
            for var in self.entryMapping.keys():
                df = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=var , index_col=0)
                df = df.loc[~df.loc[:,self.entryMapping[var][0]].isna()]
                
                self.mapping[var] = df.T.to_dict()
         
            
        
                
    def createVariableMapping(self):
        # loading data if necessary
#        if not hasattr(self, 'data'):        
#            self.loadData()
        
        
        import numpy as np
 
        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')       
        self.mapping = dict()
        for data in self.loadData():
            for columnKey in self.entryMapping.keys():
                if not isinstance(self.entryMapping[columnKey], list):
                    self.entryMapping[columnKey] = [self.entryMapping[columnKey]]
                availableSeries = data.drop_duplicates(columnKey).set_index(columnKey)    
                
                if columnKey not in self.mapping.keys():
                    self.mapping[columnKey] = pd.DataFrame(index=availableSeries.index, columns = self.entryMapping[columnKey])
    #                if "unit" in self.entryMapping[columnKey]:
    #                    self.mapping.unit = availableSeries.unit
                else:
                    newEntries = pd.DataFrame(index=availableSeries.index, columns = self.entryMapping[columnKey])
                    
                    for idx in newEntries.index:
                        if idx not in self.mapping[columnKey].index:
                            self.mapping[columnKey].loc[idx,:] = newEntries.loc[idx,:]
                            
                if "unit" in self.entryMapping[columnKey]:
                    self.mapping[columnKey].loc[availableSeries.index,"unit"] = availableSeries.unit
            
        for columnKey in self.entryMapping.keys():   
            self.mapping[columnKey].to_excel(writer, engine='openpyxl', sheet_name=columnKey, index_label="original variable")
        
        writer.close()

    def loadData(self):
        for dataFile in self.setup.DATA_FILES[:]:
            yield pd.read_csv(dataFile, index_col = None, header =0)
        
    def gatherMappedData(self, spatialSubSet = None, updateTables=False):
    
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
        self.createSourceMeta()
#        # meta data
#        self.loadMetaData()
        
        tablesToCommit  = []
        metaDict = dict()
        metaDict['source'] = self.setup.SOURCE_ID
        excludedTables = dict()
        excludedTables['empty'] = list()
        excludedTables['erro'] = list()
        excludedTables['exists'] = list()
        #%%
#        datafilter = list()
#        datafilter.append(self.data)
#        filterList = list(self.entryMapping.keys())
#        tableList = list()
#        metaDict = dict()
#        metaDict['source_name'] = [self.setup.SOURCE_ID]
#        metaDict['source_year'] = [self.setup.SOURCE_YEAR]
        import copy
        import numpy as np
        
        def process_and_filter(self, datafilter, filterList, tableList,metaDict):
            
            if len(filterList) == 0:
                yearColumns = dt.util.yearsColumnsOnly(datafilter[-1])
                for key in metaDict.keys():
                    metaDict[key] = '|'.join(metaDict[key])
                dataTable = dt.Datatable(datafilter[-1].loc[:,yearColumns], meta=metaDict)
                dataTable.index = datafilter[-1].loc[:,'country']
                if 'unitTo' in dataTable.meta and (isinstance(dataTable.meta['unitTo'],str)) :
                    # convert if required
                    dataTable = dataTable.convert(metaDict['unitTo'])
                    del dataTable.meta['unitTo']
                    
                tableList.append(dataTable)
                del yearColumns
                del dataTable
                del key
                del datafilter, filterList, metaDict
                
                return tableList
            columnKey = filterList.pop()
            print(columnKey)
            for mappFrom, mappTo in self.mapping[columnKey].items():
                print(mappFrom, mappTo)
                mask = datafilter[-1].loc[:,columnKey] == mappFrom
                datafilter.append(datafilter[-1].loc[mask,:])
                for key in mappTo.keys():
                    if not isinstance(mappTo[key],str):
                        continue
                    if key in metaDict.keys():
                        print(metaDict[key])
                        print(mappTo[key])
                        metaDict[key].append(mappTo[key])

                    else:
                        metaDict[key] = [mappTo[key]]
#                metaDict.update(mappTo)
                if len(datafilter[-1]) == 0:
                    # break loop if empty filtered set
                    
                    #clean
                    _ = datafilter.pop()
                    print('Meta: ' + str(metaDict))
                    for key in mappTo.keys():
                        if not isinstance(mappTo[key],str):
                            continue
                        metaDict[key].remove(mappTo[key])
                    del _
                    continue
                
#                sdf
                tableList = process_and_filter(self, copy.copy(datafilter), copy.copy(filterList), tableList, copy.copy(metaDict))
                
                #clean
                datafilter.pop()
                print('Meta: ' + str(metaDict))
                for key in mappTo.keys():
                    if not isinstance(mappTo[key],str):
                        continue
                    metaDict[key].remove(mappTo[key])


            del key
            
            del datafilter, filterList, metaDict
            return tableList
        
        for data in self.loadData():
            filterList = list(self.entryMapping.keys())
            tableList = list()
            metaDict = dict()
            metaDict['source_name'] = [self.setup.SOURCE_NAME]
            metaDict['source_year'] = [self.setup.SOURCE_YEAR]
            datafilter = [data]
            filteredData = process_and_filter(self, datafilter, filterList,tableList, metaDict)
#            adsfr
            tablesToCommit.extend(filteredData)
            #%%
        return tablesToCommit, excludedTables
    
class LED_2019(BaseImportTool):
    
    def __init__(self):

        self.setup = setupStruct()
        
        self.setup.SOURCE_ID    = "LED_2019"
        self.setup.SOURCE_NAME    = "LED"
        self.setup.SOURCE_YEAR    = "2019"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/LED_2019/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH + 'led.csv'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        self.setup.LICENCE = '?' # TODO
        self.setup.URL     = '?' # TODO

        self.setup.COLUMNS_TO_DROP = ['model', 'scenario', 'variable', 'unit']

        self.createSourceMeta()
                
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
        else:
            self.mapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET, index_col=0)

    def createVariableMapping(self):
        with pd.ExcelWriter(
            self.setup.MAPPING_FILE,
            engine='xlsxwriter',
            datetime_format='mmm d yyyy hh:mm:ss',
            date_format='mmmm dd yyyy'
        ) as writer:

            if not hasattr(self, 'data'):
                self.loadData()
            
            meta = self.data.loc[
                ~self.data.index.duplicated(keep='first'),
                ['model', 'scenario', 'variable', 'unit']
            ]

            variable = (
                meta['variable']
                .str.replace(" ", "_")
                .replace({
                    "Emissions|Kyoto Gases": "Emissions|KYOTOGHG"
                })
            )
            variable_components = variable.str.split('|')
            two_component_entity = variable_components.str[0].isin(["Emissions", "GDP"])
            entity = variable_components.str[:2].str.join('|').where(two_component_entity, variable_components.str[0])
            category = variable_components.str[2:].str.join('|').where(two_component_entity, variable_components.str[1:].str.join('|'))

            self.mapping = (
                meta.assign(
                    source=self.setup.SOURCE_ID,
                    variable=variable,
                    entity=entity,
                    category=category,
                    unit=(
                        # units ['million t DM/yr', 'GW', 'US$2010/kW', 'Mt CO2/yr',
                        #        'billion US$2010/yr', '%', 'Mt BC/yr', 'kt CF4/yr', 'Mt CH4/yr',
                        #        'Mt CO/yr', 'Mt CO2-equiv/yr', 'kt HFC134a-equiv/yr',
                        #        'kt HFC125/yr', 'kt HFC134a/yr', 'kt HFC143a/yr', 'kt HFC227ea/yr',
                        #        'kt HFC23/yr', 'kt HFC245fa/yr', 'kt HFC32/yr', 'kt HFC43-10/yr',
                        #        'kt N2O/yr', 'Mt NH3/yr', 'Mt NOx/yr', 'Mt OC/yr', 'kt SF6/yr',
                        #        'Mt SO2/yr', 'Mt VOC/yr', 'Tg N/yr', 't/ha/yr', 'Tg P/yr', 'EJ/yr',
                        #        'kcal/cap/day', 'million m3/yr', 'MtCO2eq/year', 'EJ_final', 'Mha',
                        #        'EJ_primary', 'Mm3', 'million ha', 'years', 'US$2010/kW/yr',
                        #        'US$2010/kWh', 'billion US$2010/yr OR local currency/yr',
                        #        'million', 'Index (2005 = 1)',
                        #        'US$2010/t CO2 or local currency/t CO2',
                        #        'US$2010/GJ or local currency/GJ', 'ZJ', 'km3/yr', 't DM/ha/yr']

                        meta['unit']
                        .replace({
                            'Mt CO2-equiv/yr': 'Mt CO2eq/yr',
                            'MtCO2eq/year': 'Mt CO2eq/yr',
                            'kt HFC134a-equiv/yr': 'kt HFC134aeq/yr',
                            'EJ_final': 'EJ',
                            'EJ_primary': 'EJ',
                            'Index (2005 = 1)': '1', # ?? TODO
                        })
                        .str.replace('US$2010', 'USD2010', regex=False)
                        .str.replace('m3', 'm**3', regex=False)
                        .str.replace(' OR local currency.*$', '', flags=re.IGNORECASE) # ?? TODO
                    )
                )
            )
            self.mapping.to_excel(writer, sheet_name=VAR_MAPPING_SHEET)
        
    def loadData(self):
         self.data = pd.read_csv(self.setup.DATA_FILE) 
         self.data.set_axis(self.data.columns.str.lower(), axis=1, inplace=True)
         self.data.set_index(self.data['model'] + '_' + self.data['scenario'] + '_' + self.data['variable'], inplace=True)
         
    def gatherMappedData(self, spatialSubSet = None, updateTables = False):
        excludedTables = defaultdict(list)
        
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
        
        tablesToCommit  = []
        for idx, metaDf in self.mapping.iterrows():
            metaDict = metaDf.to_dict()
            metaDict.update(
                source_name=self.setup.SOURCE_NAME,
                source_year=self.setup.SOURCE_YEAR,
            )
            
            metaDict = dt.core._update_meta(metaDict)
            tableID = dt.core._createDatabaseID(metaDict)

            if not updateTables and dt.core.DB.tableExist(tableID):
                excludedTables['exists'].append(tableID)
                print('table exists')
                print(tableID)
                continue
                    
            dataframe = (
                self.data.loc[idx,:].set_index('region').drop(self.setup.COLUMNS_TO_DROP, axis=1)
                .astype(float)
                .dropna(axis=1, how='all')
            )

            if not dataframe.index.is_unique:
                print(f"Table {tableID} has non-unique regions, skipping")
                continue

            try:
                dataTable = Datatable(dataframe, meta=metaDict)
            except pint.errors.UndefinedUnitError as exc:
                print(f"Undefined unit `{exc.args[0]}` for table {tableID}, skipping")
                excludedTables['error'].append(tableID)
                continue
            
            # possible required unit conversion
            if not pd.isna(metaDict.get('unitTo')):
                dataTable = dataTable.convert(metaDict['unitTo'])
            tablesToCommit.append(dataTable)
        
        return tablesToCommit, excludedTables

class IMAGE15_2020(BaseImportTool):
    
    def __init__(self):

        self.setup = setupStruct()
        
        self.setup.SOURCE_ID    = "IMAGE15_2020"
        self.setup.SOURCE_NAME    = "IMAGE15"
        self.setup.SOURCE_YEAR    = "2020"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/IMAGE15_2020/'
        self.setup.DATA_FILE    = {
            fn[:fn.rindex(".")]: os.path.join(self.setup.SOURCE_PATH, fn)
            for fn in os.listdir(self.setup.SOURCE_PATH)
            if fn.endswith((".csv", ".xlsx")) and fn != 'mapping.xlsx'
        }
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        self.setup.LICENCE = '?' # TODO
        self.setup.URL     = '?' # TODO

        self.setup.COLUMNS_TO_DROP = ['model', 'scenario', 'variable', 'unit']

        self.createSourceMeta()
                
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
        else:
            self.mapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET, index_col=0)

    def createVariableMapping(self):
        with pd.ExcelWriter(
            self.setup.MAPPING_FILE,
            engine='xlsxwriter',
            datetime_format='mmm d yyyy hh:mm:ss',
            date_format='mmmm dd yyyy'
        ) as writer:

            if not hasattr(self, 'data'):
                self.loadData()
            
            meta = self.data.loc[
                ~self.data.index.duplicated(keep='first'),
                ['model', 'scenario', 'variable', 'unit']
            ]
            variable = (
                meta['variable']
                .str.replace(" ", "_")
                .replace({
                    "Emissions|Kyoto Gases": "Emissions|KYOTOGHG"
                })
            )
            variable_components = variable.str.split('|')
            two_component_entity = variable_components.str[0].isin(["Emissions", "GDP"])
            entity = variable_components.str[:2].str.join('|').where(two_component_entity, variable_components.str[0])
            category = variable_components.str[2:].str.join('|').where(two_component_entity, variable_components.str[1:].str.join('|'))

            self.mapping = (
                meta.assign(
                    source=self.setup.SOURCE_ID,
                    variable=variable,
                    entity=entity,
                    category=category,
                    unit=(

                        # ['million t DM/yr', 'GW', '$/kW', 'ppb', 'ppm',
                        #     'billion US$2005/yr', 'Mt BC/yr', 'kt C2F6/yr', 'kt C6F14/yr',
                        #     'kt CF4/yr', 'Mt CH4/yr', 'Mt CO2/yr', 'Mt CO/yr',
                        #     'Mt CO2-equiv/yr', 'kt HFC134a-equiv/yr', 'kt HFC125/yr',
                        #     'kt HFC134a/yr', 'kt HFC143a/yr', 'kt HFC227ea/yr', 'kt HFC23/yr',
                        #     'kt HFC245fa/yr', 'kt HFC32/yr', 'kt HFC43-10/yr', 'kt N2O/yr',
                        #     'Mt NH3/yr', 'Mt NO2/yr', 'Mt OC/yr', 'kt CF4-equiv/yr',
                        #     'kt SF6/yr', 'Mt SO2/yr', 'Mt VOC/yr', 'bn tkm/yr', 'bn pkm/yr',
                        #     'Tg N/yr', 'EJ/yr', 'kcal/cap/day', 'W/m2', 'million m3/yr',
                        #     'million ha', 'US$2005/MWh', 'million', 'Index (2005 = 1)',
                        #     'US$2005/GJ', 'EJ', 'ktU', ' °C', 't DM/ha/yr', '1000 t',
                        #     'US$2005/kW', '%', 'million Ha/yr', 'years', 'US$2005/kW/yr',
                        #     'US$2005/t CO2']

                        meta['unit']
                        .str.replace('US$2005', 'USD2005', regex=False)
                        .replace({
                            'ktU': 'kt U',
                            'Mt CO2-equiv/yr': 'Mt CO2eq/yr',
                            'kt HFC134a-equiv/yr': 'kt HFC134aeq/yr',
                            'Index (2005 = 1)': '1', # ?? TODO
                        })
                        .str.replace('US$2005', 'USD2005', regex=False)
                        .str.replace('bn', 'billion', regex=False)
                        .str.replace('m3', 'm**3', regex=False)
                        .str.replace('m2', 'm**2', regex=False)
                    )
                )
            )
            
            problematic_units = pd.Series(self.mapping.unit.unique())[lambda s: ~s.map(isUnit)]
            if not problematic_units.empty:
                print("problematic units:", ", ".join(problematic_units))
            self.mapping.to_excel(writer, sheet_name=VAR_MAPPING_SHEET)
        
    def loadData(self):
        data = []
        for fn in self.setup.DATA_FILE.values():
            if fn.endswith(".csv"):
                df = pd.read_csv(fn, encoding='latin1')
            elif fn.endswith(".xlsx"):
                df = pd.read_excel(fn, sheet_name="data")
            else:
                raise RuntimeError("File must have a file ending .csv or .xlsx")
        
            df.set_axis(df.columns.str.lower(), axis=1, inplace=True)
            df.set_index(df['model'] + '_' + df['scenario'] + '_' + df['variable'], inplace=True)

            data.append(df)

        self.data = pd.concat(data, sort=False)
         
    def gatherMappedData(self, spatialSubSet = None, updateTables = False):
        excludedTables = defaultdict(list)
        
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
        
        tablesToCommit  = []
        for idx, metaDf in self.mapping.iterrows():
            metaDict = metaDf.to_dict()
            metaDict.update(
                source_name=self.setup.SOURCE_NAME,
                source_year=self.setup.SOURCE_YEAR,
            )
            
            metaDict = dt.core._update_meta(metaDict)
            tableID = dt.core._createDatabaseID(metaDict)

            if not updateTables and dt.core.DB.tableExist(tableID):
                excludedTables['exists'].append(tableID)
                print('table exists')
                print(tableID)
                continue
                    
            dataframe = (
                self.data.loc[self.data.index == idx]
                .set_index('region').drop(self.setup.COLUMNS_TO_DROP, axis=1)
                .astype(float)
                .dropna(axis=1, how='all')
            )

            if not dataframe.index.is_unique:
                print(f"Table {tableID} has non-unique regions, skipping")
                continue

            try:
                dataTable = Datatable(dataframe, meta=metaDict)
            except pint.errors.UndefinedUnitError:
                excludedTables['error'].append(tableID)
                continue
            
            # possible required unit conversion
            if not pd.isna(metaDict.get('unitTo')):
                dataTable = dataTable.convert(metaDict['unitTo'])
            tablesToCommit.append(dataTable)
        
        return tablesToCommit, excludedTables
    
class PRIMAP_HIST(BaseImportTool):
    
    def __init__(self, version="v2.1_09-Nov-2019", year=2019):

        self.setup = setupStruct()
        
        self.setup.SOURCE_ID    = "PRIMAP_" + str(year)
        self.setup.SOURCE_NAME    = "PRIMAP"
        self.setup.SOURCE_YEAR    = str(year)
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/PRIMAP/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH +  str(year) + '/PRIMAP-hist_' + str(version) + '.csv'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        self.setup.LICENCE = 'CC BY-4.0'
        self.setup.URL     = 'https://dataservices.gfz-potsdam.de/pik/showshort.php?id=escidoc:4736895'

        
#        self.setup.INDEX_COLUMN_NAME = 'SeriesCode'
#        self.setup.SPATIAL_COLUM_NAME = 'GeoAreaCode'
#        
#        self.setup.COLUMNS_TO_DROP = ['Country Name', 'Indicator Name']
        self.setup.COLUMNS_TO_DROP = ['scenario', 'category', 'entity', 'unit', 'primary_code']

        
        self.createSourceMeta()
                
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
        else:
            self.mapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET, index_col=0)

    def createVariableMapping(self):
        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')                

        #%%
        
        if not hasattr(self, 'data'):
            self.loadData()
        
        meta = self.data.loc[~self.data.index.duplicated(keep='first')]
        scenario_mapping = {'HISTCR': 'Historic|country_reported', 'HISTTP': 'Historic|third_party'}
        self.mapping = pd.DataFrame.from_dict({
            'source': self.setup.SOURCE_ID,
            'scenario': meta['scenario'].replace(scenario_mapping),
            'category': meta['category'],
            'unit': (
                (meta['unit'] + ' ' +  meta['entity'])
                .where(meta['unit'] != 'GgCO2eq', 'Gg CO2eq') + '/yr'
            ),
            'entity': 'Emissions|' + meta['entity']
        })
        self.mapping = (
            self.mapping
            .assign(
                variable=self.mapping['entity'] + '|' + self.mapping['category'],
                pathway=self.mapping['scenario'],
                unitTo=self.mapping['unit'].str.replace('Gg', 'Mt')
            )
            .reindex(columns=pd.Index(MAPPING_COLUMNS).union(self.mapping.columns))
        )
        self.mapping.to_excel(writer, sheet_name=VAR_MAPPING_SHEET)
        

        sector_mapping = {'IPCM0EL':'National Total excluding LULUCF',
                        'IPC1':'Energy',
                        'IPC1A':'Fuel Combustion Activities',
                        'IPC1B':'Fugitive Emissions from Fuels',
                        'IPC1B1':'Solid Fuels',
                        'IPC1B2':'Oil and Natural Gas',
                        'IPC1B3':'Other Emissons from Energy Production',
                        'IPC1C':'Carbon Dioxide Transport and Storage (currently no data available)',
                        'IPC2':'Industrial Processes and Product Use',
                        'IPC2A':'Mineral Industry',
                        'IPC2B':'Chemical Industry',
                        'IPC2C':'Metal Industry',
                        'IPC2D':'Non-Energy Products from Fuels and Solvent Use',
                        'IPC2E':'Electronics Industry (no data available as the category is only used for fluorinated gases which are only resolved at the level of category IPC2)',
                        'IPC2F':'Product uses as Substitutes for Ozone Depleting Substances (no data available as the category is only used for fluorinated gases which are only resolved at the level of category IPC2)',
                        'IPC2G':'Other Product Manufacture and Use',
                        'IPC2H':'Other',
                        'IPCMAG':'Agriculture, sum of IPC3A and IPCMAGELV',
                        'IPC3A':'Livestock',
                        'IPCMAGELV':'Agriculture excluding Livestock',
                        'IPC4':'Waste',
                        'IPC5':'Other'}

        dataFrame = pd.DataFrame.from_dict({'alternative': pd.Series(sector_mapping)})
        dataFrame.to_excel(writer, sheet_name='sector_mapping')
        
        writer.close()
        
    def loadData(self):
         self.data = pd.read_csv(self.setup.DATA_FILE, header=0) 
         self.data['primary_code'] = self.data.index
         self.data.set_index(self.data['entity'] + '_' + self.data['category'] + '_' + self.data['scenario'], inplace=True)
         
    def gatherMappedData(self, spatialSubSet = None, updateTables = False):
        excludedTables = defaultdict(list)
        
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
        
        tablesToCommit  = []
        for idx, metaDf in self.mapping.iterrows():
            print(idx)
            
            metaDict = metaDf.to_dict()
            metaDict.update(
                source_name=self.setup.SOURCE_NAME,
                source_year=self.setup.SOURCE_YEAR,
            )
            
            if not updateTables:
                metaDict = dt.core._update_meta(metaDict)
                tableID = dt.core._createDatabaseID(metaDict)
                if dt.core.DB.tableExist(tableID):
                    excludedTables['exists'].append(tableID)
                    print('table exists')
                    print(tableID)
                    continue
                    
            metaDict['original code'] = idx

            dataframe = (
                self.data.loc[idx,:].set_index('country').drop(self.setup.COLUMNS_TO_DROP, axis=1)
                .astype(float)
                .dropna(axis=1, how='all')
            )

            dataTable = Datatable(dataframe, meta=metaDict)
            # possible required unit conversion
            if not pd.isna(metaDict.get('unitTo')):
                dataTable = dataTable.convert(metaDict['unitTo'])
            tablesToCommit.append(dataTable)
        
        return tablesToCommit, excludedTables

class CRF_DATA(BaseImportTool):
    def __init__(self, reportingYear):

        self.setup = setupStruct()
        self.year  = str(reportingYear)
        
        self.setup.SOURCE_ID    = "UNFCCC_CRF_" + str(reportingYear)
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/UNFCCC_CRF_' + str(reportingYear) + '/'
        self.setup.LICENCE = 'open access (UN)'
        self.setup.URL     = 'https://unfccc.int/process-and-meetings/transparency-and-reporting/reporting-and-review-under-the-convention/greenhouse-gas-inventories-annex-i-parties/national-inventory-submissions-' + str(reportingYear)
    
        self.mappingDict = dict()
        
        self.mappingDict['sectors'] ={'IPC0': '7',   #total
                                 'IPC1': '8',   #energy 
                                 'IPC1|Fuel_combustion':'9',
                                 'IPC1|Fuel_combustion|Energy_industries' : '10',
                                 'IPC1|Fuel_combustion|Manufacturing&construction':'11',
                                 'IPC1|Fuel_combustion|Transport':'12',
                                 'IPC1|Fuel_combustion|Other_sectors': '13',
                                 'IPC1|Fuel_combustion|Other': '14',
                                 'IPC1|Fugitive_emissions':'15',
                                 'IPC1|Fugitive_emissions|Solid':'16',
                                 'IPC1|Fugitive_emissions|Fluid&gaseous':'17',
                                 'IPC2': '19',
                                 'IPC2|Mineral_industry': '20',  #industry and product use
                                 'IPC2|Chemical_industry': '21',  #industry and product use
                                 'IPC2|Metal_industry': '22',  #industry and product use
                                 'IPC4': '48',  #waste
                                 'IPCMAG': '28',#agriculture
                                 'LULUCF': '39',#LULUCF
                                 'LULUCF|Forestland': '40',#LULUCF
                                 'LULUCF|Grassland': '41',#LULUCF
                                 'LULUCF|Cropland': '42',#LULUCF
                                 'LULUCF|Wetlands': '43',#LULUCF
                                 'LULUCF|Settlements': '44',#LULUCF
                                 'LULUCF|Harvested_wood_products': '46',#LULUCF
                                 'IPC5': '54' , #Other
                                 'Aviation': '58', #international
                                 'Marine': '59'} #international
        

        self.mappingDict['gases'] ={'KYOTOGHG_AR4': 'J',
                                    'CO2':   'B',   
                                    'CH4':   'C',
                                    'N2O':   'D',  
                                    'HFCs':  'E',
                                    'PFCs':  'F', 
                                    'SF6':   'G' }
    
    def prepareFolders(self):
        import zipfile
        import os
        #%%
        folder = self.setup.SOURCE_PATH
        fileList = os.listdir(folder)
        fileList = [file for file in fileList if '.zip' in file]
        
        for file in fileList:
            try:
                with zipfile.ZipFile(os.path.join(folder,file), 'r') as zipObj:
                   coISO = file.split('-')[0].upper()
                   # Extract all the contents of zip file in different directory
                   zipObj.extractall(os.path.join(folder,coISO))
            except:
                print('failed: {}'.format(file))
    
    def gatherMappedData(self):
        #%%
        dataTables = dict()
        countryList = list()
        folderList = [ name for name in os.listdir(self.setup.SOURCE_PATH) if os.path.isdir(os.path.join(self.setup.SOURCE_PATH, name)) ]
        for folder in folderList:
            coISO = folder
            countryPath = self.setup.SOURCE_PATH + folder + '/'
            try:
                countryList.append(dt.mapp.countries.codes.loc[coISO,'name'])
            except:
                countryList.append(coISO)   
            print(coISO)    
            
            
            fileList =  os.listdir(countryPath)
            for fileName in fileList:
                year = int(fileName.split('_')[2])
                setup = dict()
                setup['filePath']  = countryPath
                setup['fileName']  = fileName
                setup['sheetName'] = 'Summary2'
                
                reader = dt.io.ExcelReader(setup)
                
                for sector in self.mappingDict['sectors']:
                    for gas in self.mappingDict['gases']:
                        variable = 'Emissions|' + gas + '|' + sector
                        
                        if variable not in dataTables.keys():
                            #create table
                            meta = dict()
                            meta['entity']   = 'Emissions|' + gas
                            meta['category'] = sector
                            meta['scenario'] = 'Historic|country_reported'
                            meta['source']   = self.setup.SOURCE_ID
                            meta['unit']     = 'MtCO2eq'
                            dataTables[variable] = dt.Datatable(columns=list(range(1990,2017)), meta=meta)
                        try:    
                            dataTables[variable].loc[coISO,year] = reader.gatherValue(self.mappingDict['gases'][gas] + self.mappingDict['sectors'][sector]) / 1000
                        except:
                            pass
                
        import copy
        for gas in self.mappingDict['gases']:  
            if   'Emissions|' + gas + '|LULUCF' in dataTables.keys():          
                dataTables['Emissions|' + gas + '|IPCM0EL'] = dataTables['Emissions|' + gas + '|IPC0'] - dataTables['Emissions|' + gas + '|LULUCF'] # national total excluding lulucf
                dataTables['Emissions|' + gas + '|IPCM0EL'].meta = copy.copy(dataTables['Emissions|' + gas + '|IPC0'].meta)
                dataTables['Emissions|' + gas + '|IPCM0EL'].meta['category'] = "IPCM0EL"
                dataTables['Emissions|' + gas + '|IPC3'] = dataTables['Emissions|' + gas + '|IPCMAG'] + dataTables['Emissions|' + gas + '|LULUCF'] #AFOLU
                dataTables['Emissions|' + gas + '|IPC3'].meta = copy.copy(dataTables['Emissions|' + gas + '|IPC0'].meta)
                dataTables['Emissions|' + gas + '|IPC3'].meta['category'] = "IPCM3"
        
        #%%
        tablesToCommit = list()
        for key in dataTables.keys():
            dataTables[key] = dataTables[key].astype(float)
            tablesToCommit.append(dataTables[key])
        return tablesToCommit
            
class SDG_DATA_2019(BaseImportTool):
    def __init__(self):

        self.setup = setupStruct()
        
        self.setup.SOURCE_ID    = "SDG_DB_2019"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/SDG_DB_2019/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH + 'extract_05_2019.csv'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        self.setup.LICENCE = 'open access (UN)'
        self.setup.URL     = 'https://unstats.un.org/sdgs/indicators/database/'

        
        self.setup.INDEX_COLUMN_NAME = 'SeriesCode'
        self.setup.SPATIAL_COLUM_NAME = 'GeoAreaCode'
        
        self.setup.COLUMNS_TO_DROP = ['Country Name', 'Indicator Name']
        

        
        self.createSourceMeta()
                
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
        else:
            self.mapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=VAR_MAPPING_SHEET, index_col=0)




    def loadData(self):
         self.data = pd.read_csv(self.setup.DATA_FILE, header =0) 
         self.data['primary_code'] = self.data.index
         modifierColumns = [self.setup.INDEX_COLUMN_NAME] + list(self.data.columns[14:-1])
         modifierColumns.remove('[Reporting Type]')
         #self.data[modifierColumns] = self.data[modifierColumns].fillna('NaN')
         #self.data[modifierColumns].apply(lambda x: '_'.join(x), axis=1)
         #self.data[modifierColumns].astype(str).apply(lambda x: x.str.cat(sep='_'), axis=1)
         self.data.index = self.data[modifierColumns].fillna('').astype(str).apply(lambda x: '_'.join(filter(None, x)), axis=1)
         
    def createVariableMapping(self):
        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')                

        #%%
        
        if not hasattr(self, 'data'):
#            self.data = pd.read_csv(self.setup.DATA_FILE, encoding='utf8', engine='python', index_col = None, header =0, na_values='..')
#            self.data['combined'] = self.data[self.setup.INDEX_COLUMN_NAME].apply(lambda x: '_'.join(x), axis=1)
            self.loadData()
        
        
        #self.data[self.setup.INDEX_COLUMN_NAME].apply(lambda x: '_'.join(x), axis=1)
        availableSeries = self.data.index.unique()
        descrDf = self.data['SeriesDescription'].drop_duplicates()
        
        self.mapping = pd.DataFrame(index=availableSeries, columns = MAPPING_COLUMNS + ['description'])
        self.mapping.source = self.setup.SOURCE_ID
        self.mapping.scenario = 'historic'
        self.mapping.description = descrDf
        self.mapping.description = self.mapping.description.fillna(method='ffill')
        self.mapping.to_excel(writer, sheet_name=VAR_MAPPING_SHEET)
        writer.close()
        
    def gatherMappedData(self, spatialSubSet=None):
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
        
        indexDataToCollect = self.mapping.index[~pd.isnull(self.mapping['entity'])]
        
        tablesToCommit  = []
        for idx in indexDataToCollect:
            metaDf = self.mapping.loc[idx]
            print(idx)
            
            #print(metaDf[config.REQUIRED_META_FIELDS].isnull().all() == False)
            #print(metaData[self.setup.INDEX_COLUMN_NAME])
            
            
            metaDict = {key : metaDf[key] for key in config.REQUIRED_META_FIELDS.union({'unitTo'})}           
            
            metaDict['original code'] = idx
            #metaDict['original name'] = metaDf['Indicator Name']
            
            seriesIdx = idx

            dataframe = self.data.loc[seriesIdx, ['GeoAreaCode', 'TimePeriod', 'Value']]
            dataframe = dataframe.pivot(index='GeoAreaCode', columns='TimePeriod', values='Value')
            
            dataframe = dataframe.astype(float)
            
            newData= list()
            for iRow in range(len(dataframe)):
                ISO_ID = dt.mapp.getSpatialID(dataframe.index[iRow])
                if dataframe.index[iRow] == 1:
                    ISO_ID = "World"
                if ISO_ID:
                    newData.append(ISO_ID)
                else:
                    newData.append(pd.np.nan)
            dataframe.index = newData
           
            if spatialSubSet:
                spatIdx = dataframe.index.isin(spatialSubSet)
                dataframe = dataframe.loc[spatIdx]
            
            
            
            dataframe= dataframe.dropna(axis=1, how='all')
            dataframe= dataframe.loc[~pd.isna(dataframe.index)]
            dataTable = Datatable(dataframe, meta=metaDict)
            # possible required unit conversion
            if not pd.isna(metaDict['unitTo']):
                dataTable = dataTable.convert(metaDict['unitTo'])
            tablesToCommit.append(dataTable)
        
        return tablesToCommit   

class HOESLY2018(BaseImportTool):
    def __init__(self):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "HOESLY2018"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/HOESLY2018/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH + 'compiled_raw_hoesly.csv'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        self.setup.LICENCE = ' Creative Commons Attribution 3.0 License'
        self.setup.URL     = 'https://www.geosci-model-dev.net/11/369/2018/'
        
        self.setup.MODEL_COLUMN_NAME = 'model'
        self.setup.SCENARIO_COLUMN_NAME = 'scenario'
        self.setup.REGION_COLUMN_NAME   = 'region'
        self.setup.VARIABLE_COLUMN_NAME   = 'variable'
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
            print("no mapping file found")
        else:
            self.mapping = dict()
            
            
            for var in ['variable', 'scenario', 'model', 'region']:
                df = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=var +'_mapping', index_col=0)
                df = df.loc[~df.loc[:,var].isna()]
                self.mapping.update(df.to_dict())
            
        self.createSourceMeta()

    def loadData(self):
        self.data = pd.read_csv(self.setup.DATA_FILE,   index_col = None, header =0)
        
    def createVariableMapping(self):        
        
        # loading data if necessary
        if not hasattr(self, 'data'):        
            self.loadData()
        
        
        import numpy as np
 
        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')       
        
        #variables
        #index = self.data[self.setup.VARIABLE_COLUMN_NAME].unique()
        self.availableSeries = self.data.drop_duplicates('variable').set_index( self.setup.VARIABLE_COLUMN_NAME)['unit']
        self.mapping = pd.DataFrame(index=self.availableSeries.index, columns =  [ self.setup.VARIABLE_COLUMN_NAME])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping = self.mapping.sort_index()
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name=VAR_MAPPING_SHEET)
        
        #models
        index = np.unique(self.data[self.setup.MODEL_COLUMN_NAME].values)
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = [self.setup.MODEL_COLUMN_NAME])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping = self.mapping.sort_index()
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='model_mapping')

        #scenarios
        index = np.unique(self.data[self.setup.SCENARIO_COLUMN_NAME].values)
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = [self.setup.SCENARIO_COLUMN_NAME])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping = self.mapping.sort_index()
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='scenario_mapping')
        
        #region
        index = np.unique(self.data[self.setup.region_COLUMN_NAME].values)
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = [self.setup.REGION_COLUMN_NAME])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping = self.mapping.sort_index()
        
        for idx in self.mapping.index:
            iso = dt.util.identifyCountry(idx)
            if iso is not None:
                self.mapping.loc[idx,'region'] = iso
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='region_mapping')
        writer.close()


    def gatherMappedData(self, spatialSubSet = None, updateTables=False):
        #%%
        import tqdm
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
      
        tablesToCommit  = []
        metaDict = dict()
        metaDict['source'] = self.setup.SOURCE_ID
        excludedTables = dict()
        excludedTables['empty'] = list()
        excludedTables['error'] = list()
        excludedTables['exists'] = list()
        
        
        for model in self.mapping['model'].keys():
            tempMo = self.data.loc[self.data.model == model]
            for scenario in self.mapping['scenario'].keys():
                tempMoSc = tempMo.loc[self.data.scenario == scenario]
#                for variable in self.mapping['variable'].keys():
#                    tempMoScVa = tempMoSc.loc[self.data.variable == variable]    
                    
                tables = dt.interfaces.read_long_table(tempMoSc, list(self.mapping['variable'].keys()))
                for table in tables:
                    table.meta['category'] = ""
                    table.meta['source'] = self.setup.SOURCE_ID
                    table.index = table.index.map(self.mapping['region'])
                    
                    tableID = dt.core._createDatabaseID(table.meta)
                    if not updateTables:
                        if dt.core.DB.tableExist(tableID):
                            excludedTables['exists'].append(tableID)
                        else:
                            tablesToCommit.append(table)
        return tablesToCommit, excludedTables  

class VANMARLE2017(BaseImportTool):
    def __init__(self):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "VANMARLE2017"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/VANMARLE2017/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH + 'compiled_raw_vanmarle.csv'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        self.setup.LICENCE = ' Creative Commons Attribution 3.0 License'
        self.setup.URL     = 'https://www.geosci-model-dev.net/10/3329/2017/'
        
        self.setup.MODEL_COLUMN_NAME = 'model'
        self.setup.SCENARIO_COLUMN_NAME = 'scenario'
        self.setup.REGION_COLUMN_NAME   = 'region'
        self.setup.VARIABLE_COLUMN_NAME   = 'variable'
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
            print("no mapping file found")
        else:
            self.mapping = dict()
            
            
            for var in ['variable', 'scenario', 'model', 'region']:
                df = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=var +'_mapping', index_col=0)
                df = df.loc[~df.loc[:,var].isna()]
                self.mapping.update(df.to_dict())
            
        self.createSourceMeta()

    def loadData(self):
        self.data = pd.read_csv(self.setup.DATA_FILE,   index_col = None, header =0)
        
    def createVariableMapping(self):        
        
        # loading data if necessary
        if not hasattr(self, 'data'):        
            self.loadData()
        
        
        import numpy as np
 
        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')       
        
        #variables
        #index = self.data[self.setup.VARIABLE_COLUMN_NAME].unique()
        self.availableSeries = self.data.drop_duplicates('variable').set_index( self.setup.VARIABLE_COLUMN_NAME)['unit']
        self.mapping = pd.DataFrame(index=self.availableSeries.index, columns =  [ self.setup.VARIABLE_COLUMN_NAME])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping = self.mapping.sort_index()
        self.mapping.index.name = 'orignal'
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name=VAR_MAPPING_SHEET)
        
        #models
        index = np.unique(self.data[self.setup.MODEL_COLUMN_NAME].values)
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = [self.setup.MODEL_COLUMN_NAME])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping = self.mapping.sort_index()
        self.mapping.index.name = 'orignal'
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='model_mapping')

        #scenarios
        index = np.unique(self.data[self.setup.SCENARIO_COLUMN_NAME].values)
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = [self.setup.SCENARIO_COLUMN_NAME])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping = self.mapping.sort_index()
        self.mapping.index.name = 'orignal'
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='scenario_mapping')
        
        #region
        index = np.unique(self.data[self.setup.REGION_COLUMN_NAME].values)
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = [self.setup.REGION_COLUMN_NAME])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping = self.mapping.sort_index()
        self.mapping.index.name = 'orignal'
        for idx in self.mapping.index:
            iso = dt.util.identifyCountry(idx)
            if iso is not None:
                self.mapping.loc[idx,'region'] = iso
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='region_mapping')
        writer.close()


    def gatherMappedData(self, spatialSubSet = None, updateTables=False):
        #%%
        import tqdm
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
      
        tablesToCommit  = []
        metaDict = dict()
        metaDict['source'] = self.setup.SOURCE_ID
        excludedTables = dict()
        excludedTables['empty'] = list()
        excludedTables['error'] = list()
        excludedTables['exists'] = list()
        
        
        for model in self.mapping['model'].keys():
            tempMo = self.data.loc[self.data.model == model]
            for scenario in self.mapping['scenario'].keys():
                tempMoSc = tempMo.loc[tempMo.scenario == scenario]
#                for variable in self.mapping['variable'].keys():
#                    tempMoScVa = tempMoSc.loc[self.data.variable == variable]    
                
                for variable in list(self.mapping['variable'].keys()):
                    tempMoScVar =  tempMoSc.loc[tempMoSc.variable == variable]
                    tempMoScVar.unit = self.mapping['unit'][variable]
                    tables = dt.interfaces.read_long_table(tempMoScVar, [variable])
                    for table in tables:
                        table.meta['category'] = ""
                        table.meta['source'] = self.setup.SOURCE_ID
                        table.index = table.index.map(self.mapping['region'])
                        
                        tableID = dt.core._createDatabaseID(table.meta)
                        if not updateTables:
                            if dt.core.DB.tableExist(tableID):
                                excludedTables['exists'].append(tableID)
                            else:
                                tablesToCommit.append(table)
        return tablesToCommit, excludedTables  
                
        #%%
        
        
        
class APEC(BaseImportTool):
    
    """
    IRENA data import tool
    """
    def __init__(self, year):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "APEC_" + str(year)
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/APEC/' + str(year) + '/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH + 'compiled_raw_hoesly.csv'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        self.setup.LICENCE = '(c) 2019 Asia Pacific Economic Cooperation (APERC)'
        self.setup.URL     = 'https://www.apec.org/Publications/2019/05/APEC-Energy-Demand-and-Supply-Outlook-7th-Edition---Volume-I'
        
#        self.setup.INDEX_COLUMN_NAME = ['FLOW', 'PRODUCT']
#        self.setup.SPATIAL_COLUM_NAME = 'COUNTRY'
#        self.setup.COLUMNS_TO_DROP = [ 'PRODUCT','FLOW','combined']
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
#            self.createVariableMapping()
            print("no mapping file found")
        else:
            self.mapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name='APEC')
     
            self.spatialMapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name='spatial', index_col=0)
            self.spatialMapping = self.spatialMapping.loc[~pd.isnull(self.spatialMapping.mapping)]

        self.createSourceMeta()

    def addSpatialMapping(self):
        #EU
        mappingToCountries  = dict()
        #self.spatialMapping.loc['Memo: European Union-28'] = 'EU28'
#        mappingToCountries['ASEAN'] =  ['VNM', 'PHL', 'THA', 'SGP', 'MMR', 'IDN', 'KHM', 'BRN', 'MYS', 'LAO']        
#        dt.mapp.regions.addRegionToContext('WEO',mappingToCountries)

    def gatherMappedData(self, spatialSubSet = None):
        
        tablesToCommit  = dt.TableSet()
        setup = dict()
        setup['filePath']  = self.setup.SOURCE_PATH 
        setup['fileName']  = 'APEC_Energy_Outlook_7th_Edition_Tables.xlsx'
        
        
        # loop over energy mapping
        for region in self.spatialMapping.index:
            setup['sheetName'] = region
            setup['timeColIdx']  = ['AO:A0']
            setup['spaceRowIdx'] = ['AO:A0']
            
            ex = dt.io.ExcelReader(setup)
            coISO = self.spatialMapping.loc[region,'mapping']
            print(region, ex.gatherValue('B1') + '->' + coISO)
            continue
        
            for i, idx in enumerate(list(self.mapping.index)):
                
                metaDf = self.mapping.loc[idx,:]
                #print(metaDf['What'])
    
                #Capacity
                setup['timeColIdx']  = tuple(metaDf['Time'].split(':'))
                setup['spaceRowIdx'] = tuple([metaDf['What']])
                #print(metaDf[config.REQUIRED_META_FIELDS].isnull().all() == False)
                #print(metaData[self.setup.INDEX_COLUMN_NAME])
                
                ex.timeColIdx =  [dt.io.excelIdx2PandasIdx(x) for x in setup['timeColIdx']]
                ex.spaceRowIdx = [dt.io.excelIdx2PandasIdx(x) for x in setup['spaceRowIdx']]
#                if "International" in metaDf['Name']:
#                    sdf
#                if ex.spaceRowIdx[0][0]>41 and region != 'World':
#                    ex.spaceRowIdx = [(ex.spaceRowIdx[0][0]-1,0)]
                
                df = ex.gatherData()
                df.columns = df.columns.astype(int)
                metaDict = dict()
                metaDict['entity']   = metaDf['Name'].strip().replace('| ','|')
                metaDict['category'] = ''
                metaDict['unit']     =  metaDf['unit']   
                metaDict['scenario'] =  metaDf['Scenario']  
                metaDict['source']   = self.setup.SOURCE_ID
                metaDict['unitTo'] = metaDf['unitTo']
                ID = dt.core._createDatabaseID(metaDict)
                
                if ID not in tablesToCommit.keys():
                    table = dt.Datatable(columns = range(2000,2100), meta=metaDict)
                     
                    table.loc[coISO, df.columns] = df.values
                    tablesToCommit.add(table)
                else:
                    table = tablesToCommit[ID]
                    table.loc[coISO, df.columns] = df.values
                    
            
        
        tablesList = list()
        for ID in tablesToCommit.keys():
            dataTable = tablesToCommit[ID]
            print(dataTable.meta)
            if not pd.isna(dataTable.meta['unitTo']):
                dataTable = dataTable.convert(dataTable.meta['unitTo'])
                del dataTable.meta['unitTo']
            tablesList.append(dataTable.astype(float))
        
        return tablesList, []

class FAO(BaseImportTool):
    """
    FAO data import tool
    """
    def __init__(self, year=2019):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "FAO_" + str(year)
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/FAO_' + str(year) + '/'
        self.setup.DATA_FILE    = {'Emissions_Land_Use_' : os.path.join(self.setup.SOURCE_PATH, 'Emissions_Land_Use_Land_Use_Total_E_All_Data.csv'),
                                   'Emissions_Agriculture_' : os.path.join(self.setup.SOURCE_PATH, 'Emissions_Agriculture_Agriculture_total_E_All_Data.csv'),
                                   'Environment_Emissions_by_Sector_' : os.path.join(self.setup.SOURCE_PATH, 'Environment_Emissions_by_Sector_E_All_Data.csv'),
                                   'Environment_Emissions_intensities_' : os.path.join(self.setup.SOURCE_PATH, 'Environment_Emissions_intensities_E_All_Data.csv'),
                                   'Environment_LandCover_' : os.path.join(self.setup.SOURCE_PATH, 'Environment_LandCover_E_All_Data.csv'),
                                   'Environment_LandUse_'   : os.path.join(self.setup.SOURCE_PATH, 'Environment_LandUse_E_All_Data.csv'),
                                   'Inputs_LandUse_'        : os.path.join(self.setup.SOURCE_PATH, 'Inputs_LandUse_E_All_Data.csv')
                                   }

        self.setup.MAPPING_FILE = os.path.join(self.setup.SOURCE_PATH, 'mapping.xlsx')
        self.setup.LICENCE = 'Food and Agriculture Organization of the United Nations (FAO)'
        self.setup.URL     = 'http://www.fao.org/faostat/en/#data/GL'
#        self.setup.MODEL_COLUMN_NAME = 'model'
        self.setup.SCENARIO_COLUMN_NAME = 'scenario'
        self.setup.REGION_COLUMN_NAME   = 'region'
        self.setup.VARIABLE_COLUMN_NAME   = 'entity'        
#        self.setup.INDEX_COLUMN_NAME = ['FLOW', 'PRODUCT']
#        self.setup.SPATIAL_COLUM_NAME = 'COUNTRY'
#        self.setup.COLUMNS_TO_DROP = [ 'PRODUCT','FLOW','combined']
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
            print("no mapping file found")
        else:
            self.mapping = dict()
            for var in ['entity', 'scenario', 'region']:
                df = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=var +'_mapping', index_col=0)
                df = df.loc[~df.loc[:,var].isna()]
                self.mapping.update(df.to_dict())
        self.createSourceMeta()   


    def loadData(self):
        
        for i, fileKey in enumerate(self.setup.DATA_FILE.keys()):
#            print(fileKey)
            file = self.setup.DATA_FILE[fileKey]
            temp = pd.read_csv(file, encoding='utf8', engine='python',  index_col = None, header =0)
            temp.Element = temp.Element.apply(lambda x: fileKey + x )
            if i == 0:
                self.data = temp
            else:
                self.data = self.data.append(temp)
        
        
        
        self.data.loc[:,'region'] = self.data.Area
        self.data.loc[:,'entity'] = self.data.Element + '_' + self.data.Item
        self.data.loc[:,'scenario'] = 'Historic'
        self.data.loc[:,'model'] = ''
        
        newColumns = ['region', 'entity','scenario', 'model', 'Unit']
        self.timeColumns = list()
        for column in self.data.columns:
            if column.startswith('Y') and len(column) == 5:
                self.data.loc[:,int(column[1:])] = self.data.loc[:,column]
                newColumns.append(int(column[1:]))
                self.timeColumns.append(int(column[1:]))
            
        self.data = self.data.loc[:, newColumns]
        
    def createVariableMapping(self):        
        
        # loading data if necessary
        if not hasattr(self, 'data'):        
            self.loadData()
#        return None
        
        import numpy as np
 
        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')       
        
        #variables
        #index = self.data[self.setup.VARIABLE_COLUMN_NAME].unique()
        self.availableSeries = self.data.drop_duplicates('variable').set_index( self.setup.VARIABLE_COLUMN_NAME)['Unit']
        self.mapping = pd.DataFrame(index=self.availableSeries.index, columns =  [ self.setup.VARIABLE_COLUMN_NAME])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping = self.mapping.sort_index()
        self.mapping.index.name = 'orignal'
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name=VAR_MAPPING_SHEET)
        
        #models
#        index = np.unique(self.data[self.setup.MODEL_COLUMN_NAME].values)
#        
#        self.availableSeries = pd.DataFrame(index=index)
#        self.mapping = pd.DataFrame(index=index, columns = [self.setup.MODEL_COLUMN_NAME])
#        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
#        self.mapping = self.mapping.sort_index()
#        self.mapping.index.name = 'orignal'
#        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='model_mapping')

        #scenarios
        index = np.unique(self.data[self.setup.SCENARIO_COLUMN_NAME].values)
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = [self.setup.SCENARIO_COLUMN_NAME])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping = self.mapping.sort_index()
        self.mapping.index.name = 'orignal'
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='scenario_mapping')
        
        #region
        index = np.unique(self.data[self.setup.REGION_COLUMN_NAME].values)
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = [self.setup.REGION_COLUMN_NAME])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping = self.mapping.sort_index()
        self.mapping.index.name = 'orignal'
        for idx in self.mapping.index:
            iso = dt.util.identifyCountry(idx)
            if iso is not None:
                self.mapping.loc[idx,'region'] = iso
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='region_mapping')
        writer.close()


    def gatherMappedData(self, spatialSubSet = None, updateTables=False):
        #%%
        import tqdm
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
      
        tablesToCommit  = []
        metaDict = dict()
        metaDict['source'] = self.setup.SOURCE_ID
        excludedTables = dict()
        excludedTables['empty'] = list()
        excludedTables['error'] = list()
        excludedTables['exists'] = list()
        
        
        for model in ['']:
            tempMo = self.data
            
#            tempMo = self.data.loc[self.data.model == model]
            for scenario in self.mapping['scenario'].keys():
                tempMoSc = tempMo.loc[tempMo.scenario == scenario]
#                for variable in self.mapping['variable'].keys():
#                    tempMoScVa = tempMoSc.loc[self.data.variable == variable]    
                
                for variable in list(self.mapping['entity'].keys()):
                    tempMoScVar =  tempMoSc.loc[tempMoSc.entity == variable]
                    tempMoScVar.unit = self.mapping['unit'][variable]
#                    tables = dt.interfaces.read_long_table(tempMoScVar, [variable])

                    table = tempMoScVar.loc[:, self.timeColumns]
                    
                    table = Datatable(table, meta = {'entity': self.mapping['entity'][variable],
                                                     'category':self.mapping['category'][variable],
                                                     'scenario' : scenario,
                                                     'source' : self.setup.SOURCE_ID,
                                                     'unit' : self.mapping['unit'][variable]})
                    table.index = tempMoScVar.region
#                    table.meta['category'] = ""
#                    table.meta['source'] = 
                    table.index = table.index.map(self.mapping['region'])
                    
                    table = table.loc[~pd.isna(table.index),:]
                    
                    if not pd.isna(self.mapping['unitTo'][variable]):
                        print('conversion to : ' +str(self.mapping['unitTo'][variable]))
                        table = table.convert(self.mapping['unitTo'][variable])
                    
                    tableID = dt.core._createDatabaseID(table.meta)
                    if not updateTables:
                        if dt.core.DB.tableExist(tableID):
                            excludedTables['exists'].append(tableID)
                        else:
                            tablesToCommit.append(table)
                    else:
                        tablesToCommit.append(table)
        return tablesToCommit, excludedTables  

class WEO(BaseImportTool):
    """
    WEO data import tool
    """
    def __init__(self, year):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "WEO_" + str(year)
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/WEO/' + str(year) + '/'
        self.setup.DATA_FILE    = 'WEO' + str(year) + '_AnnexA.xlsx'
        self.setup.MAPPING_FILE = config.PATH_TO_DATASHELF + 'rawdata/WEO/' + str(year) + '/mapping_WEO_' + str(year) + '.xlsx'
        self.setup.LICENCE = 'IEA all rights reserved'
        self.setup.URL     = 'https://www.iea.org/weo/'
        
#        self.setup.INDEX_COLUMN_NAME = ['FLOW', 'PRODUCT']
#        self.setup.SPATIAL_COLUM_NAME = 'COUNTRY'
#        self.setup.COLUMNS_TO_DROP = [ 'PRODUCT','FLOW','combined']
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
#            self.createVariableMapping()
            print("no mapping file found")
        else:
            self.mappingEnergy = pd.read_excel(self.setup.MAPPING_FILE, sheet_name='Energy_Balance')
            self.mappingEmissions = pd.read_excel(self.setup.MAPPING_FILE, sheet_name='SI_CO2_Ind')
     
            self.spatialMapping = pd.read_excel(self.setup.MAPPING_FILE, sheet_name='spatial')

        self.createSourceMeta()

    def addSpatialMapping(self):
        #EU
        mappingToCountries  = dict()
        #self.spatialMapping.loc['Memo: European Union-28'] = 'EU28'
        mappingToCountries['ASEAN'] =  ['VNM', 'PHL', 'THA', 'SGP', 'MMR', 'IDN', 'KHM', 'BRN', 'MYS', 'LAO']        
        dt.mapp.regions.addRegionToContext('WEO',mappingToCountries)

    def gatherMappedData(self, spatialSubSet = None):
        
#%%
        tablesToCommit  = dt.TableSet()
        setup = dict()
        setup['filePath']  = self.setup.SOURCE_PATH 
        setup['fileName']  = self.setup.DATA_FILE
        
        
        # loop over energy mapping
        for region in self.spatialMapping.index:
            se7tup['sheetName'] = region + '_Balance'
            for i, idx in enumerate(list(self.mappingEnergy.index)):
#                print(i)
                metaDf = self.mappingEnergy.loc[idx,:]
                print(metaDf['What'])
                
                #Capacity
                setup['timeIdxList']  = tuple(metaDf['Time'].split(':'))
                setup['spaceIdxList'] = tuple([metaDf['What']])
                #print(metaDf[config.REQUIRED_META_FIELDS].isnull().all() == False)
                #print(metaData[self.setup.INDEX_COLUMN_NAME])
                
                if i == 0:
                    ex = dt.io.ExcelReader(setup)
                else:
                    ex.timeIdxList =  [dt.io.excelIdx2PandasIdx(x) for x in setup['timeIdxList']]
                    ex.spaceIdxList = [dt.io.excelIdx2PandasIdx(x) for x in setup['spaceIdxList']]
                    #print(ex.df)
#                if "International" in metaDf['Name']:
#                    sdf
                if ex.spaceIdxList[0][0]>41 and region != 'World':
                    ex.spaceIdxList = [(ex.spaceIdxList[0][0]-1,0)]
                
#                print(ex.setup())
                if i == 0:
                    df = ex.gatherData()
                else:
                    df = ex.gatherData(load=False)
                print(df)
                df = df.loc[:, yearsColumnsOnly(df)]
                df.columns = df.columns.astype(int)
                metaDict = dict()
                metaDict['entity']   = metaDf['Name'].strip().replace('| ','|')
                metaDict['category'] = ''
                metaDict['unit']     =  metaDf['unit']   
                metaDict['scenario'] =  metaDf['Scenario']  
                metaDict['source']   = self.setup.SOURCE_ID
                metaDict['unitTo'] = metaDf['unitTo']
                metaDict = dt.core._update_meta(metaDict)
                ID = dt.core._createDatabaseID(metaDict)
                coISO = self.spatialMapping.loc[region,'mapping']
                if ID not in tablesToCommit.keys():
                    table = dt.Datatable(columns = range(2000,2100), meta=metaDict)
                     
                    table.loc[coISO, df.columns] = df.values
                    tablesToCommit.add(table)
                else:
                    table = tablesToCommit[ID]
                    table.loc[coISO, df.columns] = df.values
                    
            # CO2 and emission indicators
            
            setup['sheetName'] = region + '_El_CO2_Ind'
            for i, idx in enumerate(list(self.mappingEmissions.index)):
                metaDf = self.mappingEmissions.loc[idx,:]
                print(metaDf['What'])
    
                #Capacity
                setup['timeIdxList']  = tuple(metaDf['Time'].split(':'))
                setup['spaceIdxList'] = tuple([metaDf['What']])
                #print(metaDf[config.REQUIRED_META_FIELDS].isnull().all() == False)
                #print(metaData[self.setup.INDEX_COLUMN_NAME])
                
                if i == 0:
                    ex = dt.io.ExcelReader(setup)
#                    asd
                else:
                    ex.timeIdxList =  [dt.io.excelIdx2PandasIdx(x) for x in setup['timeIdxList']]
                    ex.spaceIdxList = [dt.io.excelIdx2PandasIdx(x) for x in setup['spaceIdxList']]
#                if "International" in metaDf['Name']:
#                    sdf
                if ex.spaceIdxList[0][0]>51 and region != 'World':
                    ex.spaceIdxList = [(ex.spaceIdxList[0][0]-1,0)]
                
                if i == 0:
                    df = ex.gatherData()
                else:
                    df = ex.gatherData(load=False)
                print(df)
                df = df.loc[:, yearsColumnsOnly(df)]
                df.columns = df.columns.astype(int)
                metaDict = dict()
                metaDict['entity']   = metaDf['Name'].strip().replace('| ','|')
                metaDict['category'] = ''
                metaDict['unit']     =  metaDf['unit']   
                metaDict['scenario'] =  metaDf['Scenario']  
                metaDict['source']   = self.setup.SOURCE_ID
                metaDict['unitTo'] = metaDf['unitTo']
                
                metaDict = dt.core._update_meta(metaDict)
                ID = dt.core._createDatabaseID(metaDict)
                coISO = self.spatialMapping.loc[region,'mapping']
                if ID not in tablesToCommit.keys():
                    table = dt.Datatable(columns = range(2000,2100), meta=metaDict)
                     
                    table.loc[coISO, df.columns] = df.values
                    tablesToCommit.add(table)
                else:
                    table = tablesToCommit[ID]
                    table.loc[coISO, df.columns] = df.values

        
        tablesList = list()
        for ID in tablesToCommit.keys():
            dataTable = tablesToCommit[ID]
            print(dataTable.meta)
            if not pd.isna(dataTable.meta['unitTo']):
                dataTable = dataTable.convert(dataTable.meta['unitTo'])
                del dataTable.meta['unitTo']
            tablesList.append(dataTable.astype(float))
        
        return tablesList, []

#%% Enerdata
class ENERDATA(BaseImportTool):
    def __init__(self, year = 2019):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "ENERDATA_" + str(year)
        self.setup.SOURCE_PATH  = os.path.join(config.PATH_TO_DATASHELF,'rawdata', self.setup.SOURCE_ID)
        if year == 2019:
            self.setup.DATA_FILE    = os.path.join(self.setup.SOURCE_PATH, 'enerdata_2019_G2G.xlsx')
        elif year == 2020:
            self.setup.DATA_FILE    = os.path.join(self.setup.SOURCE_PATH, 'export_enerdata_1137124_050510.xlsx')
            self.setup.DATA_FILE    = os.path.join(self.setup.SOURCE_PATH, 'export_enerdata_1137124_113516.xlsx')
        
#        self.setup.DATA_FILE    = os.path.join(self.setup.SOURCE_PATH, 'export_enerdata_1137124_112738.xlsx')
        self.setup.MAPPING_FILE =  os.path.join(self.setup.SOURCE_PATH,'mapping_' + str(year) + '.xlsx')
        self.setup.LICENCE = ' Restricted use in the Brown 2 Green project only'
        self.setup.URL     = 'https://www.enerdata.net/user/?destination=services.html'
        
        self.setup.REGION_COLUMN_NAME   = 'ISO code'
        self.setup.VARIABLE_COLUMN_NAME   = 'Item code'
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
            print("no mapping file found")
        else:
            self.mapping = dict()
            
            
            for var in ['entity', 'region']:
                df = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=var +'_mapping', index_col=0)
                df = df.loc[~df.loc[:,var].isna()]
                self.mapping.update(df.to_dict())
            
        self.createSourceMeta()

    def loadData(self):
        self.data = pd.read_excel(self.setup.DATA_FILE,   index_col = None, header =0, na_values='n.a.')
        
        self.data.loc[:,'region'] = self.data.loc[:,self.setup.REGION_COLUMN_NAME]
        self.data.loc[:,'entity'] = self.data.loc[:,self.setup.VARIABLE_COLUMN_NAME]
        self.data.loc[:,'scenario'] = 'Historic'
        
        self.timeColumns = list()
        for col in self.data.columns:
            if isinstance(col,int):
                self.timeColumns.append(col)
#        self.data.loc[:,'model'] = ''
    def createVariableMapping(self):        
        #%%
        # loading data if necessary
        if not hasattr(self, 'data'):        
            self.loadData()
        
        
        import numpy as np
 
        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')       
        
        #variables
        #index = self.data[self.setup.VARIABLE_COLUMN_NAME].unique()
        self.availableSeries = self.data.drop_duplicates(self.setup.VARIABLE_COLUMN_NAME).set_index( self.setup.VARIABLE_COLUMN_NAME)[['Unit', 'Title']]
        self.mapping = pd.DataFrame(index=self.availableSeries.index, columns =  [ 'entity', 'category', 'unitTo'])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping = self.mapping.sort_index()
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name=VAR_MAPPING_SHEET)
        
        #models
#        index = np.unique(self.data[self.setup.MODEL_COLUMN_NAME].values)
#        
#        self.availableSeries = pd.DataFrame(index=index)
#        self.mapping = pd.DataFrame(index=index, columns = [self.setup.MODEL_COLUMN_NAME])
#        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
#        self.mapping = self.mapping.sort_index()
#        
#        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='model_mapping')

        #scenarios
#        index = np.unique(self.data[self.setup.SCENARIO_COLUMN_NAME].values)
#        
#        self.availableSeries = pd.DataFrame(index=index)
#        self.mapping = pd.DataFrame(index=index, columns = [self.setup.SCENARIO_COLUMN_NAME])
#        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
#        self.mapping = self.mapping.sort_index()
#        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='scenario_mapping')
        
        #region
        index = self.data[self.setup.REGION_COLUMN_NAME].unique()
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = ['region'])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping = self.mapping.sort_index()
        
        for idx in self.mapping.index:
            if not isinstance(idx,(str, int)):
                continue
            iso = dt.util.identifyCountry(idx)
            if iso is not None:
                self.mapping.loc[idx,'region'] = iso
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='region_mapping')
        writer.close()
        #%%

    def gatherMappedData(self, spatialSubSet = None, updateTables=False):
        #%%
        import tqdm
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
      
        tablesToCommit  = []
        metaDict = dict()
        metaDict['source'] = self.setup.SOURCE_ID
        excludedTables = dict()
        excludedTables['empty'] = list()
        excludedTables['error'] = list()
        excludedTables['exists'] = list()
        
        
#        for model in ['']:
#            tempMo = self.data
#            
##            tempMo = self.data.loc[self.data.model == model]
#            for scenario in self.mapping['scenario'].keys():
#                tempMoSc = tempMo.loc[tempMo.scenario == scenario]
##                for variable in self.mapping['variable'].keys():
##                    tempMoScVa = tempMoSc.loc[self.data.variable == variable]    
                
        for variable in list(self.mapping['entity'].keys()):
#            metaDf = self.mapping.loc[variable]
            tempMoScVar =  self.data.loc[self.data.entity == variable]
            tempMoScVar.unit = self.mapping['unit'][variable]
#                    tables = dt.interfaces.read_long_table(tempMoScVar, [variable])

            table = tempMoScVar.loc[:, self.timeColumns]
            
            table = Datatable(table, meta = {'entity': self.mapping['entity'][variable],
                                             'category':self.mapping['category'][variable],
                                             'scenario' : 'Historic',
                                             'source' : self.setup.SOURCE_ID,
                                             'unit' : self.mapping['unit'][variable]})
            table.index = tempMoScVar.region
#                    table.meta['category'] = ""
#                    table.meta['source'] = 
            table.index = table.index.map(self.mapping['region'])
            
            table = table.loc[~pd.isna(table.index),:]
            if not pd.isna(self.mapping['unitTo'][variable]):
                print('conversion to : ' +str(self.mapping['unitTo'][variable]))
                table = table.convert(self.mapping['unitTo'][variable])
            tableID = dt.core._createDatabaseID(table.meta)
            if not updateTables:
                if dt.core.DB.tableExist(tableID):
                    excludedTables['exists'].append(tableID)
                else:
                    tablesToCommit.append(table)
            else:
                tablesToCommit.append(table)
        return tablesToCommit, excludedTables  
   
    
#%%
class CAT_Paris_Sector_Rolllout(BaseImportTool):
   
    def __init__(self):
        self.setup = setupStruct()
        self.setup.SOURCE_ID    = "CAT_PSR_2019"
        self.setup.SOURCE_PATH  = config.PATH_TO_DATASHELF + 'rawdata/CAT_PSR_2019/'
        self.setup.DATA_FILE    = self.setup.SOURCE_PATH + 'portal_data_all_160620.csv'
        self.setup.MAPPING_FILE = self.setup.SOURCE_PATH + 'mapping.xlsx'
        self.setup.LICENCE = ' Creative Commons Attribution 3.0 License'
        self.setup.URL     = 'https://climateactiontracker.org/data-portal/'
        
        
        self.colums_to_process =  ['variable', 'scenario', 'region']
        
#        self.setup.MODEL_COLUMN_NAME = 'model'
        self.setup.SCENARIO_COLUMN_NAME = 'variable'
        self.setup.REGION_COLUMN_NAME   = 'country'
        self.setup.VARIABLE_COLUMN_NAME   = 'old_var'
        
        self.setup.columnMapping = {'variable' : 'entity',
                                   'region'   : 'region',
                                   'scenario' : 'scenario'}
        
        if not(os.path.exists(self.setup.MAPPING_FILE)):
            self.createVariableMapping()
            print("no mapping file found")
        else:
            self.mapping = dict()
            
            
            for var in self.colums_to_process:
                df = pd.read_excel(self.setup.MAPPING_FILE, sheet_name=var +'_mapping', index_col=0)
                df = df.loc[~df.loc[:,self.setup.columnMapping[var]].isna()]
                self.mapping.update(df.to_dict())
            
        self.createSourceMeta()

    def loadData(self):
        self.data = pd.read_csv(self.setup.DATA_FILE,   index_col = None, header =0)
        self.data.loc[:, 'old_var'] =  self.data.loc[:,['sector', 'indicator']].apply(lambda x: '_'.join(map(str, x)),axis=1)
        self.data.loc[:, 'scenario'] =  self.data.loc[:,'variable']
        self.data.loc[:, 'region'] =  self.data.loc[:,'country']
        self.data.loc[:, 'model'] = ''
        self.data.loc[:,'variable'] = self.data.loc[:,'old_var']
    def createVariableMapping(self):        
        
        # loading data if necessary
        if not hasattr(self, 'data'):        
            self.loadData()
        
        
        import numpy as np
 
        writer = pd.ExcelWriter(self.setup.MAPPING_FILE,
                    engine='xlsxwriter',
                    datetime_format='mmm d yyyy hh:mm:ss',
                    date_format='mmmm dd yyyy')       
        
        #variables
        #index = self.data[self.setup.VARIABLE_COLUMN_NAME].unique()
        self.availableSeries = self.data.drop_duplicates(self.setup.VARIABLE_COLUMN_NAME).set_index( self.setup.VARIABLE_COLUMN_NAME)['unit']
        self.mapping = pd.DataFrame(index=self.availableSeries.index, columns =  [ 'enitty', 'category'])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping = self.mapping.sort_index()
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name=VAR_MAPPING_SHEET)
        
        #models
#        index = np.unique(self.data[self.setup.MODEL_COLUMN_NAME].values)
        
#        self.availableSeries = pd.DataFrame(index=index)
#        self.mapping = pd.DataFrame(index=index, columns = [self.setup.MODEL_COLUMN_NAME])
#        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
#        self.mapping = self.mapping.sort_index()
#        
#        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='model_mapping')

        #scenarios
        index = np.unique(self.data[self.setup.SCENARIO_COLUMN_NAME].values)
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = [self.setup.SCENARIO_COLUMN_NAME])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping = self.mapping.sort_index()
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='scenario_mapping')
        
        #region
        index = np.unique(self.data[self.setup.REGION_COLUMN_NAME].values)
        
        self.availableSeries = pd.DataFrame(index=index)
        self.mapping = pd.DataFrame(index=index, columns = [self.setup.REGION_COLUMN_NAME])
        self.mapping = pd.concat([self.mapping, self.availableSeries], axis=1)
        self.mapping = self.mapping.sort_index()
        
        for idx in self.mapping.index:
            iso = dt.util.identifyCountry(idx)
            if iso is not None:
                self.mapping.loc[idx,'region'] = iso
        
        self.mapping.to_excel(writer, engine='openpyxl', sheet_name='region_mapping')
        writer.close()


    def gatherMappedData(self, spatialSubSet = None, updateTables=False):
        #%%
        import tqdm
        # loading data if necessary
        if not hasattr(self, 'data'):
            self.loadData()        
      
        tablesToCommit  = []
        metaDict = dict()
        metaDict['source'] = self.setup.SOURCE_ID
        excludedTables = dict()
        excludedTables['empty'] = list()
        excludedTables['error'] = list()
        excludedTables['exists'] = list()
        
#        self.data = self.data

        for scenario in self.mapping['scenario'].keys():
            tempMoSc = self.data.loc[self.data.scenario == scenario]
            for variable in self.mapping['entity'].keys():
                tempMoScVa = tempMoSc.loc[tempMoSc.variable == variable]    
#                for category in self.mapping['category'].keys():
#                tempMoScVa = tempMoScVa.loc[tempMoScVa.variable == category]
                tempMoScVa = tempMoScVa.loc[:,['unit', 'model', 'scenario', 'year', 'region', 'value', 'variable']]
                tempMoScVa.loc[:,'unit'] = self.mapping['unit'][variable]
                tempMoScVa.loc[:,'scenario'] = self.mapping['scenario'][scenario]
##                    dfg
                tables = dt.interfaces.read_long_table(tempMoScVa, [variable])
                for table in tables:
                    table.meta['entity'] = self.mapping['entity'][variable]
                    table.meta['category'] = self.mapping['category'][variable]
                    table.meta['scenario'] = self.mapping['scenario'][scenario]
                    table.meta['source'] = self.setup.SOURCE_ID
                    table.index = table.index.map(self.mapping['region'])
                    
                    tableID = table.generateTableID()
                    if not updateTables:
                        if dt.core.DB.tableExist(tableID):
                            excludedTables['exists'].append(tableID)
                        else:
                            tablesToCommit.append(table)
        return tablesToCommit, excludedTables  

     
#%%
def HDI_import(year=2020):
    sourceMeta = {'SOURCE_ID': 'HDI_' + str(year),
                  'collected_by' : 'AG',
                  'date': dt.core.getDateString(),
                  'source_url' : 'http://hdr.undp.org/en/data',
                  'licence': 'open source' }
    
    SOURCE_PATH = os.path.join(dt.config.PATH_TO_DATASHELF, 'rawdata/', sourceMeta['SOURCE_ID'])
    data = pd.read_csv(os.path.join(SOURCE_PATH, "Human Development Index (HDI).csv"), na_values='..')
    
    yearColumns = dt.util.yearsColumnsOnly(data)
    
    data = data.loc[:,yearColumns]
    
#    regionMapping = {x:y for x,y in zip(list(data.loc[:,'Country']), list(data.loc[:,'Country'].map(lambda x : dt.getCountryISO(str(x)))))}
    regionMapping = {
         ' Afghanistan': 'AFG',
         ' Albania': 'ALB',
         ' Algeria': 'DZA',
         ' Andorra': 'AND',
         ' Angola': 'AGO',
         ' Antigua and Barbuda': 'ATG',
         ' Argentina': 'ARG',
         ' Armenia': 'ARM',
         ' Australia': 'AUS',
         ' Austria': 'AUT',
         ' Azerbaijan': 'AZE',
         ' Bahamas': 'BHS',
         ' Bahrain': 'BHR',
         ' Bangladesh': 'BGD',
         ' Barbados': 'BRB',
         ' Belarus': 'BLR',
         ' Belgium': 'BEL',
         ' Belize': 'BLZ',
         ' Benin': 'BEN',
         ' Bhutan': 'BTN',
         ' Bolivia (Plurinational State of)': 'BOL',
         ' Bosnia and Herzegovina': 'BIH',
         ' Botswana': 'BWA',
         ' Brazil': 'BRA',
         ' Brunei Darussalam': 'BRN',
         ' Bulgaria': 'BGR',
         ' Burkina Faso': 'BFA',
         ' Burundi': 'BDI',
         ' Cabo Verde': 'CPV',
         ' Cambodia': 'KHM',
         ' Cameroon': 'CMR',
         ' Canada': 'CAN',
         ' Central African Republic': 'CAF',
         ' Chad': 'TCD',
         ' Chile': 'CHL',
         ' China': 'CHN',
         ' Colombia': 'COL',
         ' Comoros': 'COM',
         ' Congo': 'COG',
         ' Congo (Democratic Republic of the)': 'COD',
         ' Costa Rica': 'CRI',
         ' Croatia': 'HRV',
         ' Cuba': 'CUB',
         ' Cyprus': 'CYP',
         ' Czechia': 'CZE',
         " Côte d'Ivoire": 'CIV',
         ' Denmark': 'DNK',
         ' Djibouti': 'DJI',
         ' Dominica': 'DMA',
         ' Dominican Republic': 'DOM',
         ' Ecuador': 'ECU',
         ' Egypt': 'EGY',
         ' El Salvador': 'SLV',
         ' Equatorial Guinea': 'GNQ',
         ' Eritrea': 'ERI',
         ' Estonia': 'EST',
         ' Eswatini (Kingdom of)': 'SWZ',
         ' Ethiopia': 'ETH',
         ' Fiji': 'FJI',
         ' Finland': 'FIN',
         ' France': 'FRA',
         ' Gabon': 'GAB',
         ' Gambia': 'GMB',
         ' Georgia': 'GEO',
         ' Germany': 'DEU',
         ' Ghana': 'GHA',
         ' Greece': 'GRC',
         ' Grenada': 'GRD',
         ' Guatemala': 'GTM',
         ' Guinea': 'GIN',
         ' Guinea-Bissau': 'GNB',
         ' Guyana': 'GUY',
         ' Haiti': 'HTI',
         ' Honduras': 'HND',
         ' Hong Kong, China (SAR)': 'HKG',
         ' Hungary': 'HUN',
         ' Iceland': 'ISL',
         ' India': 'IND',
         ' Indonesia': 'IDN',
         ' Iran (Islamic Republic of)': 'IRN',
         ' Iraq': 'IRQ',
         ' Ireland': 'IRL',
         ' Israel': 'ISR',
         ' Italy': 'ITA',
         ' Jamaica': 'JAM',
         ' Japan': 'JPN',
         ' Jordan': 'JOR',
         ' Kazakhstan': 'KAZ',
         ' Kenya': 'KEN',
         ' Kiribati': 'KIR',
         ' Korea (Republic of)': 'KOR',
         ' Kuwait': 'KWT',
         ' Kyrgyzstan': 'KGZ',
         " Lao People's Democratic Republic": 'LAO',
         ' Latvia': 'LVA',
         ' Lebanon': 'LBN',
         ' Lesotho': 'LSO',
         ' Liberia': 'LBR',
         ' Libya': 'LBY',
         ' Liechtenstein': 'LIE',
         ' Lithuania': 'LTU',
         ' Luxembourg': 'LUX',
         ' Madagascar': 'MDG',
         ' Malawi': 'MWI',
         ' Malaysia': 'MYS',
         ' Maldives': 'MDV',
         ' Mali': 'MLI',
         ' Malta': 'MLT',
         ' Marshall Islands': 'MHL',
         ' Mauritania': 'MRT',
         ' Mauritius': 'MUS',
         ' Mexico': 'MEX',
         ' Micronesia (Federated States of)': 'FSM',
         ' Moldova (Republic of)': 'MDA',
         ' Mongolia': 'MNG',
         ' Montenegro': 'MNE',
         ' Morocco': 'MAR',
         ' Mozambique': 'MOZ',
         ' Myanmar': 'MMR',
         ' Namibia': 'NAM',
         ' Nepal': 'NPL',
         ' Netherlands': 'NLD',
         ' New Zealand': 'NZL',
         ' Nicaragua': 'NIC',
         ' Niger': 'NER',
         ' Nigeria': 'NGA',
         ' North Macedonia': 'MKD',
         ' Norway': 'NOR',
         ' Oman': 'OMN',
         ' Pakistan': 'PAK',
         ' Palau': 'PLW',
         ' Palestine, State of': 'PSE',
         ' Panama': 'PAN',
         ' Papua New Guinea': 'PNG',
         ' Paraguay': 'PRY',
         ' Peru': 'PER',
         ' Philippines': 'PHL',
         ' Poland': 'POL',
         ' Portugal': 'PRT',
         ' Qatar': 'QAT',
         ' Romania': 'ROU',
         ' Russian Federation': 'RUS',
         ' Rwanda': 'RWA',
         ' Saint Kitts and Nevis': 'KNA',
         ' Saint Lucia': 'LCA',
         ' Saint Vincent and the Grenadines': 'VCT',
         ' Samoa': 'WSM',
         ' Sao Tome and Principe': 'STP',
         ' Saudi Arabia': 'SAU',
         ' Senegal': 'SEN',
         ' Serbia': 'SRB',
         ' Seychelles': 'SYC',
         ' Sierra Leone': 'SLE',
         ' Singapore': 'SGP',
         ' Slovakia': 'SVK',
         ' Slovenia': 'SVN',
         ' Solomon Islands': 'SLB',
         ' South Africa': 'ZAF',
         ' South Sudan': 'SSD',
         ' Spain': 'ESP',
         ' Sri Lanka': 'LKA',
         ' Sudan': 'SDN',
         ' Suriname': 'SUR',
         ' Sweden': 'SWE',
         ' Switzerland': 'CHE',
         ' Syrian Arab Republic': 'SYR',
         ' Tajikistan': 'TJK',
         ' Tanzania (United Republic of)': 'TZA',
         ' Thailand': 'THA',
         ' Timor-Leste': 'TLS',
         ' Togo': 'TGO',
         ' Tonga': 'TON',
         ' Trinidad and Tobago': 'TTO',
         ' Tunisia': 'TUN',
         ' Turkey': 'TUR',
         ' Turkmenistan': 'TKM',
         ' Uganda': 'UGA',
         ' Ukraine': 'UKR',
         ' United Arab Emirates': 'ARE',
         ' United Kingdom': 'GBR',
         ' United States': 'USA',
         ' Uruguay': 'URY',
         ' Uzbekistan': 'UZB',
         ' Vanuatu': 'VUT',
         ' Venezuela (Bolivarian Republic of)': 'VEN',
         ' Viet Nam': 'VNM',
         ' Yemen': 'YEM',
         ' Zambia': 'ZMB',
         ' Zimbabwe': 'ZWE',
         'Human Development': None,
         'Very high human development': None,
         'High human development': None,
         'Medium human development': None,
         'Low human development': None,
         'Developing Countries': None,
         'Regions': None,
         'Arab States': None,
         'East Asia and the Pacific': None,
         'Europe and Central Asia': None,
         'Latin America and the Caribbean': None,
         'South Asia': None,
         'Sub-Saharan Africa': None,
         'Least Developed Countries': None,
         'Small Island Developing States': None,
         'Organization for Economic Co-operation and Development': None,
         'World': 'World'}
    
    data.index = data.loc[:,'Country'].map(regionMapping)
    data = data.loc[~data.index.isnull(),:].astype(float)
    
    data.index[data.index.duplicated()]
    
    meta =  {'entity'   : 'HDI_Human_development_index',
             'scenario' : 'Historic', 
             'unit'     : 'dimensionless',
             'source'   : sourceMeta['SOURCE_ID']}
    table = dt.Datatable(data, meta=meta)
    table.generateTableID()
    
    dt.commitTables([table], 'UNWPP2017 data', sourceMeta)
    
    
#    def 
    #%%
def UN_WPP_2019_import():
    sourceMeta = {'SOURCE_ID': 'UN_WPP2019',
                          'collected_by' : 'AG',
                          'date': dt.core.getDateString(),
                          'source_url' : 'https://population.un.org/wpp/Download/Standard/Population/',
                          'licence': 'open source' }
        
    mappingDict = {int(x) : y for x,y  in zip(dt.mapp.countries.codes.numISO, dt.mapp.countries.codes.index) if not(pd.np.isnan(x))}
    mappingDict[900] = 'World'
    SOURCE = "UN_WPP2019"
    SOURCE_PATH = dt.config.PATH_TO_DATASHELF + 'rawdata/UN_WPP2019/'
    metaSetup = {'source'   : SOURCE,
                 'entity'   : 'population',
                 'unit'     : 'thousands',
                 'category' : 'total'}
    
    # change setup
    excelSetup = dict()
    excelSetup['filePath']  = SOURCE_PATH
    excelSetup['fileName']  = 'WPP2019_POP_F01_1_TOTAL_POPULATION_BOTH_SEXES.xlsx'
    excelSetup['sheetName'] = 'ESTIMATES'
    excelSetup['timeColIdx']  = ('H17', 'CJ17')
    excelSetup['spaceRowIdx'] = ('E18', 'E306')
    
    tables = list()
    
    # gather historic data
    #        itool = UN_WPP(excelSetup)
    metaSetup['scenario'] = 'historic'
    extractor = dt.io.ExcelReader(excelSetup)
    table = extractor.gatherData()
    table= table.replace('…',pd.np.nan)
    table['newIndex'] = table.index
    table['newIndex'] = table.index.to_series().map(mappingDict)
    table.loc[pd.isnull(table['newIndex']), 'newIndex'] = table.index[pd.isnull(table['newIndex'])]
    table = table.set_index('newIndex')
    newIdx = [mappingDict[x] for x in table.index if x in mappingDict.keys()]
    tables.append(dt.Datatable(table, meta = metaSetup))
    
    
    #gather projectinos
    #excelSetup['timeColIdx']  = ('F17', 'CW17')
    
    scenDict = {'PROJECTION_LOW': 'LOW VARIANT',
                'PROJECTION_MED': 'MEDIUM VARIANT',
                'PROJECTION_HI': 'HIGH VARIANT'}
    #itool = UN_WPP(excelSetup)
    
    for scenario, sheetName in scenDict.items():
        metaSetup['scenario'] = scenario
        excelSetup['sheetName'] = sheetName
        extractor = dt.io.ExcelReader(excelSetup)
        table = extractor.gatherData()
        table= table.replace('…',pd.np.nan)
        table['newIndex'] = table.index
        table['newIndex'] = table.index.to_series().map(mappingDict)
        table.loc[pd.isnull(table['newIndex']), 'newIndex'] = table.index[pd.isnull(table['newIndex'])]
        table = table.set_index('newIndex')
        tables.append(dt.Datatable(table, meta = metaSetup))
    #%%
    def add_EU(table):
        EU_COUNTRIES = list(dt.mapp.regions.EU28.membersOf('EU28'))
        table.loc['EU28'] = table.loc[EU_COUNTRIES].sum()
        return(table)
    
    tables = [add_EU(table) for table in tables]
    
    dt.commitTables(tables, 'UNWPP2017 data', sourceMeta, append_data=True)
    return tables



#%% 
sources = sourcesStruct()
_sourceClasses = [IEA_World_Energy_Balance, IEA_WEB_2018, ADVANCE_DB, IAMC15_2019, IRENA2019,
                  SSP_DATA, SDG_DATA_2019, AR5_DATABASE, IEA_FUEL_2019, PRIMAP_HIST, SDG_DATA_2019,
                  CRF_DATA, WDI_2020, APEC, WEO, VANMARLE2017, HOESLY2018, FAO, LED_2019, IMAGE15_2020]

nSourceReader = 0
for _sourceClass in _sourceClasses:
    try:
        _source = _sourceClass()
        sources[_source.setup.SOURCE_ID] = _source
        nSourceReader +=1
    except:
        pass
print('{} source reader found and added into "datatoolbox.sources".'.format(nSourceReader))
        

if config.DEBUG:
    print('Raw sources loaded in {:2.4f} seconds'.format(time.time()-tt))



if __name__ == '__main__':
#%% PRIMAP HIST
    primap = PRIMAP_HIST(2019)
#    tableList, excludedTables = primap.gatherMappedData()
#    dt.commitTables(tableList, 'PRIMAP 2019 update', primap.meta)
#%% PRIMAP DOWNSCALE
    primap_down = PRIMAP_DOWNSCALE()
#    tableList, excludedTables = primap_down.gatherMappedData()
#    dt.commitTables(tableList, 'PRIMAP DOWNSCALING 2020', primap_down.meta)
#    asdf1s
#%% CRF data
    crf_data = CRF_DATA(2020)
    #iea = IEA2016()
#    tableList = crf_data.gatherMappedData()
#    crf_data.createSourceMeta()
#    dt.commitTables(tableList, 'CRF_data_2020', crf_data.meta, update=True)
#    sdf
#%% ADVANCE DB
    advance = ADVANCE_DB()
#    iea = IEA2016()
#    tableList, excludedTables = advance.gatherMappedData()
#    dt.commitTables(tableList, 'ADVANCE DB IAM data', advance.meta)
#%%WDI data
    wdi = WDI_2020()    
#    tableList = wdi.gatherMappedData(updateTables=True)
#    
##    iea.openMappingFile()
#    dt.commitTables(tableList, 'Added WDI 2020  data', wdi.meta, update=True)
#    sdf
#%%IEA World Energy Balance
    iea19 = IEA_World_Energy_Balance(2020)
#    iea19.createVariableMapping()
#    iea19.addSpatialMapping()
#    tableList, excludedTables = iea19.gatherMappedData(updateTables=True)
#    dt.commitTables(tableList, 'IEA2020 World balance update', iea19.meta,update=True)
#    sdf
#    iea16 = IEA2016()
#    iea18 = IEA_WEB_2018()
#    iea18.addSpatialMapping()
#    tableList, excludedTables = iea18.gatherMappedData(updateTables=True)
#    dt.commitTables(tableList, 'IEA2018 World balance update', iea18.meta)
#    tableIDs = [table.ID for table in tableList]
#    tableList = [dt.tools.cleanDataTable(table) for table in tableList]
#    dt.updateTables( tableIDs[0:1], tableList[0:1], 'update of tables')
#    dt.updateTables( [table.ID], [table], 'update of tables')
#%% IEA emissions
    ieaEmissions = IEA_FUEL_2019()
#    tableList, excludedTables = ieaEmissions.gatherMappedData(updateTables=True)
#    dt.commitTables(tableList, 'IEA fuel emission data', ieaEmissions.meta, update=True)
#    ddsa
#%% IEA emissions detailed
    ieaEmissions_detailed = IEA_FUEL_DETAILED_2019()
#    tableList, excludedTables = ieaEmissions_detailed.gatherMappedData(updateTables=True)
#    dt.commitTables(tableList, 'IEA fuel emission detailed data', ieaEmissions.meta, update=True)
    
#%% IRENA data
    irena19 = IRENA2019()
#    tableList = irena19.gatherMappedData()
#    dt.commitTables(tableList, 'IRENA 2019 new data', irena19.meta)
#    dt.updateTables()
#%% SDG_DB data
    sdg2019 = SDG_DATA_2019()
#    tableList = sdg2019.gatherMappedData()
#    dat.commitTables(tableList, 'SDG_DB 2019 data', sdg2019.meta)    

#%% AIM DATA

    aim = AIM_SSP_DATA_2019()
#    tableList, excludedTables = aim.gatherMappedData(updateTables=True)
#    aim.createSourceMeta()
#    dt.commitTables(tableList, 'update AIM 1.5 data R20', aim.meta, update=True)
    
#%% IAMC DATA

    iamc = IAMC15_2019()    
#    tableList, excludedTables = iamc.gatherMappedData(updateTables=False)
##    iamc.createSourceMeta()
#    dt.commitTables(tableList, 'update IAM 1.5 data R20', iamc.meta, update=True)
#    sad
#%% CD LINKS

    cdlinks = CDLINKS_2018()    
#    tableList, excludedTables = cdlinks.gatherMappedData(updateTables=False)
#    cdlinks.createSourceMeta()
#    dt.commitTables(tableList, 'update CD Linksdata ', cdlinks.meta, update=False)

#%% IAMC CMPI6

    cmip6 = IAMC_CMIP6()    
#    tableList, excludedTables = cmip6.gatherMappedData(updateTables=False)
#    cmip6.createSourceMeta()
#    dt.commitTables(tableList, 'added CMIP6 dataset', cmip6.meta, update=False)
#    sadf
#%% SSPDB 2013
    
    ssp2013 = SSP_DATA()
    tableList, excludedTables = ssp2013.gatherMappedData(updateTables=True)
    dt.commitTables(tableList, 'SSP Database data added', ssp2013.meta, update=True)
#    for countryCode in tableList[0].index:
#        country = pycountry.countries.get(name = countryCode)
#        if country is not None:
#            print(countryCode + ': ' + country.alpha_3)
#        else:
#            print(countryCode + ' not found')
    
#%% AR5
    ar5_db = AR5_DATABASE()
#    tableList, excludedTables = ar5_db.gatherMappedData()
#    dt.commitTables(tableList, 'AR5  data added', ar5_db.meta)
#%% WEO
    weo = WEO(2020)
#    tableList, excludedTables = weo.gatherMappedData()
#    dt.commitTables(tableList, 'WEO  data updated', weo.meta, update=True)  
    
#%% FAO
    fao = FAO(2020)
#    tableList, excludedTables = fao.gatherMappedData(updateTables=True)
#    dt.commitTables(tableList, 'FAO  data added', fao.meta, update=True)  
    
#%% APEC
    apec = APEC(2019)
#    tableList, excludedTables = apec.gatherMappedData()
    #dt.commitTables(tableList, 'AR5  data added', apec.meta) 

#%% hoesley
    hoesley = HOESLY2018()
#    tableList, excludedTables = hoesley.gatherMappedData()
#    dt.commitTables(tableList, 'Hoesley data updated', hoesley.meta, update=False)  
#%% VANMARLE2017
    vanmarle = VANMARLE2017()
#    tableList, excludedTables = vanmarle.gatherMappedData()
#    dt.commitTables(tableList, 'vanmarle data updated', vanmarle.meta, update=False)  
#%% Enerdata
    enerdata = ENERDATA(2019)
#    tableList, excludedTables = enerdata.gatherMappedData(updateTables=True)
#    dt.commitTables(tableList, 'enerdata data updated', enerdata.meta, update=True)  
    #%%
    enerdata = ENERDATA(2020)
#    tableList2020, excludedTables = enerdata.gatherMappedData(updateTables=True)
#    dt.commitTables(tableList2020, 'enerdata data updated', enerdata.meta, update=True)  
    
#%% CAT Paris sector Rollout
    cat_psr = CAT_Paris_Sector_Rolllout()
#    tableList, excludedTables = cat_psr.gatherMappedData()
#    dt.commitTables(tableList, 'CAT PSR data', cat_psr.meta, update=False)  
    #%%
    sdf
    i = 66
    
    table19 = tableList[i]
    table20 = tableList2020[i]
    print(table19.meta['variable'])
    table19 -table20
        
    #%%
##################################################################
#    helper funtions
##################################################################  
def Anne_extract()  :  
    wdi = WDI_2018()
    tableList = wdi.gatherMappedData()
    LDC_list =["AGO", "BEN", "BFA", "BDI", "CAF", "TCD", "COM", "COD", "DJI", "ERI",
      "ETH", "GMB", "GIN", "GNB", "LSO", "LBR", "MDG", "MWI", "MLI", "MRT",
      "MOZ", "NER", "RWA", "STP", "SEN", "SLE", "SOM", "SSD", "SDN", "TZA",
      "TGO", "UGA", "ZMB",
      # Asia
      "AFG", "BGD", "BTN", "KHM", "TLS", "LAO", "MMR", "NPL", "YEM",
      # Oceania
      "KIR", "SLB", "TUV", "VUT",
      # The Americas
      "HTI"]  
    LDC_list.append('LDC')  
    LDC_list.append('WLD')
    #%%
    filteredTable = list()
    for table in tableList:
        filteredTable.append(table.filter(LDC_list))
    
    writer = pd.ExcelWriter('wdi_extract.xlsx',
                            engine='xlsxwriter',
                            datetime_format='mmm d yyyy hh:mm:ss',
                            date_format='mmmm dd yyyy')
    writer.close()
    
    for table in filteredTable:
    
        if table.meta['unit'] == 'USD':
            table = table.convert('millions USD')
        table.to_excel('wdi_extract.xlsx', sheetName=table.generateTableID()[:30],append=True)
    
def IEA_mapping_generation():
    path= '/media/sf_Documents/datashelf/rawdata/IEA2018/'
    os.chdir(path)
    df= pd.read_csv('World_Energy_Balances_2018_clean.csv',encoding="ISO-8859-1", engine='python', index_col = None, header =0, na_values='..')

#%%

            
