#!/usr/bin/python

# This file is a part of watch-docker-hosts
# MIT
#
# Copyright (C) 2016 Roman Weinberger <rw@roman-weinberger.net>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.)

from docker import Client
import os

def ip_and_host_for_id(id):
    info = cli.inspect_container(id)
    hostname = info['Config']['Hostname'] + '.docker'
    network, nwinfo = info['NetworkSettings']['Networks'].popitem()
    ip = nwinfo['IPAddress']
    return ip, hostname

def disable_hosts_ip(ip):
    """Remove existing entries for this IP from /etc/hosts"""
    return os.system('sed -i.back -e "/^\\('+ip+'.*\\)$/d" /etc/hosts')

def disable_hosts_hostname(hostname):
    """Remove existing entries for this Hostname from /etc/hosts"""
    return os.system('sed -i.back -e "/^\\(.* '+hostname+'\\)$/d" /etc/hosts')

def enable_new_hostname(hostname, ip):
    """Add a new entry for this IP/Hostname to /etc/hosts"""
    return os.system('echo "'+ip+' '+hostname+'" >> /etc/hosts')

if __name__ == "__main__":
    cli = Client(base_url='unix://var/run/docker.sock')
    events = cli.events(decode=True)
    for event in events:
        if event['Type'] == "container" and event['Action'] == 'start':
            # new container => get ip adress and update
            ip, hostname = ip_and_host_for_id(event['id']) 
            print("New DockerHost: " + hostname + " => " + ip)
            disable_hosts_ip(ip)
            enable_new_hostname(hostname, ip)
        elif event['Type'] == "container" and event['Action'] == 'stop':
            ip, hostname = ip_and_host_for_id(event['id']) 
            print("Stopped DockerHost: " + hostname + " => " + ip)
            disable_hosts_hostname(hostname)
        


