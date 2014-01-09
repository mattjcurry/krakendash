# kraken

A free Ceph dashboard for stats and monitoring

You can see what it looks like [here](http://imgur.com/a/JoVPy)

## Installation and Roadmap

### Prerequisites:

The ceph-rest-api must be run on either a member of your Ceph cluster, or on a installed client node that has admin access to the cluster.

do:
```
apt-get install git
apt-get install python-pip
pip install django
pip install requests
```

### Installation:

create a new user called kraken then:
```
  cd /home/kraken
  git clone https://github.com/krakendash/krakendash
```
  
In the krakendash/contrib directory there are two files, api.sh and django.sh

```
cp krakendash/contrib/*.sh .
```

api.sh starts the ceph-rest-api in a screen session called api
django.sh starts krakendash in a screen session called django

You can run these files to kick off the api and application. To detach a screen session, use CTRL-A, then his the D key.

Now you can run Kraken!

in /home/kraken do:
./api.sh (if you are running kraken on a ceph client or cluster node)
./django.sh
  
  
Also, if needed, edit krakendash/kraken/kraken/settings.py

Here you can change CEPH_BASE_URL to point at your host running ceph-rest-api, it is preconfigured already for localhost.
You can also change the STATICFILES_DIRS and TEMPLATE_DIRS if you are using a different username than kraken.



## Phase One
- [x] Cluster status
- [x] List pools, size
- [x] Pool status
- [x] Cluster data usage
- [x] MON status
- [x] OSD status

## Phase Two
- [] Advanced metrics
- [] Better graphs
- [x] Multi-MON support
- [] Better UI

## Phase Three
- [] RPC
- [] Remove OSD
- [] Remove MON
- [] Delete pool

### Phase Four
- [] Collectd integration
- [] Graphite integration

### Phase Five
- [] Auth system
- [] User session tracking

### Phase Six
- [] Multi-cluster support
