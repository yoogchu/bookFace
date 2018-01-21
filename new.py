import subprocess

subprocess.call(
    ["ffmpeg -i testvideo.mp4 -vcodec h264 -s 160x90 output.mp4 -y"],
    stdout=subprocess.PIPE, shell=True)
