# lookupserv

lookupserv is a telnet based means running FST lookups. When the service is
started, transducer files are opened and pipelines are prepared so that lookups
remain fast.

## Running the server

Take a look at `services.yaml`, and copy to a new file, or edit it. Then run
the service:

    python lookupserv.py services.yaml

Note you may either define an individual command, or a whole pipeline of
commands. As long as this runs on the commandline, then it should run in the
service definition; however preference is to defining paths to utilities
explicitly.

See the help for more:
    
    python lookupserv.py --help

## Connecting as a client

Once the services are running, it is fairly easy to connect and use the
utilities. Simply connect via telnet using the defined ports, then to use a
specific utility, send the name of that utility as the first line after
connecting. Subsequent lines sent to the telnet server are interpreted as input
to the tool, and input is returned.

You can test this in the terminal: 

    $ telnet localhost 9001

(Or whatever port you defined):

    Trying 127.0.0.1...
    Negotiating binary mode with remote host.
    Connected to localhost.
    Escape character is '^]'.
    sme-cg
    mun čálán

    "<mun>"
        "mun" Pron <sme> Pers Sg1 Nom
    "<čálán>"
        "čállit" V <sme> TV Ind Prs Sg1 @+FMAINV

Sending a blank line (press enter) will then disconnect.

## Logging

The output of all tools is logged to `logs/`. If no file exists, then the tool
has not been used yet.

## What this does

The pipelines in `services.yaml` are run in separate threads, as well as the
telnet servers. Telnet clients sockets are connected to pipeline service
threads via [zeromq][zmq].

  [zmq]: zeromq.org/intro:read-the-manual

    Main Process:
        worker-thread-1
        worker-thread-2
        worker-thread-3
        telnet-server-thread-1

Work to each of the worker threads is queued automatically and returned to the
proper serivce and socket.


