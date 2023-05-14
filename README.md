# FBI-MostWanted Python tool
An open-source tool that gets information on the FBI Wanted program, this includes lists of wanted criminals, unidentified victims, etc. 

This tool is an enhanced version of the previous one written by @rly0nheart. Thanks to him for making my work more easier by creating fbi-api handling python library.

 Please check the **"Improvements"** section below to learn about the new features.

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
| <code>--dump</code>| *path/to/file <txt/pdf>* |  *dump output to a specified file, behaves differently for pdf*  |
| <code>--wanted</code>| |  *return dossiers of the current wanted persons*  |
| <code>--records</code>| *number* |  *number of records to fetch with --wanted, DEFAULT=10*  |
| <code>--wanted-person</code>| *ID#* |  *return a dossier of a wanted person*  |
| <code>--images</code>| |  *download images seperately in a folder. FileName Format: ***name+number+caption****  |
| <code>--download</code>| |  *download a person's casefile (beta) (only works with --wanted-person)*  |
| <code>--reward</code>| | *Filter out records that contain a reward*  |
| <code>--verbose</code>| | *enable verbosity*  |
| <code>--version</code>| |  *show program's version number and exit*  |
| <code>--author</code>| |  *show author's information and exit*  |
| <code>--licence/--license</code>| |  *show program's licen[cs]e and exit*  |

# Improvements
* You now have the capability to **download PDF files for each entry/record** on the wanted list, whereas before, you were limited to downloading a single PDF file for an individual person.
* If you provide a **dump file with a PDF extension, the tool will automatically enter download mode and proceed to download the PDF files** of all wanted individuals. The downloaded files will be saved in the directory with the same name as the provided dump file.
* You can now fetch any **desired number of records from the wanted list using the "--records" option**.
* Additionally, you have the capability to **download each image file separately using --images**. The downloaded image files will be stored in the "wanted-images" directory for OSINT purposes.
* By including the "--reward" option, **you can easily filter out records that include a reward**. If you specify the "--records" parameter along with it, be aware that the filter will be applied to the available entries, potentially resulting in a count lower than the specified "--records" value.

# LICENSE
![license](https://user-images.githubusercontent.com/74001397/137917929-2f2cdb0c-4d1d-4e4b-9f0d-e01589e027b5.png)


# Credits
Thanks for the @rly0nheart <a href="https://pypi.org/project/fbi-api/">fbi-api</a> python library and the tool. 
* [About rly0nheart](https://about.me/rly0nheart)
* [rly0nheart GitHub](https://github.com/rly0nheart)
* [rly0nheart Twitter](https://twitter.com/rly0nheart)

# Contributer 
You can follow him and me to get more updates about cybersec, development and many more 
* [PakCyberbot GitHub](https://github.com/PakCyberbot)
* [PakCyberbot Twitter](https://twitter.com/Pakcyberbot)


