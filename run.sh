#!/bin/bash

gcc -o mdlj mdlj.c -lm -lgsl  -lgslcblas -lm

### Время памяти
# N=64
# T=1
# rho=0.7
# echo "rx ry rz vx vy vz" > data1
# echo "rx ry rz vx vy vz" > data2
# ./mdlj -N $N -rho $rho -T0 $T -T $T -uf -dt 0.001 -ns 100000 -fs 100 >> data1
# echo "Done first"
# ./mdlj -N $N -rho $rho -T0 $T -T $T -uf -dt 0.0001 -ns 1000000 -fs 1000 >> data2
# 
# python tm.py

### Radial distribution function
# N=1000
# rho=0.840874054 ## 0.0213 * (3.405)^3
# T=1.409411764 ## 85 / 119.8
# echo "rx ry rz vx vy vz" > dataYarnell
# 
# START=$(date +%s.%N)
# 
# ./mdlj -uf -N $N -rho $rho -T0 $T -T $T -dt 0.001 -ns 10000 -fs 100 >> dataYarnell
# 
# # for (( i=0; i<10; i++ ))
# # do
# #     ./mdlj -uf -N $N -rho $rho -T0 $T -T $T -dt 0.001 -ns 10000 -fs 100 >> dataYarnell
# #     echo "i-th iteration done!"
# # done
# 
# END=$(date +%s.%N)
# DIFF=$(echo "$END - $START" | bc)
# 
# echo "Total time: $DIFF"
# 
# python rdf.py

### Diffusion
N=343
rho=0.7
echo "rx ry rz vx vy vz" > dataDif1
echo "rx ry rz vx vy vz" > dataDif2
echo "rx ry rz vx vy vz" > dataDif3

START=$(date +%s.%N)

echo "diffusion"
T=1
./mdlj -uf -N $N -rho $rho -T0 $T -T $T -dt 0.0001 -ns 200000 -fs 1000 -tau 1000 >> dataDif1

echo "Done first"
END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo "time: $DIFF"

T=1.5
./mdlj -uf -N $N -rho $rho -T0 $T -T $T -dt 0.0001 -ns 200000 -fs 1000 -tau 1000 >> dataDif2

echo "Done second"
END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo "time: $DIFF"

T=2
./mdlj -uf -N $N -rho $rho -T0 $T -T $T -dt 0.0001 -ns 200000 -fs 1000 -tau 1000 >> dataDif3

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)

echo "Total time: $DIFF"

python diffusion.py

## VAC
# N=125
# rho=0.7
# echo "rx ry rz vx vy vz" > dataVAC1
# echo "rx ry rz vx vy vz" > dataVAC2
# echo "rx ry rz vx vy vz" > dataVAC3
# 
# START=$(date +%s.%N)
# 
# echo "VAC"
# ## made dt smaller
# T=1
# ./mdlj -uf -N $N -rho $rho -T0 $T -T $T -dt 0.00001 -ns 1000000 -fs 1000 -tau 1000 >> dataVAC1
# 
# echo "Done first"
# END=$(date +%s.%N)
# DIFF=$(echo "$END - $START" | bc)
# echo "time: $DIFF"
# 
# T=1.5
# ./mdlj -uf -N $N -rho $rho -T0 $T -T $T -dt 0.00001 -ns 1000000 -fs 1000 -tau 1000 >> dataVAC2
# 
# echo "Done second"
# END=$(date +%s.%N)
# DIFF=$(echo "$END - $START" | bc)
# echo "time: $DIFF"
# 
# T=2
# ./mdlj -uf -N $N -rho $rho -T0 $T -T $T -dt 0.00001 -ns 1000000 -fs 1000 -tau 1000 >> dataVAC3
# 
# END=$(date +%s.%N)
# DIFF=$(echo "$END - $START" | bc)
# 
# echo "Total time: $DIFF"
# 
# python vac.py

## Influence of the thermostat frequency
# N=343
# rho=0.7
# T=1.5
# 
# START=$(date +%s.%N)
# echo "Thermostat"
# 
# for (( i=10; i<=1510; i+=500 ))
# do
#     echo "rx ry rz vx vy vz" > dataTherm$i
#     ./mdlj -uf -N $N -rho $rho -T0 $T -T $T -dt 0.0001 -ns 200000 -fs 1000 -tau $i >> dataTherm$i
#     echo "$i-th iteration done!"
#     END=$(date +%s.%N)
#     DIFF=$(echo "$END - $START" | bc)
#     echo "time: $DIFF"
# done
