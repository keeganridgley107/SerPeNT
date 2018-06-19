# ipTools

Homebrew is a Python based network auditing toolkit by Keegan Ridgley.
 
---

## Install

to install IpTools open a terminal and run the following commands:

``` 
git clone https://github.com/keeganridgley107/ipTools.git &&
cd ipTools
```



## Usage

```
usage: ipTools.py [-h] address [-n] [-p] [port,port-port,+]

Automated Wireless Network Utility

positional arguments:
  address               Target Address : 8.8.8.8 or google.com

optional arguments:
  -h, --help            show this help message and exit
  -p PORTS, --ports PORTS
                        Ports to scan : 22,23-80
  -n, --network         Scan network
  ```
  
### Examples:

---

###### Scan localhost for web server 

```python ipTools.py localhost -p 80```

###### Scan localhost for ftp, ssh and telnet services 

```python ipTools.py localhost -p 20-23```

---

### Notes:

- ipTools must be provided with an ip or domain name as an address

- The network flag will scan the entire host network

- Ports should be comma separated and can include ranges 

- IpTools is a hobby project still in development, check for future updates! 

