
from pony.orm import db_session, commit

from .models import (
    Client, Ram, Swap, Cpu, SingleCPU, Disk
)


class MainOperation:
    def __init__(self, all_data):
        self.cpu = all_data.get('main')
        self.all_cpu = all_data.get('all')
        self.ram = all_data.get('ram')
        self.swap = all_data.get('swap')
        self.disk = all_data.get('disk')
        self.network = all_data.get('ip')
        self.client = None

    @db_session
    def main(self):
        cpu = self.register_cpu()
        all_cpu = self.register_all_cpu()
        ram = self.register_ram()
        swap = self.register_swap()
        disk = self.register_disk()
        self.client = self.register_or_get_network(
            cpu, all_cpu, ram, swap, disk
        )

        # self.client.ram = ram
        # self.client.swap = swap
        # self.client.cpu = cpu
        # self.client.single_cpu = all_cpu
        # self.client.disk = disk

        commit()

    def register_or_get_network(self, cpu, all_cpu, ram, swap, disk):
        hostname = str(self.network['hostname'])
        ip = str(self.network['ip'])
        client = Client.get(name=hostname)

        if client is None:
            print('Not exists')
            client = Client(name=hostname, ip=ip)

        client.cpu = [c_cpu for c_cpu in client.cpu] + [cpu]
        client.single_cpu = [s_cpu for s_cpu in client.single_cpu] + all_cpu
        client.ram = [c_ram for c_ram in client.ram] + [ram]
        client.swap = [c_swap for c_swap in client.swap] + [swap]
        client.disk = [c_disk for c_disk in client.disk] + [disk]

        commit()

        return client

    def register_cpu(self):
        percent_use = self.cpu['cpu']
        min_freq = self.cpu['frequency'].min
        max_freq = self.cpu['frequency'].max
        actual_freq = self.cpu['frequency'].current

        try:
            cpu = Cpu(
                percent_use=percent_use,
                min_freq=min_freq,
                max_freq=max_freq,
                actual_freq=actual_freq
            )
            commit()
        except Exception as e:
            cpu = None
            print(e)

        return cpu

    def register_all_cpu(self):
        all_cpu = []

        for i, value in enumerate(self.all_cpu['cpu']):
            freqs = self.all_cpu['frequencies'][i]
            percent_use = value
            min_freq = freqs.min
            max_freq = freqs.max
            actual_freq = freqs.current
            try:
                sc = SingleCPU(
                    client = self.client,
                    percent_use=percent_use,
                    min_freq=min_freq,
                    max_freq=max_freq,
                    actual_freq=actual_freq,
                    num_cpu=i
                )
                commit()
                all_cpu.append(sc)
            except Exception as e:
                print(e)

        return all_cpu

    def register_ram(self):
        total = self.ram['total']
        used = self.ram['used']
        free = self.ram['available']
        unit = self.ram['units']

        try:
            ram = Ram(
                client = self.client,
                total=total,
                used=used,
                free=free,
                unit=unit
            )
            commit()
        except Exception as e:
            ram = None
            print(e)

        return ram

    def register_swap(self):
        total = self.swap['total']
        used = self.swap['used']
        free = self.swap['available']
        unit = self.swap['units']

        try:
            swap = Swap(
                client = self.client,
                total=total,
                used=used,
                free=free,
                unit=unit
            )
            commit()
        except Exception as e:
            swap = None
            print(e)

        return swap

    def register_disk(self):
        total = self.disk['total']
        used = self.disk['used']
        free = self.disk['free']
        unit = self.disk['units']

        try:
            disk = Disk(
                client = self.client,
                total=total,
                used=used,
                free=free,
                unit=unit
            )
            commit()
        except Exception as e:
            disk = None
            print(e)

        return disk
