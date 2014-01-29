# Copyright (c) 2013,2014 Donald Talton
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:

# Redistributions of source code must retain the above copyright notice, this
#  list of conditions and the following disclaimer.

# Redistributions in binary form must reproduce the above copyright notice, this
#  list of conditions and the following disclaimer in the documentation and/or
#  other materials provided with the distribution.

# Neither the name of Donald Talton nor the names of its
#  contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.conf import settings
from django.core.files.temp import NamedTemporaryFile
from cephclient import wrapper

import requests
import re
import math
import json
import subprocess

URLS = settings.CEPH_URLS
get_data = wrapper.CephWrapper(endpoint = settings.CEPH_BASE_URL)

''' the main request builder '''
def req(url):
  headers = {'Accept': 'application/json' }
  timeout = 10
  r = requests.get(url, headers=headers, timeout=timeout)
  response_json = r.text
  return response_json

''' Cluster collection methods '''

def home(request):

  ''' overall cluster health '''

  cresp, cluster_health = get_data.get_health(body = 'json')
  sresp, cluster_status = get_data.get_status( body = 'json')

  ''' mons '''

  mons = cluster_status['output']['health']['health']['health_services'][0]
  total_mon_count = {key:len(value) for key,value in mons.iteritems()}['mons']
  mons_ok = 0
  mons_warn = 0
  mons_crit = 0

  for mon in mons['mons']:
    if mon['health'] == "HEALTH_OK":
      mons_ok = mons_ok + 1
    elif mon['health'] == "HEALTH_WARN":
      mons_warn = mons_warn + 1
    else:
      mons_crit = mons_crit + 1


  ''' get a rough estimate of cluster free space. is this accurate '''
  presp, pg_stat = get_data.pg_stat(body = 'json')
  gb_avail = cluster_status['output']['pgmap']['bytes_total'] / 1024 / 1024
  gb_used = cluster_status['output']['pgmap']['bytes_used'] / 1024 / 1024

  ''' pgs '''
  pg_statuses = cluster_status['output']['pgmap']

  pg_ok = 0
  pg_warn = 0
  pg_crit = 0

  ''' pg states '''
  pg_warn_status = re.compile("(creating|degraded|replay|splitting|scrubbing|peering|repair|recovering|backfill|wait-backfill|remapped)")
  pg_crit_status = re.compile("(down|inconsistent|incomplete|stale)")

  for state in pg_statuses['pgs_by_state']:

    if state['state_name'] == "active+clean":
      pg_ok = pg_ok + state['count']

    elif pg_warn_status.search(state['state_name']):
      pg_warn = pg_warn + state['count']

    elif pg_crit_status.search(state['state_name']):
      pg_crit = pg_crit + state['count']



  ''' osds '''
  dresp, osd_dump = get_data.osd_dump(body = 'json')
  osd_state = osd_dump['output']['osds']

  osds_ok = 0
  osds_warn = 0
  osds_crit = 0

  for osd in osd_state:
    if osd['state'][0] == "exists" and osd['state'][1] == "up":
      osds_ok = osds_ok + 1
    elif osd['state'][0] == "exists" and osd['state'][1] == "down":
      osds_warn = osds_warn + 1
    else:
      osds_crit = osds_crit + 1

  return render_to_response('home.html', locals())

def ops(request):
  return render_to_response('ops.html', locals())


def osd_details(request, osd_num):
  osd_num = int(osd_num)
  osd_details = json.loads(req(URLS['osd_details']))
  osd_disk_details = osd_details['output']['osds'][osd_num]
  osd_perf = json.loads(req(URLS['osd_perf']))
  osd_disk_perf = osd_perf['output']['osd_perf_infos'][osd_num]
  return render_to_response('osd_details.html', locals())
