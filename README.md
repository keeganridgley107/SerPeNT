
# ipTools

ipTools is a :snake: based network auditing toolkit.

---

## Install

to install IpTools open a terminal and run the following command:

``` 
git clone https://github.com/keeganridgley107/ipTools.git &&
cd ipTools
```

## Usage

```
usage: ipTools.py [-h] address [-p] [port-port,port,+] [-n] [-c] [-u]

Simple Wireless Network Utility

positional arguments:
  address               Target Address : 8.8.8.8 or google.com

optional arguments:
  -h, --help            show this help message and exit
  -p PORTS, --ports PORTS
                        Ports to scan : 20-25,80
  -n, --network         Scan network : X.X.X.1-254
  -c, --connect         Connect to discovered hosts
  -u, --udp             include UDP scan

Created by K
```

### Examples:

###### Scan localhost for http web server 

```python ipTools.py localhost -p 80```

###### Scan localhost for ftp service and connect if found

```python ipTools.py localhost -c -p20```

### Notes:

- ipTools must be provided with an ip or domain name as an address
- Use ipTools only in ways consistent with local laws, you are responsible for consent prior to scanning!
- The network flag will scan the entire host network 
- Ports should be comma separated and can include ranges 
- IpTools is a hobby project still in development, check for future updates! 

