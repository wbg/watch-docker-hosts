## watch-docker-hosts

Watches docker events and adds hostnames for docker containers to /etc/hosts i.e. makes it easy to access every docker container by its hostname directly from the host machine. 

See this quick hack as a starting point for your own version.

### reasons

My development setup is quite simple: for each project i create a docker-compose file, add the required services and give each container a dedicated hostname. During develoment i want to be able to access each container using its hostname (think access to a db, queue or something else) and dont want to worry about port forwading or complex service discovery tools.

So this script simply expects a docker container with a hostname and as soon as a container starts it adds an entry containing IP + hostname + _docker_ as a postfix to ```/etc/hosts```.

e.g. for a compose file like
```
web:
  image: httpd
  hostname: my-webserver
  # ...
```

a new hosts entry like
```
172.18.0.2 my-webserver.docker
```
will be added and the service can be reached using http://my-webserver.docker/ in your browser.

If you need more than that - i.e. a polished, solid and complex tool - there is always the awesome [dnsdock](https://github.com/aacebedo/dnsdock) solution.

### howto

This script expects a working docker as well a python installation. Furthermore it needs the [docker-py](https://github.com/docker/docker-py) library that can be installed with pip:
```
pip install docker-py
```

You can run this script standalone with python using something like:
```
python watch-docker-hosts.py
```

I prefer to add it to my init system - e.g. for systemd you can create a new service by adding the following content to ```/lib/systemd/system/watch-docker-hosts.service```.
```
[Unit]
Description=Watch Docker Hosts
After=docker.service

[Service]
Type=idle
ExecStart=/usr/bin/python /path/to/watch-docker-hosts.py 

[Install]
WantedBy=default.target
```

To enable this service on startup and start it for the first time simply issue the following commands:
```
sudo systemctl enable watch-docker-hosts
sudo systemctl start watch-docker-hosts
```

### warning

This ist just a quick script for my personal needs so dont expect it to work for you :-)