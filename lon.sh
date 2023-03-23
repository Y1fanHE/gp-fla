# parity 4, max tree height 5
for i in $(seq 1 100)
do
    python parity.py 4 $i 100 5 &
done
wait
zip parity4-5 *dat
rm *dat

# parity 4, max tree height 7
for i in $(seq 1 100)
do
    python parity.py 4 $i 100 7 &
done
wait
zip parity4-7 *dat
rm *dat

# parity 4, max tree height 9
for i in $(seq 1 100)
do
    python parity.py 4 $i 100 9 &
done
wait
zip parity4-9 *dat
rm *dat

# parity 6, max tree height 5
for i in $(seq 1 100)
do
    python parity.py 6 $i 1000 5 &
done
wait
zip parity6-5 *dat
rm *dat

# parity 6, max tree height 7
for i in $(seq 1 100)
do
    python parity.py 6 $i 1000 7 &
done
wait
zip parity6-7 *dat
rm *dat

# parity 6, max tree height 9
for i in $(seq 1 100)
do
    python parity.py 6 $i 1000 9 &
done
wait
zip parity6-9 *dat
rm *dat

# nguyen 2, max tree height 5
for i in $(seq 1 100)
do
    python nguyen.py 2 $i 5000 5 &
done
wait
zip nguyen2-5 *dat
rm *dat

# nguyen 2, max tree height 7
for i in $(seq 1 100)
do
    python nguyen.py 2 $i 5000 7 &
done
wait
zip nguyen2-7 *dat
rm *dat

# nguyen 2, max tree height 9
for i in $(seq 1 100)
do
    python nguyen.py 2 $i 5000 9 &
done
wait
zip nguyen2-9 *dat
rm *dat

# nguyen 9, max tree height 5
for i in $(seq 1 100)
do
    python nguyen.py 9 $i 5000 5 &
done
wait
zip nguyen9-5 *dat
rm *dat

# nguyen 9, max tree height 7
for i in $(seq 1 100)
do
    python nguyen.py 9 $i 5000 7 &
done
wait
zip nguyen9-7 *dat
rm *dat

# nguyen 9, max tree height 9
for i in $(seq 1 100)
do
    python nguyen.py 9 $i 5000 9 &
done
wait
zip nguyen9-9 *dat
rm *dat

# ant 1, max tree height 5
for i in $(seq 1 100)
do
    python ant.py 1 $i 1000 5 &
done
wait
zip ant1-5 *dat
rm *dat

# ant 1, max tree height 7
for i in $(seq 1 100)
do
    python ant.py 1 $i 1000 7 &
done
wait
zip ant1-7 *dat
rm *dat

# ant 1, max tree height 9
for i in $(seq 1 100)
do
    python ant.py 1 $i 1000 9 &
done
wait
zip ant1-9 *dat
rm *dat
