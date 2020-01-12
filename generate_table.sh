
declare -A s_sums_g
declare -A i_sums_g
declare -A s_lists_g
declare -A i_lists_g
for file in c++/extra/genetic/*
do
    IFS=' ' read -r -a array <<< $(cat $file)
    # echo ${array[0]}
    s_lists_g[${array[0]}]="${s_lists_g[${array[0]}]} ${array[3]::-1}"
    i_lists_g[${array[0]}]="${i_lists_g[${array[0]}]} ${array[6]::-1}"
    s_sums_g[${array[0]}]=$((${s_sums_g[${array[0]}]}+${array[3]::-1}))
    i_sums_g[${array[0]}]=$((${i_sums_g[${array[0]}]}+${array[6]::-1}))
    # echo ${s_sums_g[${array[0]}]}
done

declare -A s_sums_l
declare -A i_sums_l
declare -A s_lists_l
declare -A i_lists_l
for file in c++/extra/local_search/*
do
    IFS=' ' read -r -a array <<< $(cat $file)
    # echo ${array[0]}
    s_lists_l[${array[0]}]="${s_lists_l[${array[0]}]} ${array[3]::-1}"
    i_lists_l[${array[0]}]="${i_lists_l[${array[0]}]} ${array[6]::-1}"
    s_sums_l[${array[0]}]=$((${s_sums_l[${array[0]}]}+${array[3]::-1}))
    i_sums_l[${array[0]}]=$((${i_sums_l[${array[0]}]}+${array[6]::-1}))
    # echo ${s_sums_l[${array[0]}]}
done

for i in "${!i_sums_g[@]}"
do
    i_avg_g=$(bc -l <<< "scale=2; ${i_sums_g[$i]}/10")
    s_avg_g=$(bc -l <<< "scale=2; ${s_sums_g[$i]}/10")
    s_stddev_g="0.0"
    i_stddev_g="0.0"
    for e in ${s_lists_g[$i]}
    do
        # echo $e
        s_stddev_g=$(bc -l <<< "scale=2; ${s_stddev_g} + ($s_avg_g-$e)^2")
    done
    for e in ${i_lists_g[$i]}
    do
        # echo $e
        i_stddev_g=$(bc -l <<< "scale=2; ${i_stddev_g} + ($i_avg_g-$e)^2")
    done
    s_stddev_g=$(bc -l <<< "scale=2; sqrt($s_stddev_g/10)")
    i_stddev_g=$(bc -l <<< "scale=2; sqrt($i_stddev_g/10)")\

    i_avg_l=$(bc -l <<< "scale=2; ${i_sums_l[$i]}/10")
    s_avg_l=$(bc -l <<< "scale=2; ${s_sums_l[$i]}/10")
    s_stddev_l="0.0"
    i_stddev_l="0.0"
    for e in ${s_lists_l[$i]}
    do
        # echo $e
        s_stddev_l=$(bc -l <<< "scale=2; ${s_stddev_l} + ($s_avg_l-$e)^2")
    done
    for e in ${i_lists_l[$i]}
    do
        # echo $e
        i_stddev_l=$(bc -l <<< "scale=2; ${i_stddev_l} + ($i_avg_l-$e)^2")
    done
    s_stddev_l=$(bc -l <<< "scale=2; sqrt($s_stddev_l/10)")
    i_stddev_l=$(bc -l <<< "scale=2; sqrt($i_stddev_l/10)")\
    echo "$i & $s_avg_g & $s_stddev_g & $i_avg_g & $i_stddev_g & $s_avg_l & $s_stddev_l & $i_avg_l & $i_stddev_l\\\\"
done
