"""

Usage:
    lookupserv.py <yaml_config_file> [-hdv] [--clear-logs]

Options:
    -h --help       Print this message.
    -v --verbose    Verbose
    -d --debug      Do not launch clients, but provide local session.
    --clear-logs    Clear logs on launch

"""

import sys, os

import zmq
context = zmq.Context()

def prepare_utilities(config, cmd_args):
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

def run_local_session(utilities, cmd_args):
    """ Here we only listen on the local commandline.  """

    while True:
        print "choose service?"
        process = raw_input()
        u = utilities.get(process, False)
        if not u:
            print "Invalid service, choose one of:"
            print utilities.keys()
            continue
        print "listening for"
        print u
        while True:
            input_line = raw_input()

            if len(input_line.strip()) == 0:
                sys.exit()

            q = u.get('queue')
            sock = q.socket
            sock.send(input_line)
            message = sock.recv()
            print >> sys.stdout, message

def accept_clients(service_defs, utilities, cmd_args):
    """ Here we do whatever we need to to listen for requests, and send
    them off to the processes they need to go to.  """
    from servers import TelnetListener
    import time

    servers = {}

    for service in service_defs:
        name = service.get('name')
        listener = TelnetListener(service, utilities)
        servers[name] = listener
        listener.start()

    while True:
        time.sleep(0.02)


def erase_logs():
    print >> sys.stderr, "Deleting logs:"
    for f in os.listdir('logs/'):
        f_path = os.path.join('logs/', f)
        print >> sys.stderr, f_path
        os.remove(f_path)

def check_paths():
    # socket_tmp/ logs/
    try: os.mkdir('logs')
    except OSError: pass

    try: os.mkdir('socket_tmp')
    except OSError: pass

def main():
    """ Kick off everything, and start listening.
    """
    from docopt import docopt
    import yaml
    check_paths()

    cmd_arguments = docopt(__doc__, version='Lookupserv 0.1.0')

    services_yaml_file = cmd_arguments.get('<yaml_config_file>')

    clear_logs = cmd_arguments.get('--clear-logs')

    if clear_logs:
        erase_logs()

    with open(services_yaml_file, 'r') as F:
         services_yaml = yaml.load(F)

    utility_defs = prepare_utilities(services_yaml, cmd_arguments)

    if cmd_arguments.get('--debug', False):
        run_local_session(utility_defs, cmd_arguments)
    else:
        accept_clients(services_yaml.get('Services'), utility_defs, cmd_arguments)


if __name__ == "__main__":
    sys.exit(main())

