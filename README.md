# ipTools

Simple network and server auditing toolkit 
 
---

## Install

```git clone https://github.com/keeganridgley107/ipTools.git```

```cd ipTools```

## Usage

The toolkit comes with two flavors, Standard and Guided.

Standard ipTools can be provided with a ip or a domain as an address

The network flag will scan the entire host network


```
usage: ipTools.py [-h] address [-n] [-p] [port,port,+]

Automated Wireless Network Utility

positional arguments:
  address               Target Address : 8.8.8.8 or google.com

optional arguments:
  -h, --help            show this help message and exit
  -p PORTS, --ports PORTS
                        Ports to scan : 22,23,80
  -n, --network         Scan network
  ```




## Guided Mode

```python ipToolsHelper.py```

An interactive version of the ipTools utility with some extra features.

Including scan outcomes as reports in the ipTools/Reports folder

And interactive rule and dictionary file creation for faster auditing!

Guided mode is still being coded! 

## Credit

```keeganridgley.com```