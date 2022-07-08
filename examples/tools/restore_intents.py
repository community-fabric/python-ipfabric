import json
from collections import OrderedDict

from ipfabric import IPFClient
from ipfabric.tools import RestoreIntents

if __name__ == "__main__":
    ipf = IPFClient()
    ri = RestoreIntents(ipf)

    # ri.restore_from_file(intents_file='intents.json', groups_file='groups.json', dashboard_file='dashboard.json')

    intents = ipf.get('reports').json()
    groups = ipf.get('reports/groups').json()
    dashboard = json.loads(ipf.get('settings/dashboard').text, object_pairs_hook=OrderedDict)
    ri.restore_from_dictionary(intents, groups, dashboard)

    # ri.restore_default(version='v4.4')
