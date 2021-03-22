import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def getRDF(data, tsteps, rsteps, npart):
    g = np.zeros(rsteps)
    dr = rmax / rsteps
    
    totalpart = npart
    for t in range(tsteps):
        for i in range(npart):
            for j in range(npart):
                xij2 = (data['rx'][t * npart + i]\
                        - data['rx'][t * npart + j])**2
                yij2 = (data['ry'][t * npart + i]\
                        - data['ry'][t * npart + j])**2
                zij2 = (data['rz'][t * npart + i]\
                        - data['rz'][t * npart + j])**2
                rij2 = xij2 + yij2 + zij2
    
                if(rij2 < rmax**2 and i != j):
                    ## We found a particle in spherical shell 
                    ## rij + dr
                    g[int(np.sqrt(rij2) / dr)] += 1
                    totalpart += 1
    
    ## Average density in a sphere or radius rmax
    V = 4 / 3 * np.pi * rmax**3
    rho = totalpart / npart / V

    for i in range(rsteps):
        rInner = rmax / rsteps * i
        rOuter = rmax / rsteps * (i + 1)
        # V = 4 / 3 * np.pi * (rOuter**3 - rInner**3)
        V = 4 * np.pi * rInner**2 * dr
        g[i] /= V
    
    g /= tsteps * rho
    return g

data = np.genfromtxt('dataYarnell', names=True)
# data2 = np.genfromtxt('data2', names=True)
# data3 = np.genfromtxt('data3', names=True)

sigma = 3.405 ## Angstrom
tsteps = 100
rsteps = 500
rmax = 8 / sigma
npart = 343
dr = rmax / rsteps

g = getRDF(data, tsteps, rsteps, npart)
# g2 = getRDF(data2, tsteps, rsteps, npart)
# g3 = getRDF(data3, tsteps, rsteps, npart)

sns.set(context='notebook', style='darkgrid')
fig, ax = plt.subplots(figsize=(6, 6))

xvalues = np.arange(0, rmax, dr) * sigma
ax.plot(xvalues, g, label=r'$T = 1.409, \rho = 0.84$ (Fluid)')
# ax.plot(xvalues, g2, label=r'Gas and Liquid: $T = 1.0$')
# ax.plot(xvalues, g1, label=r'Fluid: $T = 3.0$')

ax.set_xlim(left=3)
ax.set_ylim(bottom=0)
ax.set_xlabel(r'$r (\AA)$')
ax.set_ylabel(r'$g(r)$')
ax.legend()

fig.savefig("media/rdfYarnell.pdf")
fig.savefig("media/rdfYarnell.svg")
fig.savefig("media/rdfYarnell.png", dpi=200)
plt.show()
