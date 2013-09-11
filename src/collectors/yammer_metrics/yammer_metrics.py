# coding=utf-8

"""
Collect [Yammer Metrics](http://metrics.codahale.com/) JSON output for the local node

#### Dependencies

 * urlib2

"""

import urllib2

try:
    import json
    json  # workaround for pyflakes issue #13
except ImportError:
    import simplejson as json

import diamond.collector


class MetricsCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(MetricsCollector,
                            self).get_default_config_help()
        config_help.update({
            'url':  ""
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(MetricsCollector, self).get_default_config()
        config.update({
            'url': "http://127.0.0.1:8081/metrics",
            'path': 'metrics'
        })
        return config

    def flatten(self, structure, key="", path="", flattened=None):
        if flattened is None:
            flattened = {}
        if not isinstance(structure, (dict, list)):
            flattened[((path + ".") if path else "") + key] = structure
        elif isinstance(structure, list):
            for i, item in enumerate(structure):
                self.flatten(item, "%d" % i, ".".join(filter(None,[path,key])), flattened)
        elif isinstance(structure, dict):
            for new_key, value in structure.items():
                self.flatten(value, new_key, ".".join(filter(None,[path,key])), flattened)
        return flattened

    def select_number_values(self, payload):
        published = {}
        for key, value in payload.items():
            if isinstance(value, (int, float, long)):
                published[key] = value
        return published

    def collect(self):
        if json is None:
            self.log.error('Unable to import json')
            return {}
        url = self.config['url']
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError, err:
            self.log.error("%s: %s", url, err)
            return

        try:
            result = json.load(response)
        except (TypeError, ValueError):
            self.log.error("Unable to parse response from Metrics page as a"
                           + " json object")
            return

        flattened = self.flatten(result)
        metrics = self.select_number_values(flattened)

        for key in metrics:
            self.publish(key, metrics[key])
