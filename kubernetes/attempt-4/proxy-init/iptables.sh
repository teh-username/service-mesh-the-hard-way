#!/bin/sh

# Create POD_INBOUND chain
iptables -t nat -N POD_INBOUND

# Create POD_OUTBOUND chain
iptables -t nat -N POD_OUTBOUND

# Create PROXY_REDIRECT chain
iptables -t nat -N PROXY_REDIRECT

# Redirect all INBOUND tcp packets to POD_INBOUND chain for processing
iptables -t nat -A PREROUTING -p tcp -j POD_INBOUND

# Don't route to proxy any traffic not meant for the declared service ports
iptables -t nat -A POD_INBOUND -p tcp ! -m multiport --dports $SERVICE_PORTS -j RETURN

# Redirect all traffic to the declared service ports to the proxy ingress
iptables -t nat -A POD_INBOUND -p tcp -j REDIRECT --to-ports $PROXY_INGRESS_PORT

# Redirect all OUTBOUND tcp packets to POD_OUTBOUND chain for processing
iptables -t nat -A OUTPUT -p tcp -j POD_OUTBOUND

# Redirect all non-interpod traffic to PROXY_REDIRECT chain
iptables -t nat -A POD_OUTBOUND ! -d 127.0.0.1/32 -o lo -j PROXY_REDIRECT

# Don't process proxy related traffic
iptables -t nat -A POD_OUTBOUND -m owner --uid-owner $UID -j RETURN
iptables -t nat -A POD_OUTBOUND -m owner --gid-owner $GID -j RETURN

# Don't process inter-pod traffic
iptables -t nat -A POD_OUTBOUND -d 127.0.0.1/32 -j RETURN

# Everything else, redirect through the proxy
iptables -t nat -A POD_OUTBOUND -j PROXY_REDIRECT

# All traffic in PROXY_OUTBOUND goes through the proxy egress
iptables -t nat -A PROXY_REDIRECT -p tcp -j REDIRECT --to-ports $PROXY_EGRESS_PORT
