# containerized_deploy

This directory contains a Dockerfile that will build an image that runs
the oahpa services. 


# Explaining the setup

The setup is similar to how the old gtoahpa-01 did it. It runs uwsgi
as the orchistrator for the various instances, one per language. The
configuration for each instance is located in `uwsgi_vassals/` as `.ini` files.
All traffic is routed through nginx (see its configuration in `nginx.conf`).
Static data goes straight to `/var/www/html`, while all dynamic content does a
`proxy_pass` to the uwsgi instance that it needs to go to.

The database is built in, and runs as part of the image, too. This means that
the container will run 4 services: uwsgi, nginx, mariadb-server, and finally,
to control it all, supervisord.

The diagram of the traffic flow would be something like this:

Local setup (`make run`):

```
User's browser --> *CONTAINER* [nginx] ---- proxy_pass ----> uwsgi-instance
```

On `gtoahpa-02`:

```
User's browser ---> global nginx ---> *CONTAINER* [nginx inside container] ----
                                                                              |
                                       uwsgi instance <-----proxy_pass- -------
```


# Building the image

Running `make image` will invoke `podman` to build the image, and tag it as
`oahpa_all`. It's a very simple command, so refer to the `Makefile` for how
it works, and change `podman` with `docker`, or what else you want to do.

Note:

1. There are many steps in the `Dockerfile`, so building it takes a while.
Just building python2 alone takes a lot of time. Have patience.
2. The resulting image is *5.52GB*. Intermediary images may also take up some
space, so make sure you're not low on space on your hard drive. Refer to podman
documentation on how to remove the image, and intermediary stage images, if
you want to delete the built image from your system to save space.
3. It downloads various packages from PyPI. At the time of writing, 2024-09-24,
these are all available, but in the future they may not be. *TODO: Possible
to download these packages, and keep them as part of this folder, so we're
not dependent on these packages existing forever on PyPI?*

(As a side note to (3), I will assume that the python2 tarball will be available
on python.org for the forseeable future. It even contains python1 releases.
Also, I do _not_ assume that mysql-5.6.51 will be available on Oracle's sites
forever, hence why it has been copied here.)


# Running the image

A simple `make run` will run the image locally. You can now access the services
on [http://localhost:5000/davvi/](http://localhost:5000/davvi/) (replace
`davvi` with the instance you want to take a look at).


# List of files

```text
Dockerfile                    The dockerfile to build the image
*_oahpa.sql.gz                Dump of the old database on gtoahpa-01
Makefile                      Common tasks, like building and running
init_db.sh                    Script run inside the building container
                              which imports the database.
lookup                        lookup binary, as retrieved from gtoahpa-01
media                         the media directory, all static
my.cnf                        MySql configuration
mysql-5.6.51-linux-glibc2.12-x86_64.tar.gz
                              Old, compatible version of mysql, downloaded
                              from Oracle's archive websites
nginx.conf                    Nginx configuration
ped-sme.fst                   .fst retrieved from old gtoahpa-01
roll_keys.sh                  Script to write new SECRET_KEYs to the
                              settings_not_in_svn.py scripts for each instance.
sjd_oahpa.ini                 UNUSED. This is a vassal description file,
                              which is _not_ in use. All the ones that are
                              in use, is in uwsgi_vassals/
sme-num.fst                   An old .fst file downloaded from gtoahpa-01
supervisord.conf              Supervisord configuration
uwsgi-plugin-python_2.0.18-1_amd64.deb
                              An old debian package which we need, that has
                              been removed from newer versions of debian.
                              The image is based on debian:bookworm, and
                              this package has been removed from bookworm.
                              It was retrieved from the buster archives.
uwsgi.ini                     uwsgi configuration
uwsgi_vassals                 uwsgi vassals (descriptions on how to run each
                              instance of oahpa - one per language)
```


# Dumping the old database

Dumping the database was done through this command, on `gtoahpa-01`:

```bash
mysqldump --password=PASSWORD -u USER DATABASE --no-tablespaces | gzip -c > INSTANCE.sql.gz
```

Replace `PASSWORD` with the password for that database. It is found in the
`settings_not_in_svn.py` file for the corresponding instance. User is always
`LANG_oahpa` (where `lang` is the 3-letter language code). Database is the same
as user.


# Other notes

The `settings_not_in_svn.py` files found in `*_oahpa_project/`, are directly
copied from the old running `gtoahpa-01` server. The `roll_keys.sh` script
makes sure to write new `SECRET_KEY`s to those files, so that the ones that
are present in the files in the repository, is just for demonstrative purposes.


# Hosting it on gtoahpa-02

On `gtoahpa-02`, this image is run by systemd. The service file is 
`/etc/systemd/system/oahpa_all.service`. The user `services` runs the image.
The globally installed nginx has `location` blocks for each of the names of
the instances, so that `/davvi` (etc) will `proxy_pass` to nginx in the
container.
