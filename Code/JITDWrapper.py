import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat,savemat
from scipy import sparse
from jpype import *
import os
import scipy.io as spio
FILENAME = "../Data/spktimes_4_exps_6_conds.mat"

try:
    JITD = 1
    if JITD:
        jarLocation = "external/infodynamics.jar"
        startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=" + jarLocation) #Start JITDready JVM ->shutdownJVM()
        print("JVM Started")
except Exception:
    pass
    

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
    
    
def dataLoader(exp,cond,tbase):
    rasterfile = "../Data/Sparse/E{0}_C{1}_T{2}".format(exp,cond,tbase)
    if os.path.isfile(rasterfile+".npz"):
        print("Returning saved sparse matrix",rasterfile.split("/")[-1])
        raster = sparse.load_npz(rasterfile+".npz")
        raster = raster.toarray()
        return raster,raster.shape[0]
    data = loadmat(FILENAME)["spks"][exp][cond][0]
    Ncount = data.shape[0] #neuron count
    maxdata = max([max(data[n][0]) for n in range(Ncount)])+1 #max spike time of sample
    raster=np.zeros((Ncount,int(maxdata/tbase)))  #raster dimensions
    for n in range(Ncount):
        for s in data[n][0]:
            if not np.isnan(s):
                raster[n][int(s/tbase)]=1 #binarizing [0,TBIN[ and so on
    print ("Saving sparse matrix")
    sparse.save_npz(rasterfile,sparse.csr_matrix(raster))
    return raster,Ncount


def dataLoaderTxt():
    with open("../Data/bint.txt") as O:
        file = O.readlines()
    file = [list(map(int,x.strip().split())) for x in file]
    return np.array(file)

def Entropy(exp,cond,tbase):
    hfile="../Data/PreComputed/H/E{0}_C{1}_T{2}".format(exp,cond,tbase)
    if os.path.isfile(hfile+".npy"):
        print ("Returning PreComputed HMatrix "+hfile.split("/")[-1])
        return np.load(hfile+".npy")
    raster,Ncount = dataLoader(exp,cond,tbase)
    calcClass = JPackage("infodynamics.measures.discrete").EntropyCalculatorDiscrete
    calc = calcClass(2)
    H = np.zeros(Ncount)
    for S in range(Ncount):
        source = JArray(JInt, 1)(raster[S].tolist())
        calc.initialise()
        calc.addObservations(source)
        H[S]=calc.computeAverageLocalOfObservations()
        print(S," ",end="")
    np.save(hfile,H)
    return H

def MutualInformation(exp,cond,tbase):
    mifile="../Data/PreComputed/MI/E{0}_C{1}_T{2}".format(exp,cond,tbase)
    if os.path.isfile(mifile+".npy"):
        print ("Returning PreComputed MIMatrix "+mifile.split("/")[-1])
        return np.load(mifile+".npy")
    raster,Ncount = dataLoader(exp,cond,tbase)
    calcClass = JPackage("infodynamics.measures.discrete").MutualInformationCalculatorDiscrete
    calc = calcClass(2, 2, 0)
    MI = np.zeros((Ncount,Ncount))
    for S in range(Ncount):
        source = JArray(JInt, 1)(raster[S].tolist())
        for D in range(S,Ncount):
            if S==D: continue;
            destination = JArray(JInt, 1)(raster[D].tolist())
            calc.initialise()
            calc.addObservations(source, destination)
            MI[S][D]=calc.computeAverageLocalOfObservations()
        print(S," ",end="")
    np.save(mifile,MI)
    return MI

def TransferEntropy(exp,cond,tbase):
    tefile="../Data/PreComputed/TE/E{0}_C{1}_T{2}".format(exp,cond,tbase)
    if os.path.isfile(tefile+".npy"):
        print ("Returning PreComputed TEMatrix "+tefile.split("/")[-1])
        return np.load(tefile+".npy")
    raster,Ncount = dataLoader(exp,cond,tbase)
    calcClass = JPackage("infodynamics.measures.discrete").TransferEntropyCalculatorDiscrete
    #dim,dest_Hlen,dest_delay,source_Hlen,source_delay,delay_source_dest
    calc = calcClass(2, 1, 1, 1, 1, 0)
    TE = np.zeros((Ncount,Ncount))
    for S in range(Ncount):
        source = JArray(JInt, 1)(raster[S].tolist())
        for D in range(Ncount): #FULL
            if S==D: continue;
            destination = JArray(JInt, 1)(raster[D].tolist())
            calc.initialise()
            calc.addObservations(source, destination)
            TE[S][D]=calc.computeAverageLocalOfObservations()
        print(S," ",end="")
    np.save(tefile,TE)
    return TE

def ActiveInformationStorage(exp,cond,tbase):
    aisfile="../Data/PreComputed/AIS/E{0}_C{1}_T{2}".format(exp,cond,tbase)
    if os.path.isfile(aisfile+".npy"):
        print ("Returning PreComputed AISVector "+aisfile.split("/")[-1])
        return np.load(aisfile+".npy")
    raster,Ncount = dataLoader(exp,cond,tbase)
    calcClass = JPackage("infodynamics.measures.discrete").ActiveInformationCalculatorDiscrete
    #dim,Hlen
    calc = calcClass(2, 1)
    AIS = np.zeros(Ncount)
    for S in range(Ncount):
        source = JArray(JInt, 1)(raster[S].tolist())
        calc.initialise()
        calc.addObservations(source)
        AIS[S]=calc.computeAverageLocalOfObservations()
        print(S," ",end="")
    np.save(aisfile,AIS)
    return AIS

def plotLogLogHistogram(Data,Nindex=123):
    fig, ax = plt.subplots()
    ax.loglog()
    plt.hist(Data[Nindex], density=1, bins=100)
    plt.show()

def plotNeuronRanking(Data,Nindex=123):
    fig, ax = plt.subplots()
    ax.set_yscale("log")
    plt.plot(list(range(Data.shape[0])),sorted(Data[Nindex])[::-1])
    plt.show()
    
if __name__ == "__main__":
    A = MutualInformation(0,3,0.01)
    A = A+A.T
    B = MutualInformation(0,3,0.02)
    B = B+B.T
    plt.figure(figsize=(15,10))
    plt.subplot(1,2,1)
    plt.imshow(A,cmap="hot")
    plt.subplot(1,2,2)
    plt.imshow(B,cmap="hot")
    plt.show()
    print ("MAIN")
