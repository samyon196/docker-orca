import sys
import yaml
import docker

def read_configuration(filename):
    with open(filename, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def system_up(config, project_name):
    print("starting")
    # 1. Create networks
    # 2. Start containers
    # 3. Disconnect from none
    # 4. Connect to networks as needed, config network interface
    # 5. Execute commands inside containers after all network is ready
    print("config is " + str(read_configuration(sys.argv[2])))

def system_down(config, project_name):
    print("stopping")

# Run using: docker-orca.py <start/stop> <cfg_file> <name>
if __name__ == "__main__":
    
    # Load parameters
    opname = sys.argv[1] 
    config = read_configuration(sys.argv[2])
    project_name = sys.argv[3]

    # Apply appropriate function
    if opname == 'up':
        system_up(config, project_name)
    elif opname == 'down':
        system_down(config, project_name)
    else:
        print('wrong use')