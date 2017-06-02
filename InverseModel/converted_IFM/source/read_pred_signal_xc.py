@mfunction("time, firesignal")
def read_pred_signal_xc(numcomp=None):
    # This function will read 
    #1. the vctor of time
    #2. the matrix of vectors of firesignal over time [signal1, signal2,
    #signal3,...]


    #Inputs:  Number of Cpompartments, Number of Fire- Will get the fire signals from an excel spreadsheet
    #Outputs: The vector of time simulation
    #         The matrix of fire signal 

    # setting config

#If use upper layer temperature, use 1, else, 0
#If use O2 concentration, use 1, else, 0
#If use CO2 concentration, use 1, else, 0
    usedsignal = mcat([1, OMPCSEMI, 1, OMPCSEMI, 0, OMPCSEMI, 0])#If use Mass flow rate, use 1, else, 0

    #According to Guo's paper, temperature turns out to be the best fire
    #temperature.

    #if other fire signal is used, this part has to change
    numsignal = usedsignal(1) * numcomp + usedsignal(2) * numcomp + usedsignal(3) * numcomp + usedsignal(4)#For each compartment, it'll has one upper layer temperature,O2 concentration, CO2 concentration
    column = 1#determine which column of firesignal matrix it is writing on

    #Read the time vector and length
    filename = mstring('pred_signal_xc_n.csv')
    csvreadh(filename)
    length = size(data, 1)
    datasize = length - 3#First 4 rows are useless
    time = data(mslice[4:length], 1)#saved as column
    firesignal = zeros(datasize, numsignal)

    #signal for temperature
    if usedsignal(1) == 1:
        filename = mstring('pred_signal_xc_n.csv')
        csvreadh(filename)
        for counter in mslice[1:numcomp]:
            firesignal(mslice[:], column).lvalue = data(mslice[4:length], 5 * counter - 3)        #location of Temp in the sheet
            column = column + 1
            end
            end

            #signal for O2 concentration
            if usedsignal(2) == 1:
                filename = mstring('pred_signal_xc_s.csv')
                csvreadh(filename)
                for counter in mslice[1:numcomp]:
                    firesignal(mslice[:], column).lvalue = data(mslice[4:length], 20 * counter - 17)                #location of O2 concentration in the sheet
                    column = column + 1
                    end
                    end

                    #signal for CO2 concentration
                    if usedsignal(3) == 1:
                        filename = mstring('pred_signal_xc_s.csv')
                        csvreadh(filename)
                        for counter in mslice[1:numcomp]:
                            firesignal(mslice[:], column).lvalue = data(mslice[4:length], 20 * counter - 16)                        #location of O2 concentration in the sheet
                            column = column + 1
                            end
                            end

                            #signal for mass flow rate
                            if usedsignal(4) == 1:
                                filename = mstring('pred_signal_xc_f.csv')
                                csvreadh(filename)
                                #     for counter=1:numcomp-1
                                for counter in mslice[1:1]:
                                    firesignal(mslice[:], column).lvalue = data(mslice[4:length], 2 * counter + 2)                                #location of mass flow rate in the sheet
                                    column = column + 1
                                    end
                                    end

                                    #filename= 'hrr_pred_oxy_w.csv';

                                    #[~,data]=csvreadh(filename);
                                    #pred_mass=data(5:length,2)';

                                    end
