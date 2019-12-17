% MEX MONTECARLO SCRIPT
% mex MCMC_IsingModel.c -output MCMC_IsingModel
function FitModel(filename,datafolder,modelfolder)
    % LOADING DATA
    clear all;
    close all;

    load strcat(datafolder,"/",filename)
    binnedSpikes = sparse(logical(binnedSpikes(:,:)));
    [N,T] = size(binnedSpikes); % Binned spike train: N = number of neurons; T = number of timebins
    D=N*(N+1)/2;

    % MEAN AND COVARIANCE OF SUFFICIENT STATISTICS
    offMat = zeros(D);
    for n1=1:N
        offMat(n1,n1) = n1;
        for n2=(n1+1):N
            offMat(n1,n2) = offset(n1,N)+n2;
            offMat(n2,n1) = offMat(n1,n2);
        end
    end


    tic % It might take several minutes
    chi = zeros( D );
    for b=1:T
        [L,~,~] = find( binnedSpikes(:,b) );
        index = offMat(L,L);
        index = index(:);
        chi(index,index) = chi(index,index)+1;
    end
    toc


    p = diag(chi)/T;
    chiC = chi/T - p * p';
    eV = sort(eig(chiC));

    % INITIAL CONDITION
    global params;

    jListIn = zeros([N*(N-1)/2 1]);
    hListIn = log( p(1:N)./(1 - p(1:N)) );
    params = [hListIn; jListIn];

    % INFERENCE REGULARIZATION
    etaH = 0.000; % L2 regularization on fileds h
    etaJ = 0.0000; % L2 regularization on couplings J
    etaMat = diag( [ etaH * ones([N 1]) ; etaJ * ones([N*(N-1)/2 1])   ]  ); % L2 regularization as big matrix


    % PARAMETERS INFERENCE 
    %delete(gcp);
    parallel = gcp('nocreate'); % for parallel processing
    if isempty(parallel)
        c = parcluster;
        parpool(c)
        nWork = c.NumWorkers;
    else
        nWork = parallel.NumWorkers;
    end

    logTd=3;
    nStepMore=0; %increase this for posterior sampling
    threshold = exp(-0.0);
    alphaStart = 1.0;
    verbose = true;

    [ q , output ] = dataDriven_IsingModel( N, T, 1/eV(1), logTd, p, chiC, etaMat, alphaStart, threshold, nStepMore, nWork , verbose);

    filePath = pwd; % chose a path to save the file
    save([strcat(modelfolder,"/",filename)],'hListIn','jListIn','p','q','output','params');
end
    if PLOT:
    % PLOTTING PARAMETERS
    fig=figure;
    subplot(1,2,1)
    hold on
    %plot([0 max(p(1:N))*1.05],[0 max(p(1:N))*1.05],'k','Linewidth',2.0)
    %plot(p(1:N),q(1:N),'.','Markersize',16)
    histogram(params(1:N))
    xlabel('Fields','FontSize', 16);
    ylabel('Histogram','FontSize', 16);

    subplot(1,2,2)
    hold on
    histogram(params(N+1:end))
    xlabel('Couplings','FontSize', 16);
    ylabel('Histogram','FontSize', 16);

    % PLOTTING CORRELATIONS
    ccData = zeros([ N*(N-1)/2 1]);
    ccModel = zeros([ N*(N-1)/2 1]);

    for n1=1:N
        for n2=(n1+1):N
            ccData(offset(n1,N)+n2-N) = p(offset(n1,N)+n2) - p(n1)*p(n2);
            ccModel(offset(n1,N)+n2-N) = q(offset(n1,N)+n2) - q(n1)*q(n2);

        end
    end

    fig=figure;
    subplot(1,2,1)
    hold on
    plot([0 max(p(1:N))*1.05],[0 max(p(1:N))*1.05],'k','Linewidth',2.0)
    plot(p(1:N),q(1:N),'.','Markersize',16)
    xlabel('Data: mean rate','FontSize', 16);
    ylabel('Model: mean rate','FontSize', 16);

    subplot(1,2,2)
    hold on
    plot([0 max(ccData)*1.05],[0 max(ccData)*1.05],'k','Linewidth',2.0)
    plot(ccData,ccModel,'.','Markersize',16)
    xlabel('Data: covariances','FontSize', 16);
    ylabel('Model: covariances','FontSize', 16);

    % PLOTTING RUNNING DETAILS
    fig=figure;
    [xD,y1D,y2D]= plotyy(output(:,1),output(:,3),output(:,1),output(:,2)); 
    y1D.LineWidth=3.0;
    y2D.LineWidth=3.0;
    set(xD(1),'XLim',[-0. numel(output(:,1))+0.5])
    set(xD(1),'YTick',0:5:20,'FontWeight','bold','FontSize',13);
    set(xD(2),'YTick',0:0.25:2,'FontWeight','bold','FontSize',13);
    %set(xD(1),'XTick',0:5:32,'FontWeight','bold','FontSize',10);
    legend('$\epsilon$','$\alpha$','Location','northeast');
    %legend('\epsilon','\alpha','Location','northeast');
    set(legend, 'Interpreter','LaTex');
    set(legend,'FontSize',30);
    set(gca,'box','off');
    xlabel('Learning steps','FontSize', 14);
    xlabh = get(gca,'XLabel');
    xlabh.Position(2) = -1.15;

end
    