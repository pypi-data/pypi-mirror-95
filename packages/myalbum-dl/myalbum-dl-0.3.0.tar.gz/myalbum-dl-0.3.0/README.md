# myalbum-dl
![Package Version](https://img.shields.io/pypi/v/myalbum-dl?style=flat-square) ![Python Version](https://img.shields.io/pypi/pyversions/myalbum-dl?style=flat-square)

A command-line tool written in Python for downloading albums from MyAlbum

<img src="https://raw.githubusercontent.com/GBS3/myalbum-dl/main/media/terminal.gif">

## Installation
In order to install the tool, run the following in your terminal:

```sh
$ pip install myalbum-dl
```

## Usage
Once `myalbum-dl` is installed, all you need to do is run the following in your terminal to use it:

```sh
$ myalbum-dl <URL>
```

For example:

```sh
$ myalbum-dl https://myalbum.com/album/uRCYu2bHECn7
```

### Arguments
Here's a list of available arguments you can pass at the command line:
```
positional arguments:
    album                           URL of the album to scrape
    
optional arguments:
    -h, --help                      show this help message and exit
    --debug                         option to enable debugging
    -s, --separate                  separate media types into their own directories
```

For example, if you want files to be separated by media type into their own directories, you can pass the `separate` argument like so:

```sh
$ myalbum-dl https://myalbum.com/album/uRCYu2bHECn7 -s
```

or

```sh
$ myalbum-dl https://myalbum.com/album/uRCYu2bHECn7 --separate
```