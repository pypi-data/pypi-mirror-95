![Markdown Logo](https://i.pinimg.com/originals/98/df/87/98df87df9dd9694b31b5ccc522320850.png)
# YouTubeEased:
A YouTube API based library which will make your coding faster and better.
DISCLAIMER!
This library is vary basic and not very stabled, therefore you might get some errors.
## Install:
```pip install YouTubeEased```
## Library Needed:
```youtube_dl```
## How To Call The Library??
```python
# This way you call the __init__ function of the library!
from YouTubeEased import YouTubeEased
```

## Great What Now?
Now we need to actually call the function by typing:
```python
from YouTubeEased import YouTubeEased

# Here you type the URL!
youtube = YouTubeEased("URL")
```
If you don't want to use the regular way, you can also call the functions that are saved in the `Function` folder.
I don't recommend doing it because the library not stable yet.
```python
# All the functions can be taken by this way too!
from YouTubeEased.Functions.Downloader import DownloadURL
from YouTubeEased.Functions.GetInfo import GetInfoVideo
from YouTubeEased.Functions.URLChecker import YoutubeURLChecker, URLNotSupported
```

## Examples
```python
from YouTubeEased import YouTubeEased
from YouTubeEased.Functions.URLChecker import YoutubeURLChecker
from YouTubeEased.Functions.URLChecker import URLNotSupported


def download(url) -> None:
    # except URL errors
    try:
        youtube = YouTubeEased(url)
        print("URL Valid")
    except URLNotSupported:
        print("URL not supported!")
    #-----------------------------------#
    #                OR:                #
    #-----------------------------------#
    if YoutubeURLChecker(url).is_good_url():
        print("URL Valid")
    else:
        print("URL not supported!")

        
user = input("Type URL: ")
download(user)
```

```python
from YouTubeEased import YouTubeEased

user_url = input("Type URL: ")
user_fname = input("Type file name: ")
user_type_download = input("1. Video" 
                           "2. Audio"
                           "Type Here: ")

youtube = YouTubeEased(user_url)
youtube.file_name(user_fname)

if user_type_download == '1':
    youtube.download_video()
elif user_type_download == '2':
    youtube.download_audio()
else:
    print("Wrong input.")
```
## More Information:
This library was made for educational reasons and to make new coders feel more
comfortable around new libraries.