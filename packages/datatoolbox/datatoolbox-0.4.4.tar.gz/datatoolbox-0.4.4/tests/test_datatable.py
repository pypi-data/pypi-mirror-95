#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 09:30:40 2020

@author: ageiges
"""
import datatoolbox as dt
import numpy as np


def test_creation():
    metaDict = {'source' : 'TEST',
                'entity' : 'values',
                'unit' : 'm'}
    metaDict2 = {'source' : 'TEST2',
                'entity' : 'area',
                'unit' : 'km'}    
        
    data = np.asarray([[1,2.2,3,4 ],
                       [2.3, np.nan, 3.4, np.nan],
                       [1.3, np.nan, np.nan, np.nan],
                       [np.nan, 3.4, 2.4, 3.2]])
    
    
    data2 = np.asarray([[1,2.2,3,4.5 ],
                   [2.3, np.nan, 3.4, np.nan],
                   [1.1, np.nan, np.nan, np.nan],
                   [np.nan, 3.3, 2.4, np.nan]])
    
    
    df = dt.Datatable(data, meta=metaDict, columns = [2010, 2012, 2013, 2015], index = ['ARG', 'DEU', 'FRA', 'GBR'])
    df2 = dt.Datatable(data2, meta=metaDict2, columns = [2009, 2012, 2013, 2015], index = ['ARG', 'DEU', 'FRA', 'GBR'])
    
    
    assert isinstance(df, dt.Datatable)
    assert isinstance(df2, dt.Datatable)
    

def test_append():
    metaDict = {'source' : 'TEST',
                'scenario' : 'scen1',
                'entity' : 'Population',
                'unit' : 'm'}
     
    data = np.asarray([[1,2.2,3,4 ],
                       [2.3, np.nan, 3.4, np.nan],
                       [1.3, np.nan, np.nan, np.nan],
                       [np.nan, 3.4, 2.4, 3.2]])
    
    metaDict2 = {'source' : 'TEST2',
                'entity' : 'area',
                'scenario' : 'scen2',
                'unit' : 'km'}  
    data2 = np.asarray([[1,2.2,3,4.5 ],
                   [2.3, np.nan, 3.4, np.nan],
                   [1.1, np.nan, np.nan, np.nan],
                   [np.nan, 3.3, 2.4, np.nan]])
    
    metaDict3 = {'source' : 'TEST2',
                'entity' : 'Population',
                'scenario' : 'scen3',
                'unit' : 'km'} 
    data3 = np.asarray([[1,2.2,3,4.5 ],
                   [2.3, np.nan, 3.4, np.nan]])
    
    df = dt.Datatable(data, meta=metaDict, columns = [2010, 2012, 2013, 2015], index = ['ARG', 'DEU', 'RUS', 'IND'])
    df2 = dt.Datatable(data2, meta=metaDict2, columns = [2009, 2012, 2013, 2015], index = ['ARG', 'DEU', 'FRA', 'GBR'])
    df3 = dt.Datatable(data3, meta=metaDict3, columns = [2009, 2012, 2013, 2015], index = ['FRA', 'GBR'])
    
    dt_merge = df.append(df3)
    obs_vlues = np.array([[    np.nan, 1.0e+00, 2.2e+00, 3.0e+00, 4.0e+00],
                          [    np.nan, 2.3e+00,     np.nan, 3.4e+00,     np.nan],
                          [    np.nan, 1.3e+00,     np.nan,     np.nan,     np.nan],
                          [    np.nan,     np.nan, 3.4e+00, 2.4e+00, 3.2e+00],
                          [1.0e+03,     np.nan, 2.2e+03, 3.0e+03, 4.5e+03],
                          [2.3e+03,     np.nan,     np.nan, 3.4e+03,     np.nan]])

    assert (dt_merge.values == obs_vlues)[~np.isnan(dt_merge.values)] .all()
    assert dt_merge.meta['scenario'] == "computed: scen1+scen3"

def test_clean():
    from pandas.testing import assert_frame_equal
    metaDict2 = {'source' : 'TEST2',
                'entity' : 'area',
                'unit' : 'km'}    
        
    
    
    data2 = np.asarray([[1,2.2,3,np.nan ],
                   [2.3, np.nan, 3.4, np.nan],
                   [1.1, np.nan, np.nan, np.nan],
                   [np.nan, 3.3, 2.4, np.nan]])
    
    
    df2 = dt.Datatable(data2, meta=metaDict2, columns = [2009, 2012, 2013, 2015], index = ['ARG', 'DEU', 'FRA', 'USSDR'])
    exp = dt.Datatable(data2, meta=metaDict2, columns = [2009, 2012, 2013, 2015], index = ['ARG', 'DEU', 'FRA', 'UDSSR'])
    exp = exp.drop('UDSSR')
    exp = exp.drop(2015, axis=1)
    df2_clean = df2.clean()
    df2_clean == df2.clean()
    assert assert_frame_equal(df2_clean, exp) is None


def test_consistent_meta():
    #%%
    df = dt.Datatable(data=np.asarray([[2.2,3.4 ],
                                       [2.3,  3.4]]
                                       ), 
                    meta={'source' : 'TEST',
                          'entity' : 'Area',
                          'category': 'Forestery',
                          'scenario' : 'Historic',
                          'unit' : 'm'}, 
                    columns = [2010, 2012], 
                    index = ['ARG', 'DEU'])
    
    df.generateTableID()
    
    assert df.meta['variable'] == 'Area|Forestery'
    assert df.meta['pathway']  == 'Historic'
    
    # check removal of empty meta
    df.meta['category'] = np.nan
    df.meta['model'] = ''
    df.meta['description'] = ''
    df.generateTableID()
    
    assert 'category' not in df.meta.keys()
    assert 'model' not in df.meta.keys()
    assert 'description' not in df.meta.keys()
    
    #%%
    
if __name__ == '__main__':    
    test_creation()
    test_append()
    test_clean()
    test_consistent_meta()
    