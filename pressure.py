import numpy as np

for T in range(10, 91, 10):
    data = np.genfromtxt('dataRiceParam' + str(T), names=True)
    print("P = ", np.average(data['P']))
