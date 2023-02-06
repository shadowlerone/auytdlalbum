# auytdlalbum
Automatically applies custom tags to mp3 files inside a folder. To be used with YT-dlp downloads. Python 3 is required.

Usage: Usage: autoytdlalbum.py {outputfoldername} {querymetadata} {coverartfilepath}

For querymetadata, follow the format: "[tagname] = [value] | [othertagname] = [value] | [othertagname] = [value]"

tagnames to use:

artist: "art"
album artist: "albart"
disc number: "dis"
year of release: "year"
genre: "gen"

If there are unspecified tags, default values will be set if the tag in the file is empty.

The file is to be placed in the directory where mp3 files are located. Note mp3 files inside other folders in the directory will be copied on on the output directory and have their tags set.

The program is designed to work with mp3 files downloaded using yt-dlp. Other mp3 files may work however, but do note the name of the file will be pasted over to the title tag.
