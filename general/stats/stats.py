
import logging
import pprint
import os
import socket

import coloredlogs
import psutil as pc
import pytz


logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')
local_tz = pytz.timezone('America/Mexico_City')


class Stats:
    def __init__(self, interval=1, units='GB'):
        """
        :interval(float): interval of get status
        """
        self.interval = interval
        self.units = units
        self.divisor_unit = self.divisor(units)

    def main(self):
        stats = {}
        pp = pprint.PrettyPrinter(indent=4)
        stats['main'] = self.main_processor()
        stats['all'] = self.all_processors()
        stats['ram'] = self.random_access_memory()
        stats['swap'] = self.swap()
        stats['disk'] = self.read_only_memory()
        stats['ip'] = self.get_ip()

        return stats

    def main_processor(self):
        main = pc.cpu_percent(self.interval)
        freqs = pc.cpu_freq()

        return {
            'cpu': main,
            'frequency': freqs
        }

    def all_processors(self):
        all_ = pc.cpu_percent(self.interval, percpu=True)
        freqs = pc.cpu_freq(True)

        return {
            'cpu': all_,
            'frequencies': freqs
        }

    def divisor(self, units):
        divisor = None
        if self.units == 'B':
            divisor = 1
        if self.units == 'KB':
            divisor = 1024
        elif self.units == 'MB':
            divisor = 1024 ** 2
        elif self.units == 'GB':
            divisor = 1024 ** 3
        else:
            raise Exception('units does not valid')

        return divisor

    def random_access_memory(self):
        ram = pc.virtual_memory()

        return {
            'total': ram.total / self.divisor_unit,
            'available': ram.available / self.divisor_unit,
            'used': (ram.total - ram.available) / self.divisor_unit,
            'units': self.units
        }

    def swap(self):
        swap = pc.swap_memory()

        return {
            'total': swap.total / self.divisor_unit,
            'available': swap.used / self.divisor_unit,
            'used': (swap.total - swap.used) / self.divisor_unit,
            'units': self.units
        }

    def read_only_memory(self):
        disk = pc.disk_usage('/')

        return {
            'total': disk.total / self.divisor_unit,
            'used': disk.used / self.divisor_unit,
            'free': disk.free / self.divisor_unit,
            'units': self.units
        }

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()

        return {
            'ip': ip,
            'hostname': socket.gethostname()
        }


if __name__ == '__main__':
    stats = Stats()
    stats.main()
