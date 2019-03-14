#!/bin/sh

# Create POD_OUTBOUND chain
iptables -t nat -N POD_OUTBOUND

# Create PROXY_REDIRECT chain
iptables -t nat -N PROXY_REDIRECT

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
iptables -t nat -A PROXY_REDIRECT -p tcp -j REDIRECT --to-ports $PROXY_PORT
