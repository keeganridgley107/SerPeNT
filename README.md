
# SerPeNT
###### The Simple Python Network Toolkit

Serpent is a simple cross platform :snake: based interactive network toolkit.
It allows users to perform several simple networking tasks without much thought.

#### Features Include:
    IP/Port Scanner
    Vulnerabilty Scanner
    Packet Sniffer
    Python RAT
    Web Scraper
    Static File Server

---

## Install

to install Serpent open a terminal and run the following command:

``` 
git clone https://github.com/keeganridgley107/ipTools.git &&
cd ipTools
```

## Usage

To use serpent in a terminal run 

```python3 serpent.py```
 
then select the tool you want to use from the options menu

```
##############################
########## Options ###########
##############################

        [1] Scanner
        [2] Servers
        [3] Sniffers
        [4] Scrapers
        [5] Exit

Select an option to continue...
>
```

---------

## Serpent Tools 

All of the tools in Serpent can be accessed individually. 
This allows advanced users to use features not yet included in serpent.py 

### Scanner

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

- Serpent is a work in progress. 
- use at your own risk 
- only use on networks own. 

