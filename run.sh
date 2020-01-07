
set -euo 'pipefail'

results_dir="c++/results/local_search/"
additional_dir="c++/extra/local_search/"
mkdir -p $results_dir

# ./clean_cmake.sh
cmake . -DCMAKE_BUILD_TYPE=Release
make

for file in ../programming1/instances_final/b*.txt
do
    for i in {1..10}
    do
        out/tsptdmd "${file}" "$results_dir$(basename $file)_$i.txt" "$additional_dir$(basename $file)_$i.txt"
        python3 validate_main.py "$results_dir$(basename $file)_$i.txt"
    done
done
