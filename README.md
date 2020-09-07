# playstv-saver
Python script to recover your clips from plays.tv using archive.org

## Requirements
+ Python 3.7 (made using 3.7.7)
+ `pip install -r requirements.txt` (you should probably use a virtual environment)
+ You need to find your plays.tv profile on https://web.archive.org/ for the script to do its work
  + The URL should look something like `https://web.archive.org/web/(some date and time)/https://plays.tv/u/(your username)`
+ Run with `python scraper.py <profile url>`. 
  + This will grab all the available clip pages and put them in a file called `out.txt`.
+ Run it again, it will detect the file and download all the clips to `video_out/`.
  + I will update this soon so you only have to run it once :]
