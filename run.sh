
set -euo 'pipefail'

mkdir -p "results/$1"
for file in ../programming1/instances_final/a*.txt
do
    python3 main.py "${file}" "ShortBlockMove" $1
done
