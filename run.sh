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
# N=343
# rho=0.5
# echo "rx ry rz vx vy vz" > data1
# echo "rx ry rz vx vy vz" > data2
# echo "rx ry rz vx vy vz" > data3
# 
# T=3 ## Fluid
# ./mdlj -uf -N $N -rho $rho -T0 $T -T $T -dt 0.001 -ns 100000 -fs 1000 >> data1
# 
# echo "First done!"
# 
# T=1.0 ## Gas and Liquid
# ./mdlj -uf -N $N -rho $rho -T0 $T -T $T -dt 0.001 -ns 100000 -fs 1000 >> data2
# 
# echo "Second done!"
# 
# T=0.3 ## Gas and solid
# ./mdlj -uf -N $N -rho $rho -T0 $T -T $T -dt 0.001 -ns 100000 -fs 1000 >> data3
# 
# echo "Almost done!"
# 
# python rdf.py

### Diffusion
N=343
rho=0.8
T=2 ## Fluid
echo "rx ry rz vx vy vz" > dataDif

./mdlj -uf -N $N -rho $rho -T0 $T -T $T -dt 0.0001 -ns 100000 -fs 1000 >> dataDif

echo "Almost done!"

python diffusion.py
