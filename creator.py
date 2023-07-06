import os
import re
import argparse
from moviepy.editor import *

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--smooth', action='store_true', help='Enable smooth transitions')
parser.add_argument('--resolution', type=int, default=1024, help='Resolution of the output video (square)')
parser.add_argument('--fps', type=int, default=24, help='Frames per second in the output video')
parser.add_argument('--output', type=str, default="infinite_video", help='Name of the output video file (without extension)')
args = parser.parse_args()

# Getting the list of images
image_folder = "imgs"
images = [i for i in os.listdir(image_folder) if i.endswith(".png")]

# Sorting images by number in their name in reverse order
images.sort(key=lambda f: int(re.search(r"(\d+)", f).group()), reverse=True)

# Transform images into zooming clips
clips = []
for img in images:
    clip = ImageClip(os.path.join(image_folder, img))

    # Setting the clip duration
    clip = clip.set_duration(3)  # Each image will be displayed for 3 seconds

    # Resize image from 200% to 100% size during the clip
    zoom_clip = clip.resize(lambda t: 2 - t / clip.duration)

    # Apply crossfadein and crossfadeout to final video if smooth flag is passed
    if args.smooth:
        zoom_clip = zoom_clip.crossfadein(1).crossfadeout(1)

    clips.append(zoom_clip)

# Concatenate all zooming clips into a final video
final_video = concatenate_videoclips(clips, method="compose")

# Crop the final video
final_video = final_video.crop(x_center=final_video.w/2, y_center=final_video.h/2, width=final_video.w/2, height=final_video.h/2)

# Resize the final video to the desired resolution
final_video = final_video.resize((args.resolution, args.resolution))

# Write the result to a file, automatically adding .mp4 extension
final_video.write_videofile(f"{args.output}.mp4", fps=args.fps)

