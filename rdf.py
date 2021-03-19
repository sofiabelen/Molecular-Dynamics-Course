import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def getRDF(data, tsteps, rsteps, npart):
    g = np.zeros(rsteps)
    dr = rmax / rsteps
    rho = npart / rmax**2
    
    for t in range(tsteps):
        for i in range(npart):
            for j in range(i + 1, npart):
                xij2 = (data['rx'][t * npart + i] - data['rx'][t * npart + j])**2
                yij2 = (data['ry'][t * npart + i] - data['ry'][t * npart + j])**2
                zij2 = (data['rz'][t * npart + i] - data['rz'][t * npart + j])**2
                rij2 = xij2 + yij2 + zij2
    
                if(rij2 < rmax**2):
                    g[int(np.sqrt(rij2) / dr)] += 2
    
    for i in range(rsteps):
        rInner = rmax / rsteps * i
        rOuter = rmax / rsteps * (i + 1)
        V = 4 / 3 * np.pi * (rOuter**3 - rInner**3)
        g[i] /= V
    
    g /= tsteps * rho
    return g

data1 = np.genfromtxt('data1', names=True)
data2 = np.genfromtxt('data2', names=True)
data3 = np.genfromtxt('data3', names=True)

tsteps = 100
rsteps = 200
rmax = 5.03968338
npart = 64
dr = rmax / rsteps

g1 = getRDF(data1, tsteps, rsteps, npart)
g2 = getRDF(data2, tsteps, rsteps, npart)
g3 = getRDF(data3, tsteps, rsteps, npart)

sns.set(context='notebook', style='darkgrid')
fig, ax = plt.subplots(figsize=(6, 6))

xvalues = np.arange(0, rmax, dr)
ax.plot(xvalues, g3, label=r'Gas and Solid: $T = 0.3$')
ax.plot(xvalues, g2, label=r'Gas and Liquid: $T = 1.0$')
ax.plot(xvalues, g1, label=r'Fluid: $T = 3.0$')

ax.set_xlabel(r'$r$')
ax.set_ylabel(r'$g(r)$')

ax.legend()

fig.savefig("media/rdf.pdf")
fig.savefig("media/rdf.svg")
fig.savefig("media/rdf.png", dpi=200)
plt.show()
