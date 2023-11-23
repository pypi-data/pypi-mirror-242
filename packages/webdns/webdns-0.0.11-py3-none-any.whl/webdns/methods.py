import ipaddress
import os

from pynetbox import api


def create_cf(cfpath, nburl, nbtoken, nbpfparams):
    '''Create DNS masq config files from Netbox prefixes

    Parameters
    ----------
    cfpath : str
        Dir path of DNS Masq config files,
    nburl : str
        Netbox URL,
    nbtoken : str
        Netbox API Token,
    tenant : str
        Tenant of Netbox ip addresses
    nbpfparams : dict
        Netbox prefix filter params,

    Raises
    ------
    None

    Returns
    -------
    None
    '''
    # Start nb connection
    nb = api(url=nburl, token=nbtoken)

    # Get nb prefixes based on config params
    prefixes = nb.ipam.prefixes.filter(
        role=nbpfparams['role'],
        site=nbpfparams['site'],
        status=nbpfparams['status'],
        vlan=nbpfparams['vlan'],
    )

    # Iterate over child prefixes (cp), creating config files
    for cp in prefixes:
        # Get tenant and open config file
        tenant = cp.tenant.slug
        cfile = open(f'{cfpath}{tenant}.conf', 'w')

        # Get ip address from ip prefix and get CIDR
        net = ipaddress.IPv4Network(cp)

        ips_cidr = [f'{str(host)}/{str(net.prefixlen)}' for host in net.hosts()]
        for ip in ips_cidr:
            # Check whether ip addr has DNS name
            ip_obj = nb.ipam.ip_addresses.get(address=str(ip))
            if ip_obj is not None:
                dns_name = ip_obj.dns_name

                # Pop subnet mask from ip addr and write on file
                str_ip, _ = ip.split('/')
                cfile.write(f'address=/{dns_name}/{str_ip}\n')

        # Save file and close
        cfile.close()
    return
   
   
def update_cf(nburl, nbtoken, cfpath, tenant=None, ipaddresses=[]):
    '''Update DNS masq entries based on IP address from Netbox

    Parameters
    ----------
    nburl : str
        Netbox URL,
    nbtoken : str
        Netbox API Token,
    cfpath : str
        Dir path of DNS Masq config files,
    tenant : str
        Tenant of Netbox ip addresses
    ipadresses : list
        List of strings of IP addresses to be updated based on Netbox entries,

    Raises
    ------
    None

    Returns
    -------
    None
    '''
    # Check whether config file exists
    # TO-DO raise errors and deal with it
    filename = f'{cfpath}/{tenant}.conf'
    if not os.path.isfile(filename):
        print("Config file {} does not exist.".format(filename))
        exit(1)

    # Start nb connection
    nb = api(url=nburl, token=nbtoken)
 
    # Get nb ip addresses from Netbox
    ipaddrs = []
    for addr in ipaddresses:
        ipaddrs.append(
            nb.ipam.ip_addresses.get(
                address=addr,
            )
        )

    # Read the entire content of the configuration file
    with open(filename, "r") as f:
        lines = f.readlines()

    # Update IP addresses DNS masq entries based on dns_name from Netbox
    new_lines = []

    # Adds a maximum of two lines
    for ipaddr in ipaddrs:
        line_found = False
        for i, line in enumerate(lines):
            if ipaddr.dns_name in line:
                # If the DNS is the same but the IP is different, update the IP
                if ipaddr.address not in line:
                    new_line = f'address=/{ipaddr.dns_name}/{ipaddr.address.split("/")[0]}\n'
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
                line_found = True
                break

        # If the line is not found, add the new line
        if not line_found:
            new_line = f'address=/{ipaddr.dns_name}/{ipaddr.address.split("/")[0]}\n'
            new_lines.append(new_line)

    # Write the updated content back to the configuration file
    with open(filename, "w") as f:
        f.writelines(new_lines)

    return