
for file in c++/extra/local_search/*
do
    IFS=' ' read -r -a array <<< $(cat $file)
    echo ${array[3]}
    python3 validate_main.py c++/results/local_search/$(basename $file)
done