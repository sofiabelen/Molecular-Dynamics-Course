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
    
    msd /= npart * trange
    return msd

def plotMSD(msd, trange, ax, label):
    def line(x, a, b):
        return a*x + b
    
    line_start = int(trange * 0.7)
    popt_line, pcov_line = curve_fit(f=line,\
            xdata=np.arange(line_start, trange - 1) * dt,\
            ydata=msd[line_start:trange - 1])
    
    time = np.arange(line_start, trange - 1) * dt
    ax.plot(np.arange(0, trange - 1) * dt, msd,
            label=r'$D = %.3f$, '%(popt_line[0] / 6) + label)

    ax.axvline(line_start * dt, 0, 1)

tsteps = 200
npart = 343
dt = 0.1
trange = int((tsteps - 1) / 2)

sns.set(context='notebook', style='darkgrid')
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlabel(r'$t$')
ax.set_ylabel(r'$<r^2(t)>$')

for i in range(3):
    tau = 100 + i * 500
    data = np.genfromtxt('dataTherm'\
            + str(tau), names=True)
    msd = getMSD(data, tsteps, npart)
    label = r'$\tau = %d$'%(tau)
    plotMSD(msd, trange, ax, label)

ax.legend()

fig.savefig("media/thermostat.pdf")
fig.savefig("media/thermostat.svg")
fig.savefig("media/thermostat.png", dpi=200)
