# TODO: backup and clear lexical parts of database
# TODO: test lookup and install commands

import os, sys

from fabric.decorators import roles

from fabric.api import ( cd
                       , run
                       , local
                       , env
                       , task
                       )

from fabric.operations import ( sudo )

from fabric.colors import red, green, cyan, yellow

from fabric.contrib.console import confirm

from fabric.utils import abort

env.use_ssh_config = True
env.no_svn_up = False
# env.key_filename = '~/.ssh/neahtta'

import socket
env.real_hostname = socket.gethostname()

# @task
# def local(*args, **kwargs):
#     """ Run a command using the local environment.
#     """
#     from fabric.operations import local as lrun
#     import os

#     env.run = lrun
#     env.hosts = ['localhost']

#     gthome = os.environ.get('GTHOME')
#     env.path_base = os.getcwd()

#     env.svn_path = gthome
#     env.dict_path = os.path.join(env.path_base, 'dicts')
#     env.neahtta_path = env.path_base
#     env.i18n_path = os.path.join(env.path_base, 'translations')

#     # Make command needs to include explicit path to file, because of
#     # fabric.
#     env.make_cmd = "make -C %s -f %s" % ( env.dict_path
#                                         , os.path.join(env.dict_path, 'Makefile')
#                                         )
#     env.remote_no_fst = False

@task
def gtlab():
    """ Run a command remotely on gtweb
    """
    env.run = run
    env.hosts = ['ryan@gtlab.uit.no']
    env.path_base = '/home/ryan'

    env.svn_path = env.path_base + '/gtsvn'
    env.univ_oahpa_path = env.svn_path + '/ped/univ_oahpa'
    env.meta_data_path = env.svn_path + '/ped'

    # env.make_cmd = "make -C %s -f %s" % ( env.dict_path
    #                                     , os.path.join(env.dict_path, 'Makefile')
    #                                     )

@task
def redeploy():
    """ SVN up some places and re-run the fastcgi initiation process """
    if env.no_svn_up:
        print(yellow("** skipping svn up **"))
        return

    with cd(env.meta_data_path):
        paths = [
            'sme',
            'univ_oahpa',
        ]
        print(cyan("** svn up **"))

        for p in paths:
            _p = os.path.join(env.meta_data_path, p)
            with cd(_p):
                env.run('svn up ' + _p)

        restart_service()

@task
def restart_service(dictionary=False):
    """ Restarts the service. """
    fail = False

    with cd(env.univ_oahpa_path):
        print(cyan("** Restarting fastcgi process"))
        stop = env.run("sh run_fastcgi_courses_test.sh")
        if not stop.failed:
            print(green("** Success"))
        else:
            fail = True

    if fail:
        print(red("** something went wrong while restarting <%s> **" % dictionary))

