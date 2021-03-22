#!/bin/bash

# gcc -o mdlj mdlj.c -lm -lgsl  -lgslcblas -lm

### Время памяти
# N=64
# T=0.44
# rho=0.5
# echo "rx ry rz vx vy vz" > data1
# echo "rx ry rz vx vy vz" > data2
# ./mdlj -N $N -rho $rho -T0 $T -T $T -uf -dt 0.001 -ns 10000 -fs 100 >> data1
# ./mdlj -N $N -rho $rho -T0 $T -T $T -uf -dt 0.0001 -ns 100000 -fs 1000 >> data2
# 
# python tm.py

### Radial distribution function
N=343
rho=0.840874054 ## 0.0213 * (3.405)^3
T=1.409411764 ## 85 / 119.8
echo "rx ry rz vx vy vz" > dataYarnell

START=$(date +%s.%N)

for (( i=0; i<10; i++ ))
do
    ./mdlj -uf -N $N -rho $rho -T0 $T -T $T -dt 0.001 -ns 10000 -fs 100 >> dataYarnell
    echo "i-th iteration done!"
done

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "Total time: $DIFF"

python rdf.py

### Diffusion
# N=343
# rho=0.8
# T=2 ## Fluid
# echo "rx ry rz vx vy vz" > dataDif
# 
# ./mdlj -uf -N $N -rho $rho -T0 $T -T $T -dt 0.0001 -ns 100000 -fs 1000 >> dataDif
# 
# echo "Almost done!"
# 
# python diffusion.py
