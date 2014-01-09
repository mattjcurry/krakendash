#!/usr/bin/env bash
screen -S api sudo ceph-rest-api -c /etc/ceph/ceph.conf --cluster ceph -i admin
