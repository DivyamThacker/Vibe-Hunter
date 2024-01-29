import pytube
import os
from scraper import song_links

def download(video_url):
  # Create a YouTube object
  yt = pytube.YouTube(video_url)

  # Get the audio stream with the highest bitrate
  audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
  # Download the audio stream as an MP3 file
  out_file = audio_stream.download()
  # Optionally, rename the downloaded file
  base, ext = os.path.splitext(out_file)
  new_file = base + '.mp3'
  os.rename(out_file, new_file)

  print("MP3 downloaded successfully:", new_file)

for song_link in song_links:
  download(song_link)