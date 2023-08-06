# Hash Artifacts

This script computes the combined hash for one or more paths.
A path can contain glob patterns, and can be a directory or a file.
The script combines the path hashes deterministically, regardless the order of the paths.

## Usage
To view information about the usage of this script, use the `-h` command:

```shell
./hash-artifacts.py -h
```

A typical invocation of the script is as follows:

```shell
./hash-artifacts.py "path/to/file.extension"
```

The script takes the following information of the path(s) into account to compute the hash:

* The content of the file (if not a directory);
* The relative file path, from the current working directory.

The reason to relativize the paths is that the absolute path (in the case of Gitlab jobs) contains parts of project
 name. 
 This means the hash would change once you rename a Gitlab repository.

To explain path relativization in more detail, let's assume we have the following directory structure:

```
project
│   README.md
│   file001.txt
│
└───folder1
│   │   file011.txt
│   │   file012.txt
│   │
│   └───subfolder1
│       │   file111.txt
│       │   file112.txt
│       │   ...
│ 
└───folder2
    │   file021.txt
    │   file022.txt
```

If you call `hash-artifacts "**"` in `/project/folder1`, then:

* The current working directory is `/project/folder1`;
* The relative paths of the files to hash are: `file011.txt` and `file011.txt`.

If you call `hash-artifacts "/*."` in `/project/folder1`, then:

* The current working directory is `/project/folder1`;
* The relative paths of the files to hash are: `../README.md` and `../file001.txt`.

To prevent prematurely (shell) expansion of parameters that include glob patterns, you can surround parameters with
 double/single quotes. 

## Glob Patterns
The script makes use of Python's `glob` module to handle expansion of glob patterns in parameters.
See [documentation of the `glob` module](https://docs.python.org/3/library/glob.html) for more information on supported
patterns and usage.

As `recursive` is enabled, paths can also include `**` as a pattern.
It will match any files and zero or more directories, subdirectories and symbolic links to directories.
