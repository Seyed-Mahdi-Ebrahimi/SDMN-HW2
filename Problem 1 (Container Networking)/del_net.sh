#!/bin/bash
ip link del br1
ip link del br2
ns=("node1" "node2" "node3" "node4" "router")
for i in $(seq 0 $((${#ns[@]}-1))); do ip netns del "${ns[$i]}"; done