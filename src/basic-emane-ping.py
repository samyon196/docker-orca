import docker
import sys
import os
import time

d = docker.from_env()

# Prune the system 
print("[0/10] Cleaning all docker stuff")
os.system("docker rm -f $(docker ps -aq)")
d.networks.prune()
d.containers.prune()    

# Create docker networks :)
print("[1/10] Creating networks")
ipam_pool1 = docker.types.IPAMPool(
    subnet='100.0.5.0/24',
    gateway='100.0.5.254'
)
ipam_pool2 = docker.types.IPAMPool(
    subnet='100.0.10.0/24',
    gateway='100.0.10.254'
)
ipam_pool3 = docker.types.IPAMPool(
    subnet='200.0.0.0/24',
    gateway='200.0.0.254'
)
ipam_config1 = docker.types.IPAMConfig(
    pool_configs=[ipam_pool1]
)
ipam_config2 = docker.types.IPAMConfig(
    pool_configs=[ipam_pool2]
)
ipam_config3 = docker.types.IPAMConfig(
    pool_configs=[ipam_pool3]
)
d.networks.create("tank1", driver="bridge", ipam=ipam_config1)
d.networks.create("tank2", driver="bridge", ipam=ipam_config2)
d.networks.create("ota", driver="bridge", ipam=ipam_config3)

# Spin up containers
print("[2/10] Creating containers...")
d.containers.run(name="terminal1", hostname="terminal1", detach=True, image="emane20", privileged=True, tty=True, network="none")
d.containers.run(name="terminal2", hostname="terminal2", detach=True, image="emane20", privileged=True, tty=True, network="none")
d.containers.run(name="radio1", hostname="radio1", detach=True, image="emane20", privileged=True, tty=True, network="none")
d.containers.run(name="radio2", hostname="radio2", detach=True, image="emane20", privileged=True, tty=True, network="none")

# Disconnect from none
print("[3/10] Removing none network...")
d.networks.get("none").disconnect("terminal1")
d.networks.get("none").disconnect("terminal2")
d.networks.get("none").disconnect("radio1")
d.networks.get("none").disconnect("radio2")

print("[4/10] Connecting radios to ota network")
d.networks.get("ota").connect("radio1")
d.networks.get("ota").connect("radio2")

# OTA Channel
print("[5/10] Connecting tank1...")
d.networks.get("tank1").connect("radio1")
d.networks.get("tank1").connect("terminal1")

print("[6/10] Connecting tank2...")
d.networks.get("tank2").connect("radio2")
d.networks.get("tank2").connect("terminal2")

print("[7/10] Set radio as dg for terminasl...")
d.containers.get("terminal1").exec_run(cmd="ip route del default")
d.containers.get("terminal1").exec_run(cmd="ip route add default via 100.0.5.1")
d.containers.get("terminal2").exec_run(cmd="ip route del default")
d.containers.get("terminal2").exec_run(cmd="ip route add default via 100.0.10.1")

# START EMANE. SET EMANE0 AS DG 
# DERIVE RADIO IP FROM APP LAN SUBNET..
print("[8/10] Enable ipv4 forwarding in radios")
d.containers.get("radio1").exec_run(cmd="sysctl -w net.ipv4.ip_forward=1")
d.containers.get("radio2").exec_run(cmd="sysctl -w net.ipv4.ip_forward=1")
# App bus



# Execute..

print("[9/10] Done !.")