from moviepy.editor import VideoFileClip, concatenate_videoclips

# Paths to the video files you want to combine
video_paths = [
    "video1.mp4",
    "video2.mp4",
    # Add more video paths as needed
]

# Load each video clip
video_clips = [VideoFileClip(path) for path in video_paths]

# Concatenate the video clips
final_clip = concatenate_videoclips(video_clips)

# Write the final combined video to a file
final_clip.write_videofile("combined_video.mp4")
