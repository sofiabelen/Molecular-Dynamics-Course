import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.optimize import curve_fit

def f(P, T):
    return 0.05 + 0.07 * P\
            - (1.04 + 0.1 * P) / T

def getMSD(data, tsteps, npart):
    trange = int((tsteps - 1) / 2)
    msd = np.zeros(trange - 1)
    for deltaT in range(1, trange):
        for t0 in range(trange):
            for i in range(npart):
                msd[deltaT - 1] +=\
                        (data['rx'][(t0 + deltaT) * npart + i]\
                        - data['rx'][t0 * npart + i])**2
                msd[deltaT - 1] +=\
                        (data['ry'][(t0 + deltaT) * npart + i]\
                        - data['ry'][t0 * npart + i])**2
                msd[deltaT - 1] +=\
                        (data['ry'][(t0 + deltaT) * npart + i]\
                        - data['ry'][t0 * npart + i])**2
    
    msd /= npart * trange
    return msd

def getDiffusion(msd, trange):
    def line(x, a, b):
        return a*x + b
    
    line_start = int(trange * 0.7)
    popt_line, pcov_line = curve_fit(f=line,\
            xdata=np.arange(line_start, trange - 1) * dt,\
            ydata=msd[line_start:trange - 1])
    
    return popt_line[0] / 6

tsteps = 200
npart = 343
dt = 1
trange = int((tsteps - 1) / 2)

T = np.arange(10, 91, 10) / 100
# P = [0.273214628, 1.008939546, 1.780406771]
P = [-0.09977464, 0.134204047,\
        0.420707078, 0.707931277, 1.008939546,\
        1.345976614, 1.621309306, 1.932180923,\
        2.268495380]

for i in range(9):
    data = np.genfromtxt('dataRice' + str(int(T[i] * 100)),\
            names=True)
    msd = getMSD(data, tsteps, npart)
    D = getDiffusion(msd, trange)
    print(np.log10(D), " ", f(P[i], T[i]))
