FileMonkey
==========

Monkey to randomly perform file system actions.

#Usage#
```shell
python monkey.py
```

#Features#
```shell
usage: monkey.py [-h] [-i INPUT] [-s SPEED] [-v VERBOSITY] [-r REBUILD]
                 [-f FILESPERDIR] [-w] [--nocreate] [--noreplace] [--norename]
                 [--noappend] [--noremove]

optional arguments:
  -h, --help            show this help message and exit
  -i, --input           Folder to monkey
  -s, --speed           Set time between each monkey action
  -v, --verbosity       Show erros and other stuff
  -r, --rebuild         Number of errors before rebuild file index
  -f, --filesperdir     Number of files to create in each folder
  -w, --wipe            Wipe monkied folder before starting
  --nocreate            Don't create files
  --noreplace           Don't replace files
  --norename            Don't rename files
  --noappend            Don't append to files
  --noremove            Don't remove files
```
