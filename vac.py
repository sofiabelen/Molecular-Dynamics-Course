import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.optimize import curve_fit

def vac(data, tsteps, npart):
    trange = int((tsteps - 1) / 2)
    vac = np.zeros(trange - 1)
    for deltaT in range(1, trange):
        ## Cᵥ = ∑Cᵥ(t) / M
        for t0 in range(trange):
            ## Cᵥ = ∑ᵢv⃗ᵢ(0)⋅v⃗ᵢ(t) / N
            for i in range(npart):
                vac[deltaT - 1] +=\
                        data['vx'][(t0 + deltaT) * npart + i]\
                        * data['vx'][t0 * npart + i]
                vac[deltaT - 1] +=\
                        data['vy'][(t0 + deltaT) * npart + i]\
                        * data['vy'][t0 * npart + i]
                vac[deltaT - 1] +=\
                        data['vz'][(t0 + deltaT) * npart + i]\
                        * data['vz'][t0 * npart + i]
    
    vac /= npart * trange * 3

    return vac

def plot(vac, trange, ax, label):
    def line(x, a, b):
        return a*x + b
    
    line_start = int(trange * 0.7)
    popt_line, pcov_line = curve_fit(f=line,\
            xdata=np.arange(line_start, trange - 1) * dt,\
            ydata=vac[line_start:trange - 1])
    
    time = np.arange(line_start, trange - 1) * dt
    ax.plot(np.arange(0, trange - 1) * dt, vac,
            label=label)

def integrate(vac, dt):
    trange = len(vac)
    area = 0

    for i in range(trange):
        area += vac[i] * dt

    return area

tsteps = 1000
npart = 343
dt = 0.01
trange = int((tsteps - 1) / 2)

data1 = np.genfromtxt('dataVAC1', names=True)
data2 = np.genfromtxt('dataVAC2', names=True)
data3 = np.genfromtxt('dataVAC3', names=True)

vac1 = vac(data1, tsteps, npart)
vac2 = vac(data2, tsteps, npart)
vac3 = vac(data3, tsteps, npart)

sns.set(context='notebook', style='darkgrid')
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlabel(r'$t$')
ax.set_ylabel(r'$<\vec{v}(0) \cdot \vec{v}(t)>$')

label1 = r'$ T = 1.0, \rho = 0.7, D = %.5f$'%(np.sum(vac1) * dt / 3)
label2 = r'$ T = 1.5, \rho = 0.7, D = %.5f$'%(np.sum(vac2) * dt / 3)
label3 = r'$ T = 2.0, \rho = 0.7, D = %.5f$'%(np.sum(vac3) * dt / 3)

plot(vac1, trange, ax, label1)
plot(vac2, trange, ax, label2)
plot(vac3, trange, ax, label3)
ax.legend()

fig.savefig("media/vac.pdf")
fig.savefig("media/vac.svg")
fig.savefig("media/vac.png", dpi=200)
plt.show()
