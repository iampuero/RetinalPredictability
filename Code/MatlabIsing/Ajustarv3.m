import maxent.*

%%
load('/home/iampuero/Documents/Memoria/Data/Fishmovie/Rasters/N51R0P0F20S1.mat')
tic
model = maxent.createModel(21,"kpairwise")
model = maxent.trainModel(model,binnedSpikes,'threshold',1.5);
toc
kpw_marginals_data = maxent.getEmpiricalMarginals(binnedSpikes,model);
kpw_marginals_model = maxent.getMarginals(model,'nsamples',size(binnedSpikes,2));
%%
ncells=21;
p2=loglog(kpw_marginals_data(2*ncells+2:end),kpw_marginals_model(2*ncells+2:end),'b*');hold on
p1=loglog(kpw_marginals_data(ncells+2:2*ncells+2),kpw_marginals_model(ncells+2:2*ncells+2),'r*');
p3=loglog(kpw_marginals_data(1:ncells+1),kpw_marginals_model(1:ncells+1),'g*');