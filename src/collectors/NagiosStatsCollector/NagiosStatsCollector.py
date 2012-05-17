import diamond.collector
import subprocess
import os

class NagiosStatsCollector(diamond.collector.Collector):
    """
    Shells out to get nagios statistics, which may or may not require sudo access
    """

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            'nagiosstats_cmd': '/usr/sbin/nagios3stats',
            'vars':            ['AVGACTHSTLAT',
                                'AVGACTSVCLAT',
                                'AVGACTHSTEXT',
                                'AVGACTSVCEXT',
                                'NUMHSTUP',
                                'NUMHSTDOWN',
                                'NUMHSTUNR',
                                'NUMSVCOK',
                                'NUMSVCWARN',
                                'NUMSVCUNKN',
                                'NUMSVCCRIT',
                                'NUMHSTACTCHK5M',
                                'NUMHSTPSVCHK5M',
                                'NUMSVCACTCHK5M',
                                'NUMSVCPSVCHK5M',
                                'NUMACTHSTCHECKS5M',
                                'NUMOACTHSTCHECKS5M',
                                'NUMCACHEDHSTCHECKS5M',
                                'NUMSACTHSTCHECKS5M',
                                'NUMPARHSTCHECKS5M',
                                'NUMSERHSTCHECKS5M',
                                'NUMPSVHSTCHECKS5M',
                                'NUMACTSVCCHECKS5M',
                                'NUMOACTSVCCHECKS5M',
                                'NUMCACHEDSVCCHECKS5M',
                                'NUMSACTSVCCHECKS5M',
                                'NUMPSVSVCCHECKS5M'],
            'use_sudo':         True,
            'sudo_cmd':         '/usr/bin/sudo',
            'path':             'nagiosstats'
        }

    def collect(self):
        if not os.access(self.config['nagiosstats_cmd'], os.X_OK) or (self.config['use_sudo'] and not os.access(self.config['sudo_cmd'], os.X_OK)):
            return
 
        command = [self.config['nagiosstats_cmd'], '--data', ",".join(self.config['vars']), '--mrtg']

        if self.config['use_sudo']:
            command.insert(0, self.config['sudo_cmd'])

        p = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0][:-1]

        for i, v in enumerate(p.split("\n")):
            metric_name = self.config['vars'][i]
            metric_value = int(v)
            self.publish(metric_name, metric_value)
