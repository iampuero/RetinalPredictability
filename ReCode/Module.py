import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as spio
from json import loads, dumps
from scipy.io import loadmat,savemat
from scipy import sparse
from jpype import *






def loadmat(filename):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)

def _check_keys(dict):
    '''
    checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries
    '''
    for key in dict:
        if isinstance(dict[key], spio.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict        

def _todict(matobj):
    '''
    A recursive function which constructs from matobjects nested dictionaries
    '''
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, spio.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict


"""
{
"MAXENTFOLDER":"Ising/",
"RASTERSFOLDER":"fRasters/",
"MODELSFOLDER":"fModels/",
"PREDICTIONSFOLDER":"fPredictions/",
"PREDPSTHFOLDER":"fpredPSTH/",
"MEASURESFOLDER":"fMeasures/",
"MEASURESPSTHFOLDER":"fMeasuresPSTH/",
"DATASETSFOLDER":"fFileDatasets/"
}
"""
{}
class Pipeline()
    def __init__(self,folders,datasource,randomfixed,criteriafixed,base):
        self.MAXENTFOLDER = folders["MAXENTFOLDER"]
        self.RASTERSFOLDER = folders["RASTERSFOLDER"]
        self.MODELSFOLDER = folders["MODELSFOLDER"]
        #Results
        self.PREDICTIONSFOLDER = folders["PREDICTIONSFOLDER"]
        self.PREDPSTHFOLDER = folders["PREDPSTHFOLDER"]
        self.MEASURESFOLDER = folders["MEASURESFOLDER"]
        self.MEASURESPSTHFOLDER = folders["MEASURESPSTHFOLDER"]
        self.DATASETSFOLDER = folders["DATASETSFOLDER"]
        
        #function constants
        self.NsR = randomfixed
        self.Ns = criteriafixed
        self.base = base
        
        #data load
        self.SINGLERASTER = 0 #PSTH?
        self.RASTER = 0 #NORMAL RASTER
        self.SPRATE = 0 #spike rate
        self.N = 0
        self.T = 0
    
    def loadData(self,datasource):
        #caso fish
        if datasource == "fish":
            pass
        elif datasource == "degus":
        rasterfile = "../Data/Sparse/E0_C3_T0.02"
        raster = sparse.load_npz(rasterfile+".npz")
        raster = raster.toarray()[:,:-63]
        self.RASTER = raster
        self.SINGLERASTER = np.sum(np.split(raster,41,axis=1),axis=0)/41
        self.SPRATE = 
        self.N, self.T = raster.shape
    
        
    
    #noported
    def loadParams(self,modelfile):
        data = loadmat(MAXENTFOLDER+MODELSFOLDER+modelfile+".mat")
        params = data["params"]
        N = len(data["hListIn"])
        P = np.zeros((N,N))
        P[np.triu_indices(N, 1)] = params[N:] 
        P = P+np.diag(params[:N])
        return P