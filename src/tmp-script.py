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
    subnet='111.11.1.0/24',
    gateway='111.11.1.254'
)
ipam_pool2 = docker.types.IPAMPool(
    subnet='222.22.2.0/24',
    gateway='222.22.2.254'
)
ipam_config1 = docker.types.IPAMConfig(
    pool_configs=[ipam_pool1]
)
ipam_config2 = docker.types.IPAMConfig(
    pool_configs=[ipam_pool2]
)
d.networks.create("net1", driver="bridge", ipam=ipam_config1)
d.networks.create("net2", driver="bridge", ipam=ipam_config2)

# Spin up containers
print("[2/10] Creating containers...")
d.containers.run(name="terminal1", detach=True, image="emane20", privileged=True, tty=True, network="none")
d.containers.run(name="terminal2", detach=True, image="emane20", privileged=True, tty=True, network="none")
d.containers.run(name="router", detach=True, image="emane20", privileged=True, tty=True, network="none")

# Disconnect from none
print("[3/10] Removing none network...")
d.networks.get("none").disconnect("terminal1")
d.networks.get("none").disconnect("terminal2")
d.networks.get("none").disconnect("router")
 
print("[4/10] Connecting router to nets")
d.networks.get("net1").connect("router")
d.networks.get("net2").connect("router")

# OTA Channel
print("[5/10] Connecting terminals to net...")
d.networks.get("net1").connect("terminal1")
d.networks.get("net2").connect("terminal2")

time.sleep(3)
print("[6/10] Set router as dg for containers...")
d.containers.get("terminal1").exec_run(cmd="ip route del default")
d.containers.get("terminal1").exec_run(cmd="ip route add default via 111.11.1.1")
d.containers.get("terminal2").exec_run(cmd="ip route del default")
d.containers.get("terminal2").exec_run(cmd="ip route add default via 222.22.2.1")

print("[7/10] Enable ipv4 forwarding in router")
d.containers.get("router").exec_run(cmd="sysctl -w net.ipv4.ip_forward=1")
# App bus



# Execute..

print("[8/10] Done !.")