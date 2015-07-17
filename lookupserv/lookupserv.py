# TODO:
#   accept some sort of connection (TELNET, or SSH)
#   open pipelines in own thread
#   communicate between main thread and child threads with zmq? 

import sys, os

import zmq
context = zmq.Context()

def prepare_utilities(config):
    """ This launches all the threads necessary, and prepares a means to
    communicate with them from the master server process.  """
    from pipelines import Pipeline, PipelineQueue

    utilities = config.get('Utilities')

    utility_defs = {}

    for utility in utilities:
        name = utility.get('name')
        q = PipelineQueue(
            context,
            utility,
        )
        utility_defs[name] = {
            'queue': q,
        }

    return utility_defs

def accept_clients(utilities):
    """ Here we do whatever we need to to listen for requests, and send
    them off to the processes they need to go to.  """

    print utilities
    print 'listening'

    # TODO: will do this over tlnet next
    while True:
        process = raw_input()
        u = utilities.get(process)
        print u
        input_line = raw_input()
        q = u.get('queue')
        sock = q.socket
        print 'sending: ' + input_line
        sock.send(input_line)
        print 'sent'
        message = sock.recv()
        print 'msg: ' + message


def main():
    """ Kick off everything, and start listening.
    """

    import yaml

    services_yaml_file = sys.argv[1]

    with open(services_yaml_file, 'r') as F:
         services_yaml = yaml.load(F)

    utility_defs = prepare_utilities(services_yaml)

    accept_clients(utility_defs)


if __name__ == "__main__":
    sys.exit(main())

