# -*- coding: utf-8 -*-


import pathlib


def extract_input_files(input_dir):
    '''
    Extract input files from input folder
    
    Parameters
    ----------
    input_dir : TYPE
        DESCRIPTION.

    Raises
    ------
    FileNotFoundError
        DESCRIPTION.

    Returns
    -------
    netlist_files : TYPE
        DESCRIPTION.

    '''
    input_dir = pathlib.Path(input_dir).resolve()
    if not input_dir.is_dir():
        raise FileNotFoundError(2, 'No such netlist directory ', input_dir)    
    netlist_files = [x for x in input_dir.iterdir() if x.is_file() and x.suffix in ('.sp', '.cdl')]
    if not netlist_files:
        raise FileNotFoundError(2, 'No matching netlist(.sp/.cdl) files')    
    
    #TODO: add const extract
    const_files = [x for x in input_dir.iterdir() if x.is_file() and x.suffixes==['.const', '.json']]
    return netlist_files,const_files
   

    
def import_stdcell(cdl_file,gds_file,lef_file=None,verilog_file=None):
    '''

    Parameters
    ----------
    cdl_file : TYPE
        DESCRIPTION.
    gds_file : TYPE
        DESCRIPTION.
    lef_file : TYPE, optional
        DESCRIPTION. The default is None.
    verilog_file : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    None.

    '''
    return 0

    



