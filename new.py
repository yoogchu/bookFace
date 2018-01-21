import subprocess

subprocess.call(
    ["ffmpeg -i fuhax.mov -vcodec h264 -s 160x160 output.mp4 -y"],
    stdout=subprocess.PIPE, shell=True)
