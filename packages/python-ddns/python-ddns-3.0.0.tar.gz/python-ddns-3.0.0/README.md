# Python-DDNS

[![GitHub license](https://img.shields.io/github/license/Cyb3r-Jak3/python-ddns?style=flat-square)](https://github.com/Cyb3r-Jak3/python-ddns/blob/master/LICENSE.md) 


[![PyPI](https://img.shields.io/pypi/v/Python-DDNS?style=flat-square)](https://pypi.org/project/Python-DDNS/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-ddns?style=flat-square)  

[![Gitlab pipeline status (branch)](https://img.shields.io/gitlab/pipeline/Cyb3r-Jak3/python-ddns/master?style=flat-square)](https://gitlab.com/Cyb3r-Jak3/python-ddns/pipelines)
[![Maintainability](https://api.codeclimate.com/v1/badges/fc98f6f42dc23a78ab22/maintainability)](https://codeclimate.com/github/Cyb3r-Jak3/python-ddns/maintainability)

This is program written in python that acts as a DDNS client for various providers. Supports IPv4 and IPv6.
Tested and supported on the following Python versions:

- 3.6
- 3.7
- 3.8
- 3.9
- 3.10-rc

## Provider List

- [X] Cloudflare
- [X] Hurricane Electric
- [X] Strato - @Braumeister
- [X] Afraid.org - @Braumeister
- [ ] DBSimple
- [ ] NameCheap

## Python Install

The recommended way is to use pip to install it.  
There is a package available on [pypi](https://pypi.org/project/Python-DDNS/).

```bash
pip install python-ddns
# Setups the config file to the right name
pddns -i

# Modify config.conf with the require fields.

# To check configuration
pddns -t

# Recommended to test to make sure everything works
pddns

# Edit crontab to run script
crontab -e
# Add
0 * * * * <path/to/pddns> >/dev/null 2>&1 #Updates every hour.
```

## Source Install

Source install if you would rather install it that way.

```bash
git clone https://gitlab.com/Cyb3r-Jak3/python-ddns
cd python-ddns/
python setup.py install

# Setups the config file to the right name
pddns -i

# Modify config.conf with the require fields.

# To check configuration
pddns -t

# Recommended to test to make sure everything works
pddns

# Edit crontab to run script
crontab -e
# Add
0 * * * * <path/to/pddns> >/dev/null 2>&1 # Updates every hour.
```

### TODO

- Easier config editing
- Better service functionality
- Other DNS systems supported