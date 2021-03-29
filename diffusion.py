import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.optimize import curve_fit

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
    
    msd /= npart * trange * 3

    return msd

def plotMSD(msd, trange, ax, label, color):
    def line(x, a, b):
        return a*x + b
    
    line_start = int(trange * 0.7)
    popt_line, pcov_line = curve_fit(f=line,\
            xdata=np.arange(line_start, trange - 1) * dt,\
            ydata=msd[line_start:trange - 1])
    
    time = np.arange(line_start, trange - 1) * dt
    ax.plot(np.arange(0, trange - 1) * dt, msd,
            label=r'$D = %.3f$, '%(popt_line[0] / 6) + label)

tsteps = 100
npart = 343
dt = 0.01
trange = int((tsteps - 1) / 2)

data1 = np.genfromtxt('dataDif1', names=True)
data2 = np.genfromtxt('dataDif2', names=True)
data3 = np.genfromtxt('dataDif3', names=True)

msd1 = getMSD(data1, tsteps, npart)
msd2 = getMSD(data2, tsteps, npart)
msd3 = getMSD(data3, tsteps, npart)

sns.set(context='notebook', style='darkgrid')
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlabel(r'$t$')
ax.set_ylabel(r'$<r^2(t)>$')

label1 = r'$ T = 1.0, \rho = 0.7 $'
label2 = r'$ T = 1.5, \rho = 0.7 $'
label3 = r'$ T = 2.0, \rho = 0.7 $'

plotMSD(msd1, trange, ax, label1, color1)
plotMSD(msd2, trange, ax, label2, color2)
plotMSD(msd3, trange, ax, label3, color3)
ax.legend()

fig.savefig("media/diffusion.pdf")
fig.savefig("media/diffusion.svg")
fig.savefig("media/diffusion.png", dpi=200)
