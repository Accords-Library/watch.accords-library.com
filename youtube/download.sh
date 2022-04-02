id="$1"
ending="$id"

shift
./yt-dlp \
  --ignore-config \
  --no-continue \
  --no-overwrites \
  --sub-langs all \
  --prefer-free-formats \
  --embed-subs \
  --embed-chapters \
  --embed-thumbnail \
  --embed-metadata \
  --write-subs \
  --write-thumbnail \
  --write-info-json \
  --convert-thumbnails webp \
  --output '../public/videos/%(id)s.%(ext)s' \
  --merge-output-format mp4 \
  --ffmpeg-location '..' \
  --batch-file 'batchfile.txt' \
  --download-archive 'donearchive.txt' \
  --cookies 'cookies.txt' \
  "$@" \
  -- "$id"
  #--abort-on-error \