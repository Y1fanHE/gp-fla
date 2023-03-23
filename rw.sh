# parity 4, max tree height 5
for i in $(seq 1 100)
do
    python parity-rw.py 4 $i 5000 5 &
done
wait
zip parity4-5-rw *dat
rm *dat

# parity 4, max tree height 7
for i in $(seq 1 100)
do
    python parity-rw.py 4 $i 5000 7 &
done
wait
zip parity4-7-rw *dat
rm *dat

# parity 4, max tree height 9
for i in $(seq 1 100)
do
    python parity-rw.py 4 $i 5000 9 &
done
wait
zip parity4-9-rw *dat
rm *dat

# parity 6, max tree height 5
for i in $(seq 1 100)
do
    python parity-rw.py 6 $i 5000 5 &
done
wait
zip parity6-5-rw *dat
rm *dat

# parity 6, max tree height 7
for i in $(seq 1 100)
do
    python parity-rw.py 6 $i 5000 7 &
done
wait
zip parity6-7-rw *dat
rm *dat

# parity 6, max tree height 9
for i in $(seq 1 100)
do
    python parity-rw.py 6 $i 5000 9 &
done
wait
zip parity6-9-rw *dat
rm *dat

# nguyen 2, max tree height 5
for i in $(seq 1 100)
do
    python nguyen-rw.py 2 $i 5000 5 &
done
wait
zip nguyen2-5-rw *dat
rm *dat

# nguyen 2, max tree height 7
for i in $(seq 1 100)
do
    python nguyen-rw.py 2 $i 5000 7 &
done
wait
zip nguyen2-7-rw *dat
rm *dat

# nguyen 2, max tree height 9
for i in $(seq 1 100)
do
    python nguyen-rw.py 2 $i 5000 9 &
done
wait
zip nguyen2-9-rw *dat
rm *dat

# nguyen 9, max tree height 5
for i in $(seq 1 100)
do
    python nguyen-rw.py 9 $i 5000 5 &
done
wait
zip nguyen9-5-rw *dat
rm *dat

# nguyen 9, max tree height 7
for i in $(seq 1 100)
do
    python nguyen-rw.py 9 $i 5000 7 &
done
wait
zip nguyen9-7-rw *dat
rm *dat

# nguyen 9, max tree height 9
for i in $(seq 1 100)
do
    python nguyen-rw.py 9 $i 5000 9 &
done
wait
zip nguyen9-9-rw *dat
rm *dat

# ant 1, max tree height 5
for i in $(seq 1 100)
do
    python ant-rw.py 1 $i 5000 5 &
done
wait
zip ant1-5-rw *dat
rm *dat

# ant 1, max tree height 7
for i in $(seq 1 100)
do
    python ant-rw.py 1 $i 5000 7 &
done
wait
zip ant1-7-rw *dat
rm *dat

# ant 1, max tree height 9
for i in $(seq 1 100)
do
    python ant-rw.py 1 $i 5000 9 &
done
wait
zip ant1-9-rw *dat
rm *dat
