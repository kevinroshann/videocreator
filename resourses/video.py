from moviepy.editor import *

text = "This is your long text that may overflow and needs to be displayed as multiple lines."
image_paths = [
    r"C:\Users\ekn\Desktop\github-projects\video creator\imgs\Messi breaking records\0.jpg",
    r"C:\Users\ekn\Desktop\github-projects\video creator\imgs\Messi breaking records\1.jpg",
    # Add more image paths as needed
]

# Define padding
padding = 50  # Adjust as needed

# Create a VideoClip with a solid color background for padding
background_clip = ColorClip((1920, 1080), color=(255, 255, 255)).set_duration(5)  # Adjust size and duration as needed

# Create text clip with multiline support
text_clip = TextClip(text, font="Arial", fontsize=72, color='black', align='center', method='caption', size=(1920 - 2 * padding, None)).set_duration(5)

# Get the height of the text clip
text_height = text_clip.h

# Calculate the y-coordinate for positioning the text clip at the bottom
y_position = 1080 - text_height - padding

# Position the text clip horizontally centered and at the bottom
text_clip = text_clip.set_position(("center", y_position))

# Create a list to store image clips
image_clips = []
audio_clip = AudioFileClip(r"C:\Users\ekn\Desktop\github-projects\video creator\audio\Messi breaking records.wav")
# Load image clips from the image paths
for image_path in image_paths:
    image_clip = ImageClip(image_path, duration=5).resize((1920, 1080))  # Match text duration and size
    image_clips.append(image_clip)

# Position the images and text clip in a CompositeVideoClip
composite_clip = CompositeVideoClip([
    background_clip.set_position(("center", "center")),
    *[(clip.set_position(("center", "center")).set_start(idx * 5)) for idx, clip in enumerate(image_clips)],
    text_clip
])

# Write the composite clip to a video file
final_clip = composite_clip.set_audio(audio_clip)

# Write the final clip to a video file
final_clip.write_videofile("output_video.mp4", fps=24)
