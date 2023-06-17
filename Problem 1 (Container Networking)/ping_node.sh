#!/bin/bash

# Declare an associative array
declare -A dictionary

# Add key-value pairs to the dictionary
dictionary["node1"]="172.0.0.2"
dictionary["node2"]="172.0.0.3"
dictionary["node3"]="10.10.0.2"
dictionary["node4"]="10.10.0.3"

# Testing reachability by pinging node $1 and $2
ip netns exec $1 ping ${dictionary[$2]}
