# Tracert utility on Python

Tracert (traceroute) is a utility that allows you to trace the route of data to a remote destination in TCP/IP networks. With
these commands, you can see the path of the data packet from your computer to the target server or site.

This is the reference implementation of tracert for Linux.

## Requirement

- Python 3.8 or later

## Usage

To run utility from repository root use

```
sudo python3 tracert.py [destination_name_or_address]
```

## Example

```
sudo python3 tracert.py lanit-tercom.ru
```

or equivalent

```
sudo python3 tracert.py 178.210.90.17
```

for example destination returned

```
Try to trace route to lanit-tercom.ru (178.210.90.17) with max route length 30:
1       _gateway (192.168.100.1)
2       192.168.1.1
3       asr1-40.kmv.ru (217.13.214.35)
4       br4v707-bdr68.kmv.ru (217.13.213.10)
5       178.35.225.117
6       109.172.24.43
7       5.143.251.250
8       dp-r1.nic.ru (31.177.68.243)
9       dp-gw1.nic.ru (31.177.67.73)
10      uweb1119.sys.nichost.ru (31.177.95.134)
11      l-t.nichost.ru (178.210.90.17)
```
