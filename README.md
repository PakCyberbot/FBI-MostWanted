# FBI-MostWanted Python tool
An open-source tool that gets information on the FBI Wanted program, this includes lists of wanted criminals, unidentified victims, etc. 

This tool is an enhanced version of the previous one written by @rly0nheart. Thanks to him for making my work more easier by creating fbi-api handling python library.

# Installation
```
$ git clone https://github.com/PakCyberbot/FBI-MostWanted.git
```

```
$ cd FBI-MostWanted
```

```
$ pip install -r requirements.txt
```

# Optional Arguments
| Option       | Metavar | Usage |
| -------------|:---------:|:---------:|
| <code>--dump</code>| *path/to/file* |  *dump output to a specified file*  |
| <code>--wanted</code>| |  *return dossiers of the current wanted persons*  |
| <code>--records</code>| *number* |  *number of records to fetch with --wanted, DEFAULT=10*  |
| <code>--wanted-person</code>| *ID#* |  *return a dossier of a wanted person*  |
| <code>--images</code>| |  *download images seperately in a folder. FileName Format: ***name+number+caption****  |
| <code>--download</code>| |  *download a person's casefile (beta) (only works with --wanted-person)*  |
| <code>--verbose</code>| | *enable verbosity*  |
| <code>--version</code>| |  *show program's version number and exit*  |
| <code>--author</code>| |  *show author's information and exit*  |
| <code>--licence/--license</code>| |  *show program's licen[cs]e and exit*  |

# Improvements
I am currently working on new features. Implemented to download multiple pdf of many person. WILL UPDATE THIS PART SOON

# LICENSE
![license](https://user-images.githubusercontent.com/74001397/137917929-2f2cdb0c-4d1d-4e4b-9f0d-e01589e027b5.png)


# Credits
Thanks for the @rly0nheart <a href="https://pypi.org/project/fbi-api/">fbi-api</a> python library and the tool. 
* [About rly0nheart](https://about.me/rly0nheart)
* [rly0nheart GitHub](https://github.com/rly0nheart)
* [rly0nheart Twitter](https://twitter.com/rly0nheart)
