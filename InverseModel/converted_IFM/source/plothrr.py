numfire = 4; print numfire

str = strcat(mstring('data4.mat'))

#str=strcat('C:\Users\Xiaolin Cai\Desktop\research1\multiroom_multifire\data.mat');
load(mstring('data4.mat'))
load(mstring('result.mat'))


#plot forward model
# for counter = 1:numfire
#     subplot(numfire+numsignal,2,counter*2-1)   %Only plot for temperature and hrr for now
#     plot(timein,hrrin(:,counter))
#     titlestr=sprintf('hrr for forward model for fire %d',counter);
#     title(titlestr)
#     xlabel('time')
#     ylabel('hrr')
# end

for counter in mslice[1:numfire]:
    subplot(numfire, 1, counter)#Only plot for temperature and hrr for now
    plot(t, hrr(mslice[:], counter))
    titlestr = sprintf(mstring('hrr for forward model for fire %d'), counter)
    title(titlestr)
    xlabel(mstring('time'))
    ylabel(mstring('hrr'))
end

for counter in mslice[1:numfire]:
    #subplot(numfire+numsignal,2,counter*2)
    #     subplot(numfire+numsignal,2,counter*2-1)
    subplot(numfire, 1, counter)
    hold(mstring('on'))
    plot(time, HRR_pred(mslice[:], counter), mstring('r'))
    #     titlestr=sprintf('hrr for inverse model for fire %d',counter);
    #     title(titlestr)
    #     xlabel('time')
    #     ylabel('hrr')
end
