# playstv-saver
Python script to recover your clips from plays.tv using archive.org

# Currently there's a bug so the script does not fetch the correct video urls, working on fixing that.

## Requirements
+ Python 3.7 (made using 3.7.7)
+ `pip install -r requirements.txt` (you should probably use a virtual environment)
+ You need to find your plays.tv profile on https://web.archive.org/ for the script to do its work
  + The URL should look something like `https://web.archive.org/web/(some date and time)/https://plays.tv/u/(your username)`
+ Run with `python scraper.py <profile url>`. 
  + This will grab all the available clip pages and put them in a file called `out.txt`.
  + After that it will download all the clips to `video_out/`.
