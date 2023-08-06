Torjailctl
=======

[![pyversions](https://img.shields.io/badge/python-3.3%2B-blue.svg)](https://pypi.org/project/torjailctl/)

Torjailctl is a tool to integrate [Firejail + Tor](https://firejail.wordpress.com/)
sandboxing in the Linux desktop. Enable Torjailctl for an application and enjoy a
more private and more secure desktop.

Those are the real coders behind this code, i've only made some brainless tweaks:
=======

https://github.com/orjail/orjail

&

https://github.com/rahiel/firectl


# Usage

To see which applications you can enable:
``` bash
torjailctl status
```

To enable tor + firejail for all program:
``` bash
sudo torjailctl enable firefox --all --tor
```

To enable tor + firejail torjailctl for a program:
``` bash
sudo torjailctl enable firefox --tor
```

To enable firejail for a program:
``` bash
sudo torjailctl enable firefox
```

To disable firejail for a program:
``` bash
sudo torjailctl disable firefox
```

## Install

Install torjailctl with pip:
``` bash
sudo pip3 install torjailctl
```

## Uninstall

To uninstall torjailctl:
``` bash
sudo torjailctl disable --all
sudo pip3 uninstall torjailctl
sudo rm /etc/firejail/firejail.config
```
