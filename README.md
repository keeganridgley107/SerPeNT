
# SerPeNT

###### The Simple Python Network Toolkit

Serpent is a simple cross platform :snake: based interactive network toolkit.

its essentially a few smaller tools wrapped up in a interactive cli that uses argparse to deal with params

#### Features Include:

- IP/Port Scanner
- Vulnerability Scanner
- Packet Sniffer - might not work on some machines
- Web Scraper
- Static File Server

---

## Install

to install Serpent open a terminal and run the following command:

``` 
git clone https://github.com/keeganridgley107/serpent.git 
cd serpent
python3 -m venv serpent_venv
source serpent_venv/bin/activate
pip3 install -r requirements.txt
```

## Usage

To use serpent the following command in a terminal:

```python serpent.py```
 
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

## Serpent Tools 

All of the tools in Serpent can be accessed individually. 
This allows advanced users to use features not yet included in serpent.py 

----

### Scanner

```
usage: scanner.py [-h] address [-p] [port-port,port,+] [-n] [-c] [-u]

Simple Python Port Scanner

positional arguments:
  address               Target Address : 8.8.8.8 or google.com

optional arguments:
  -h, --help            show this help message and exit
  -p PORTS, --ports PORTS
                        Ports to scan : 20-25,80
  -n, --network         Scan network : X.X.X.1-254
  -c, --connect         Connect to discovered hosts
  -u, --udp             include UDP scan

```

#### Scanner Examples

###### Scan localhost for http web server 

```python scanner.py localhost -p 80```

###### Scan localhost for ftp service and connect if found

```python ipTools.py localhost -c -p20```

-----------

### Static file server 

```
usage: dir_serve.py 

Simple LAN file server 

Notes: serves any files in Dektop/html over LAN at localhost:8000

```

#### Static File Server Example:

###### Create html folder and serve hello_world.txt over LAN 

```
cd ~/Desktop && mkdir html
cd html && echo "HELLO WORLD!" > hello_world.txt
cd ../serpent/ip_tools && python dir_serve.py
```

-----------

### Web Scraper 

```
usage: web_crawl.py 

Simple Python Web Scraper  

Notes: Creates a CSV file, or adds a new line for every link found on a webpage

```

-----------

## Notes

- Serpent is a work in progress. 
- use at your own risk 
- only use on networks own. 

