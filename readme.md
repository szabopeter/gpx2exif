# gpx2exif
A tool to add geographic exif info to jpg images based on a gpx file.

## Usage
1. set `gpstoolpath` variable in `scan-exif.py` to ExifTool path.
2. `setdif.py jpegtime gpstime`  
    Note: `jpegtime` and `gpstime` are times in this format: `hh:mm:ss`.
3. `scan-exif.py gpxfile.gpx jpeg1.jpg jpeg2.jpg ... jpegn.jpg > script.cmd`
4. `. script.cmd`

## Notes
* This project was converted from Python2 to Python3