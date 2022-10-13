"""
IP Calc : Return netmask, broadcast, hostMin, hostMax, prefix length of a subnet.
"""
from st2common.runners.base_action import Action

import ipaddress

class IpCalc(Action):

    def run(self,subnet):

        rc = True
        
        try:
            network = ipaddress.ip_network(subnet)
        except ValueError:
            rc = False
            return ( rc, "Error: Not a valid Subnet")

        netmask = str(network.netmask)
        broadcast = str(network.broadcast_address)
        prefix_length = int(network.prefixlen)
        host_min = str(list(network.hosts())[0])
        host_max = str(list(network.hosts())[-1])

        subnet_infos =  {
          "netmask": netmask,
          "broadcast": broadcast,
          "prefixlen": prefix_length,
          "hostmin": host_min,
          "hostmax": host_max
        }

        return (rc, subnet_infos)
