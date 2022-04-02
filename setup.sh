wget https://github.com/yt-dlp/FFmpeg-Builds/releases/download/autobuild-2022-04-01-12-45/ffmpeg-n5.0-49-gcfe1e278e2-linux64-gpl-5.0.tar.xz
tar -xf *.tar.xz
mv ffmpeg-*/bin/ffmpeg .
mv ffmpeg-*/bin/ffprobe .
rm -r ffmpeg-*

wget https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.2.2-rc1-linux-x86-64.tar.gz
tar -xf *.tar.gz
mv libwebp-*/bin/cwebp .
rm -r libwebp-*

cd youtube
wget https://github.com/yt-dlp/yt-dlp/releases/download/2022.03.08.1/yt-dlp
chmod +x yt-dlp
