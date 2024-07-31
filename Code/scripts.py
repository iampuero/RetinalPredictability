import numpy as np
import os
from scipy.io import loadmat,savemat
from scipy import sparse

def MutualInformation(exp,cond,tbase):
    mifile="../Data/PreComputed/MI/E{0}_C{1}_T{2}".format(exp,cond,tbase)
    if os.path.isfile(mifile+".npy"):
        print ("Returning PreComputed MIMatrix "+mifile.split("/")[-1])
        return np.load(mifile+".npy")
    

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
    
    
#### Parámetros Fijos
FILENAME = "../Data/spktimes_4_exps_6_conds.mat"
EXP = 0 # 0 1 2 3
COND = 3 # 0.issa 1.ifsa 2.wn 3.nm 4.ffsa 5. fssa
TBASE = 0.02 #0.001 = 1ms
RASTER = dataLoader(EXP,COND,TBASE)[0]
INTERVAL = 50 # para SpRate
N,T = RASTER.shape
NsR = [10,20,50,100,120,N-1]
Ns = [4,5,6,7,8,9,10,20,50,100,120,N-1]


def cargarDataset(TP):
    if "N{0}.json".format(TP) in os.listdir("Datasets"):
        with open("Datasets/N{0}.json".format(TP)) as DD:
            dataset = loads(DD.readline())
        print("Carga de archivo existente para neurona {0}".format(TP))

    #### Creación de Archivo
    else:
        #fixed = int(np.random.choice(range(N)))
        fixed = TP
        free = np.array(list(set(range(N))-{fixed}))
        mienum = sorted([(x[1],x[0]) for x in enumerate(MI[fixed])],reverse=1) #mayor a menor
        miids = list([x[1] for x in mienum])
        miids.remove(fixed)
        cenum = sorted([(x[1],x[0]) for x in enumerate(CC[fixed])],reverse=1)
        cids = list([x[1] for x in cenum])[:-1]
        denum = sorted([(x[1],x[0]) for x in enumerate(D[fixed])])
        dids = list([x[1] for x in denum])[1:]
        dataset = {"fixed":fixed,
                   0:dict([(n,[sorted(np.random.choice(free,n,False).tolist()) for j in range(J)]) for n in NsR]),
                   1:{},
                   2:dict([(n,[miids[:n]]) for n in Ns]),
                   3:dict([(n,[dids[:n]]) for n in Ns]),
                   4:dict([(n,[cids[:n]]) for n in Ns])} 
        newsets=[np.random.choice(list(set(range(N))-{fixed}),N-1,False).tolist() for j in range(J)]
        for n in NsR:
            dataset[1][n]=[]
            for j in range(J):
                dataset[1][n].append(newsets[j][:n])
        with open("Datasets/N{0}.json".format(TP),"w") as DD:
            DD.write(dumps(dataset))
    return dataset



def modelsMatlabLines(neuron):
    filelist = []
    for rank in [0,1,2,3,4]: #tipo de ranking
        if rank in [0,1]:
            flist,slist = [10,20,50,100,120,150],[0,1,2,3,4]
        else:
            flist,slist = [4,5,6,7,8,9,10,20,50,100,120,150],[0]
        for f in flist: #neuronas fijadas
            for s in slist: #samples
                filelist.append("E{0}C{1}T{2}N{3}R{4}P{5}F{6}S{7}".format(EXP,COND,TBASE,neuron,rank,0,f,s))
    return filelist


def modelCheck(a,b):
    foldercont = os.listdir("MatlabIsing/Models/")
    matlines =  []
    for nn in range(a,b):
        matlines = matlines+modelsMatlabLines(nn)
    rematlines=[f for f in matlines if f+".mat" not in foldercont]
    print(len(matlines),len(rematlines))

    
def run_matlab(filename,back=0):
    os.system("""matlab -nodisplay -nosplash -nodesktop -r "cd('MatlabIsing');Ajustar('Rasters','Models','{}.mat');exit()" """.format(filename)+["","&"][back])

    
def batchRun(a,b):
    foldercont = os.listdir("MatlabIsing/Models/")
    matlines =  []
    for nn in range(a,b):
        matlines = matlines+modelsMatlabLines(nn)
    rematlines=[f for f in matlines if f+".mat" not in foldercont]
    sortedlines = sorted(rematlines,key=lambda s: int(s[s.index("F")+1:s.index("S")]))
    for sub in range(len(sortedlines))[::5]:
        sl =  sortedlines[sub:sub+5]
        print(sl)
        run_matlab(sl[0],1)
        run_matlab(sl[1],1)
        run_matlab(sl[2],1)
        run_matlab(sl[3],1)
        run_matlab(sl[4],0)