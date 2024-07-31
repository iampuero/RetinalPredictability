function [RFs,NbSpk] = STAs(rast,StimTimes,Latencies,GoodCells,SizeCheckerboard,BitFilename,Subset)
%rast: the raster (variable SpikeTimes)
%StimTimes: same unit than raster, the frame times extracted from the event
%marker. Don't forget that, if the checkerboard is at 30 Hz,you should
%suppress one every two. 
%Latencies: the range of frames to take into account before and after the
%spikes, e.g. (-30:30)
%GoodCells: Which we want to have the RFs. Can be (1:length(SpikeTimes))
%SizeCheckerboard: [40 40]
%BitFilename: 'binarysource1000Mbits'
%SubSet: to restrict the computations to some window(s). Optional. 

%The normalized result is RFs/NbSpk. 

RFs = zeros([SizeCheckerboard(1),SizeCheckerboard(2),length(Latencies),length(GoodCells)]);
NbSpk = zeros(length(GoodCells),1);

fid=fopen(BitFilename,'r','ieee-le');
data=fread(fid,'uint16');
fclose(fid);

for ic=1:length(GoodCells)
    icell = GoodCells(ic);
    fprintf('icell = %d\n',icell);
    count = 0;
    if nargin>6
        r = [];
        for isub=1:size(Subset,1)
            r = [r ; double(rast{icell}( double(rast{icell})>=Subset(isub,1) & double(rast{icell})<Subset(isub,2) ))];
        end
        disp([int2str(length(r)) ' spikes for cell ' int2str(icell)])
    else
        r = double(rast{icell});
    end
    
    for ispike=1:length(r)
        if rem(ispike,100) == 0; fprintf('ispike = %d\n',ispike); end;
        IdxFrame = find( (StimTimes - r(ispike))<0,1,'last');
        if ~isempty(IdxFrame)%We found something...
            if (IdxFrame+Latencies(1)>0)%&&(IdxFrame+Latencies(end)<length(s))%...not on the border
                
                indexes = Latencies + IdxFrame - 1;%-1 so that it could be 0. 
                
                %The following is to the frame content. 
                frames = zeros([SizeCheckerboard(1),SizeCheckerboard(2),length(indexes)]);
                for it=1:length(indexes)
                    for ix=1:SizeCheckerboard(1)
                        for iy=1:SizeCheckerboard(2)
%                             total = it*SizeCheckerboard(1)*SizeCheckerboard(2) + iy*SizeCheckerboard(2) + ix;
                            total = indexes(it)*SizeCheckerboard(1)*SizeCheckerboard(2) + iy*SizeCheckerboard(2) + ix;
                            %Similar to the stimulus display program. 
                            k = floor(total/16);
                            j = mod(total,16);
                            %res((k-1)*16+1+j) = bitand(data(k+1),2^j)>0;
                            frames(ix,iy,it) = bitand(data(k+1),2^j)>0;
                        end
                    end
                end
                
                RFs(:,:,:,ic) = RFs(:,:,:,ic) + frames;%s(Latencies+IdxFrame)';                      
                count = count + 1;
            end
        end
    end

%     if count>0
%         RFs(:,ic) = RFs(:,ic) / count;
%     end
    NbSpk(ic) = count;
end

