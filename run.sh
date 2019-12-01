
set -euo 'pipefail'

mkdir -p "results/$2"
for prefix in 0 a b
do
    for file in ../programming1/instances_final/$prefix*.txt
    do
        python3 main.py "${file}" $1 $2 $3
    done
done
