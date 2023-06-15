#!/bin/bash

# Array of namespaces
namespaces=("node1" "node2" "node3" "node4")
# Array of host IP addresses
hosts=("172.0.0.2" "172.0.0.3" "10.10.0.2" "10.10.0.3")

echo "*** Testing all nodes reachability"
echo "----------------------------------"

TotalTest=0  # Initialize the counter variable
SuccessTest=0  # Initialize the counter variable
# Iterating over namespaces and trying to ping other nodes
for ((i = 0; i < ${#namespaces[@]}; i++)); do
    echo -n "${namespaces[i]} -> "
    # Iterate over the other hosts and ping them
    for ((j = 0; j < ${#hosts[@]}; j++)); do
        # Skiping the current host itself
        if ((i != j)); then
            # echo ">>> Pinging "${hosts[j]}" with ${namespaces[i]}..."
            if ip netns exec ${namespaces[i]} ping -c 1 -w 1 "${hosts[j]}" > /dev/null 2>&1; then
                echo -n "${namespaces[j]} "
                # Increment 'SuccessTest'
                SuccessTest=$((SuccessTest + 1))
            else
                echo -n "  X   "
            fi
            # Increment 'TotalTest'
            TotalTest=$((TotalTest + 1))
        fi
    done
    echo ""
done

echo "----------------------------------"
echo "*** Results: $SuccessTest/$TotalTest received"
