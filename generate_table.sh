
declare -A solution_sums
declare -A infeasible_sums
declare -A solution_lists
declare -A infeasible_lists
for file in c++/extra/local_search/*
do
    IFS=' ' read -r -a array <<< $(cat $file)
    # echo ${array[0]}
    solution_lists[${array[0]}]="${solution_lists[${array[0]}]} ${array[3]::-1}"
    infeasible_lists[${array[0]}]="${infeasible_lists[${array[0]}]} ${array[6]::-1}"
    solution_sums[${array[0]}]=$((${solution_sums[${array[0]}]}+${array[3]::-1}))
    infeasible_sums[${array[0]}]=$((${infeasible_sums[${array[0]}]}+${array[6]::-1}))
    # echo ${solution_sums[${array[0]}]}
done
for i in "${!solution_sums[@]}"
do
    infeasible_avg=$(bc -l <<< "scale=2; ${infeasible_sums[$i]}/10")
    solution_avg=$(bc -l <<< "scale=2; ${solution_sums[$i]}/10")
    solution_stddev="0.0"
    infeasible_stddev="0.0"
    for e in ${solution_lists[$i]}
    do
        echo $e
        solution_stddev=$(bc -l <<< "scale=2; ${solution_stddev} + ($solution_avg-$e)^2")
    done
    for e in ${infeasible_lists[$i]}
    do
        echo $e
        infeasible_stddev=$(bc -l <<< "scale=2; ${infeasible_stddev} + ($infeasible_avg-$e)^2")
    done
    solution_stddev=$(bc -l <<< "scale=2; sqrt($solution_stddev/10)")
    infeasible_stddev=$(bc -l <<< "scale=2; sqrt($infeasible_stddev/10)")
    echo $i $solution_avg $solution_stddev $infeasible_avg $infeasible_stddev
done