import requests
import os
import argparse


class Tracing:
    BASE_URL = 'http://ip-api.com/batch'

    def __init__(self, address):
        self.address = address
        self.address_sort_tracing = []

    def __get_tracer(self):
        address_tracing = os.popen(f'traceroute {self.address}', 'r')
        for line in address_tracing:
            try:
                self.address_sort_tracing.append(line[line.index('(') + 1:line.index(')')])
            except ValueError:  # в line нет ip адреса, поэтому функция index выдает ошибку
                # , а не быть адреса может в случае появления трех *
                break  # появились 3 *, поэтому цикл прекратился
        return self.address_sort_tracing

    def __get_ip_as(self):
        address_tracer = self.__get_tracer()
        response = requests.post(f"{self.BASE_URL}", json=[*address_tracer])
        dict_result = response.json()
        return dict_result

    def get_tracing(self):
        dict_result = self.__get_ip_as()
        print(f'# {" " * 2} ip {" " * 16} as {" " * 17} countryCode {" " * 3} provider')
        for i, elem in enumerate(dict_result):
            if elem["status"] == "fail":
                print(f'{i + 1}{(4 - len(str(i + 1))) * " "} {elem["query"]}')
            else:
                print(f'{i + 1}{(4 - len(str(i + 1))) * " "} {elem["query"]} {(16 - len(elem["query"])) * " "} '
                      f'{elem["as"]} {(25 - len(elem["as"])) * " "} {elem["countryCode"]} '
                      f'{(12 - len(elem["countryCode"])) * " "} {elem["isp"]}')


parser = argparse.ArgumentParser(description='Tracing autonomous system')
parser.add_argument('address', type=str, help='IP address or domain typing')
args = parser.parse_args()

tr = Tracing(args.address)
tr.get_tracing()
