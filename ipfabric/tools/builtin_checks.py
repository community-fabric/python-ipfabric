from typing import Any

from pydantic.dataclasses import dataclass


def sites_names(ipf):
    sites = [site['siteName'] for site in ipf.inventory.sites.all(columns=['siteName'])]
    sites.append('$main')
    return sites


@dataclass
class NonRedundantLinks:
    ipf: Any

    @staticmethod
    def _get_int_names(labels):
        source_int = None
        for label in labels['source']:
            if label['type'] == "intName":
                source_int = label['text']
                break
        target_int = None
        for label in labels['target']:
            if label['type'] == "intName":
                target_int = label['text']
                break
        return source_int, target_int

    def list(self):
        sites = sites_names(self.ipf)
        data = self.ipf.graphs.site(sites, overlay={"type": "intent", "intentRuleId": "nonRedundantEdges"})
        nodes = {node['id']: node['label'] for node in data['graphResult']['graphData']['nodes'].values()}
        links = list()
        for link in data['graphResult']['graphData']['edges'].values():
            if link['intentCheckResult']:
                source_int, target_int = self._get_int_names(link['labels'])
                source = nodes[link['source']] if link['source'] in nodes else link['source']
                target = nodes[link['target']] if link['target'] in nodes else link['target']
                links.append(dict(source=source, source_int=source_int, target=target, target_int=target_int))
        return links


@dataclass
class SinglePointsFailure:
    ipf: Any

    def list(self):
        sites = sites_names(self.ipf)
        data = self.ipf.graphs.site(sites, overlay={"type": "intent", "intentRuleId": "singlePointsOfFailure"})
        nodes = list()
        for node in data['graphResult']['graphData']['nodes'].values():
            if 'intentCheckResult' in node and node['intentCheckResult']:
                nodes.append(dict(device=node['label'], type=node['type']))
        return nodes
