import sys
import yaml

def read_configuration(filename):
    with open(filename, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def system_up():
    print("starting")
    print("config is " + str(read_configuration(sys.argv[2])))

def system_down():
    print("stopping")

# Run using: docker-orca.py <start/stop> <
if __name__ == "__main__":
    opname = sys.argv[1] 
    if opname == 'up':
        system_up()
    elif opname == 'down':
        system_down()
    else:
        print('wrong use')