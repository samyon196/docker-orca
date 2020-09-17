import sys
import yaml

# Run using: docker-orca.py <start/stop> <
if __name__ == "__main__":
    opname = sys.argv[1] 
    if opname == 'start':
        print('starting')
    elif opname == 'stop':
        print('stopping')
    else:
        print('wrong use')