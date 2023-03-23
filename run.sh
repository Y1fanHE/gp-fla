for i in $(seq 1 30)
do
    python parity-gp-map.py 4 $i
done
wait
zip parity4-gp-map *dat
rm *dat

for i in $(seq 1 30)
do
    python parity-gp.py 4 $i
done
wait
zip parity4-gp *dat
rm *dat

for i in $(seq 1 30)
do
    python parity-gp-map.py 6 $i
done
wait
zip parity6-gp-map *dat
rm *dat

for i in $(seq 1 30)
do
    python parity-gp.py 6 $i
done
wait
zip parity6-gp *dat
rm *dat

for i in $(seq 1 30)
do
    python parity-gp-map.py 9 $i
done
wait
zip parity9-gp-map *dat
rm *dat

for i in $(seq 1 30)
do
    python parity-gp.py 9 $i
done
wait
zip parity9-gp *dat
rm *dat

for i in $(seq 1 30)
do
    python parity-gp-map.py 11 $i
done
wait
zip parity11-gp-map *dat
rm *dat

for i in $(seq 1 30)
do
    python parity-gp.py 11 $i
done
wait
zip parity11-gp *dat
rm *dat

for i in $(seq 1 30)
do
    python nguyen-gp-map.py 2 $i
done
wait
zip nguyen2-gp-map *dat
rm *dat

for i in $(seq 1 30)
do
    python nguyen-gp.py 2 $i
done
wait
zip nguyen2-gp *dat
rm *dat

for i in $(seq 1 30)
do
    python nguyen-gp-map.py 6 $i
done
wait
zip nguyen6-gp-map *dat
rm *dat

for i in $(seq 1 30)
do
    python nguyen-gp.py 6 $i
done
wait
zip nguyen6-gp *dat
rm *dat

for i in $(seq 1 30)
do
    python nguyen-gp-map.py 9 $i
done
wait
zip nguyen9-gp-map *dat
rm *dat

for i in $(seq 1 30)
do
    python nguyen-gp.py 9 $i
done
wait
zip nguyen9-gp *dat
rm *dat

for i in $(seq 1 30)
do
    python nguyen-gp-map.py 10 $i
done
wait
zip nguyen10-gp-map *dat
rm *dat

for i in $(seq 1 30)
do
    python nguyen-gp.py 10 $i
done
wait
zip nguyen10-gp *dat
rm *dat

for i in $(seq 1 30)
do
    python ant-gp-map.py 1 $i
done
wait
zip ant1-gp-map *dat
rm *dat

for i in $(seq 1 30)
do
    python ant-gp.py 1 $i
done
wait
zip ant1-gp *dat
rm *dat

for i in $(seq 1 30)
do
    python ant-gp-map.py 2 $i
done
wait
zip ant2-gp-map *dat
rm *dat

for i in $(seq 1 30)
do
    python ant-gp.py 2 $i
done
wait
zip ant2-gp *dat
rm *dat
