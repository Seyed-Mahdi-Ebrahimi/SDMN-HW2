# First, we make the switches and up them
ip link add br1 type bridge
ip link add br2 type bridge
ip link set br1 up
ip link set br2 up

# This is the main and only function of the program.
SetupNode () {
  ip netns add $1 2>/dev/null
  ip link add $2-veth type veth peer name br-$2-veth
  ip link set $2-veth netns $1
  ip link set br-$2-veth master $4
  ip -n $1 addr add $3 dev $2-veth
  ip -n $1 link set dev $2-veth up 
  ip -n $1 link set dev lo up
  ip link set br-$2-veth up
  if [ ! -z "$5" ]
    then
      ip netns exec $1 ip route add default via $5
  fi
}

# Here, nodes are defined.
SetupNode "node1" "n1" "172.0.0.2/24" "br1" "172.0.0.1" 
SetupNode "node2" "n2" "172.0.0.3/24" "br1" "172.0.0.1"
SetupNode "node3" "n3" "10.10.0.2/24" "br2" "10.10.0.1"
SetupNode "node4" "n4" "10.10.0.3/24" "br2" "10.10.0.1"
# And here, router 'hands' are defined that connect two different subnets together.
SetupNode "router" "hand1" "172.0.0.1/24" "br1"
SetupNode "router" "hand2" "10.10.0.1/24" "br2"

# Here we bypass 'iptables processing' so that packets can be exchanged between different namespaces.
sysctl --write net.bridge.bridge-nf-call-iptables=0
sysctl --write net.bridge.bridge.bridge-nf-call-ip6tables=0
sysctl --write net.bridge.bridge-nf-call-arptables=0
# It applies the changes without rebooting
sysctl -p
