import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline

data1 = np.genfromtxt("data1", names=True)
data2 = np.genfromtxt("data2", names=True)

nsteps = 100
npart = 64

vdiff = np.zeros(nsteps)
rdiff = np.zeros(nsteps)

for i in range(nsteps):
    for j in range(npart):
        rdiff[i] += (data1['rx'][i * npart + j] - data2['rx'][i * npart + j])**2
        rdiff[i] += (data1['ry'][i * npart + j] - data2['ry'][i * npart + j])**2
        rdiff[i] += (data1['rz'][i * npart + j] - data2['rz'][i * npart + j])**2
        vdiff[i] += (data1['vx'][i * npart + j] - data2['vx'][i * npart + j])**2
        vdiff[i] += (data1['vy'][i * npart + j] - data2['vy'][i * npart + j])**2
        vdiff[i] += (data1['vz'][i * npart + j] - data2['vz'][i * npart + j])**2

rmax = rdiff.max()
vmax = vdiff.max()
rdiff /= nsteps # * rmax
vdiff /= nsteps # * vmax

sns.set(context='notebook', style='darkgrid')
fig, ax = plt.subplots(figsize=(6, 6))

ax.set_xlabel(r'$t$')
ax.set_yscale('log')
    
def line(x, a, b):
    return a*x + b
    
line_start = 6
popt_line, pcov_line = curve_fit(f=line,\
        xdata=np.arange(line_start, 10, 0.1),\
        ydata=rdiff[line_start * 10 : ])

ax.plot(np.arange(0, 10, 0.1), rdiff,\
        label=r'$<\Delta r^2(t)>, \quad D = %.3f$'%(popt_line[0] / 6))
ax.plot(np.arange(0, 10, 0.1), vdiff,\
        label=r'$<\Delta v^2(t)>$')
ax.axvline(3, 0, 1, label=r'$t_m \approx 3$', color='g')
ax.legend()

fig.savefig("media/tm.pdf")
fig.savefig("media/tm.svg")
fig.savefig("media/tm.png", dpi=300)
