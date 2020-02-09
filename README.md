# MUR
Tool written in python to download booklets from Marvel Unlimited.   
[Windows binaries](https://github.com/Sorrow446/MUR/releases)
 
**People have been seen selling my tools; DO NOT buy them. My tools are free and always will be.**

# Setup
**A subscripton is required to use this tool.**  
1. Login to [Marvel](http://www.marvel.com/).
2. Install ["cookies.txt" Chrome extension](https://chrome.google.com/webstore/detail/cookiestxt/njabckikapfpffapmjgojcnbfjonfjfg).
3. Dump cookies to txt file (current tab only).
4. Move "cookies.txt" to MUR's directory.

Your cookies may become unusable after a long while; just repeat the dumping process.

# Usage
MUR may only be used via CLI.

Download a single booklet and convert to PDF:   
`MUR.py -u https://www.marvel.com/comics/issue/67930/captain_america_2018_12 -f pdf`

Download multiple booklets, convert to CBZ and write booklet metadata to JSON file:   
`MUR.py -u https://www.marvel.com/comics/issue/... https://www.marvel.com/comics/issue/... -f cbz -m`
```
usage: mur.py [-h] -u [URL [URL ...]] -f {cbz,pdf} [-m]

Sorrow446.

optional arguments:
  -h, --help            show this help message and exit
  -u [URL [URL ...]], --url [URL [URL ...]]
                        URL - www.marvel.com/comics/issue/ or
                        read.marvel.com/#/book/.
  -f {cbz,pdf}, --format {cbz,pdf}
                        Export format.
  -m, --meta            Write comic's metadata to JSON file.
```
Accepted URL formats:
```
1. https://www.marvel.com/comics/issue/<id>/...
2. https://read.marvel.com/#/book/<id>
```

# Disclaimer
- I will not be responsible for how you use MUR.
- MARVEL brand and name is the registered trademark of its respective owner.   
- MUR has no partnership, sponsorship or endorsement with MARVEL.
