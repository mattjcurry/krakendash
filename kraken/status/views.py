from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.conf import settings
from django.core.files.temp import NamedTemporaryFile

import requests
import json
import subprocess

URLS = settings.CEPH_URLS

''' the main request builder '''
def req(url):
  headers = {'Accept': 'application/json' }
  timeout = 10
  r = requests.get(url, headers=headers, timeout=timeout)
  response_json = r.text
  return response_json

''' Cluster collection methods '''
def base_site(request):
  welcome = "Welcome to Kraken"
  return render_to_response('welcome.html', locals())

def cluster_fsid(request):
  fsid = req(URLS['fsid'])
  return render_to_response('fsid.html', locals())

def cluster_health(request):
  disk_free = json.loads(req(URLS['disk_free']))
  cluster_health = json.loads(req(URLS['cluster_health']))
  return render_to_response('cluster_health.html', locals())

def monitor_status(request):
  monitor_status = json.loads(req(URLS['monitor_status']))
  return render_to_response('monitor_status.html', locals())

def osd_list(request):
  osd_list = json.loads(req(URLS['osd_listids']))
  return render_to_response('osd_list.html', locals())

def osd_details(request, osd_num):
  osd_num = int(osd_num)
  osd_details = json.loads(req(URLS['osd_details']))
  osd_disk_details = osd_details['output']['osds'][osd_num]
  osd_perf = json.loads(req(URLS['osd_perf']))
  osd_disk_perf = osd_perf['output']['osd_perf_infos'][osd_num]
  return render_to_response('osd_details.html', locals())

def osd_map_summary(request):
  return HttpResponse(req(URLS['osd_map_summary']))

def osd_listids(request):
  return HttpResponse(req(URLS['osd_listids']))

def pools(request):
  osd_pools = json.loads(req(URLS['osd_pools']))
  return render_to_response('pools.html', locals())

def pool_detail(request, pool):
  pool = pool
  return render_to_response('pool_detail.html', locals())

def osd_tree(request):
  return HttpResponse(req(URLS['osd_tree']))

def pg_status(request):
  pg_status = json.loads(req(URLS['pg_status']))
  return render_to_response('pg_status.html', locals())

def pg_osd_map(request, pgid):
  pg_url = "http://localhost:5000/api/v0.1/pg/dump?dumpcontents=pgs_brief"
  pg_osd_map = json.loads(req(pg_url))
  return render_to_response('pg_osd_map.html', locals())

def crush_rules(request):
  crush_rules = json.loads(req(URLS['crush_rule_dump']))
  return render_to_response('crush_rules.html', locals())

def crushmap(request):
  r = requests.get('http://localhost:5000/api/v0.1/osd/getcrushmap')
  myfile = NamedTemporaryFile(delete=False)
  myfile.write(r.content)
  map = subprocess.call(['/usr/bin/crushtool -d', '%s']) % (myfile.name)
  return render_to_response('crushmap.html', locals())
