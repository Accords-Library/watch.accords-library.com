# watch.accords-library.com

Provides to Accord's Library the tools to archive videos on multiple platforms, most notably YouTube using [yt-dlp](https://github.com/yt-dlp/yt-dlp)
It also downloads ffmpeg and ffprobe for audio-video post-processing.
The videos and other files (metadata, live chat, comments, sub files, thumbnails) are stored in `public` which needs to be accessible from the internet.  

## Setup
```bash
git clone https://github.com/Wayback-Tube/Wayback-Tube-DL.git
cd watch.accords-library.com
sh install.sh
```

## YouTube
Add the videos IDs or URLs to archive in `youtube/batchfile.txt`  
Use the extension `get Cookies.txt` on your Browser to retrieve credentials that yt-dlp can use to bypass age restrictions.
Possibly use a burner account.  
Then place that `cookies.txt` in the `youtube` folder
Then run
```bash
./download.sh
```
Or alternatively just give the video ID as a parameter
```bash
./download.sh VIDEOID
```

That's it!

### Result
The resulting archive is composed as follows:
- The video, in the highest quality possible for the audio and video (limited to codex compatible with the MP4 container format).
- Highest quality thumbnail, saved as WebP
- A `.live-chat.json` file containing an archive all the YouTube live chat
- A `.info.json` file containing most if not all metadata publicly available about the video (duration, uploader, channel_id, tags, available qualities...)
- A `.vtt` file for each subtitle language available.

## Import archives to Strapi

Create a .env.local file with the following information:
```txt
URL_GRAPHQL=https://path.to.strapi.com/graphql
ACCESS_TOKEN=token_generated_by_strapi
```

Then run the script using:

```bash
python3 importToStrapi.py
```

