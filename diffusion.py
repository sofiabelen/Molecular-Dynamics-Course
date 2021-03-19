import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.optimize import curve_fit

tsteps = 100
npart = 343
dt = 0.01
trange = int((tsteps - 1) / 2)
msd = np.zeros(trange - 1)

data = np.genfromtxt('dataDif', names=True)

sns.set(context='notebook', style='darkgrid')
fig, ax = plt.subplots(figsize=(6, 6))

for deltaT in range(1, trange):
    for t0 in range(trange):
        for i in range(npart):
            msd[deltaT - 1] += (data['rx'][(t0 + deltaT) * npart + i] - data['rx'][t0 * npart + i])**2
            msd[deltaT - 1] += (data['ry'][(t0 + deltaT) * npart + i] - data['ry'][t0 * npart + i])**2
            msd[deltaT - 1] += (data['ry'][(t0 + deltaT) * npart + i] - data['ry'][t0 * npart + i])**2

msd /= npart * trange * 3

def line(x, a, b):
    return a*x + b

line_start = int(trange * 0.5)
popt_line, pcov_line = curve_fit(f=line,\
        xdata=np.arange(line_start, trange - 1) * dt,\
        ydata=msd[line_start:trange - 1])

time = np.arange(0, trange - 1) * dt
ax.plot(time, msd)
ax.plot(time, line(time, *popt_line),\
        label=r'Линейная асимтота $D = %.3f$'%(popt_line[0] / 6))
ax.set_xlabel(r'$t$')
ax.set_ylabel(r'$<r^2(t)>$')

ax.legend()

fig.savefig("media/diffusion.pdf")
fig.savefig("media/diffusion.svg")
fig.savefig("media/diffusion.png", dpi=200)
plt.show()
