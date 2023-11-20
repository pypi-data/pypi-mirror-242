![](https://img.shields.io/badge/python-3.9-blue) ![](https://img.shields.io/badge/python-3.10-blue) ![](https://img.shields.io/badge/python-3.11-blue) ![](https://img.shields.io/badge/python-3.12-blue)
# SDJ-REMOTETOOLS

## Description
`sdj-remotetools` is a python collection of tools working through SSH.

## Tools
All tools handle SSH connection using Paramiko.

### rcat
Works like 'cat' command but for remote files through SSH and with few enhancements
```
usage: rcat [-h] [-p] [-e ENCODING] [-b] [-s] remote_files [remote_files ...]

Works like 'cat' but through SSH.

positional arguments:
  remote_files          SSH path to the remote files, space separate, ie: joe@remote.host:/path/to/file

options:
  -h, --help            show this help message and exit
  -p, --password        Ask user for password
  -e ENCODING, --encoding ENCODING
                        Character encoding, ie: utf-8 (default)
  -b, --border          Draw border around the content
  -s, --syntax_highlight
                        Enable console syntax highlighting
```

### rlist
Works like 'ls' command but for remote path through SSH (with fewer options).
```
usage: rlist [-h] [-a] [-l] [-p] ssh_url

Works almost liks 'ls' but through SSH

positional arguments:
  ssh_url         SSH path to a remote file or directory, space separate, ie: joe@remote.host:/remote/path

options:
  -h, --help      show this help message and exit
  -a, --all       Show hidden and 'dot' files. Default: False
  -l, --long      Display extended file metadata as a table
  -p, --password  Ask user for password. Default: False
```
