import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip

# List of text
text_list = [
    "The US Federal Trade Commission (FTC) has filed a lawsuit against Facebook, alleging that the social media giant has been illegally maintaining its monopoly.",
    "Google has announced that it will be shutting down its cloud printing service by the end of 2022.",
    "Apple has released its new MacBook Pro with an M1 Max chip, which is said to be the most powerful chip ever made for a laptop.",
    "Amazon has announced that it will be opening its first brick-and-mortar store in New York City.",
    "Microsoft has announced that it will be acquiring Activision Blizzard for $68.7 billion."
]

# Slide dimensions
slide_width =1920
slide_height = 1080

# Font settings
font_size = 24
font_path = "Algerian.ttf"  # Replace with your font file path

# Background and text color
background_color = (255, 255, 255)  # White
text_color = (0, 0, 0)  # Black

# Output video settings
output_file = "output_video.mp4"
fps = 0.1  # Frames per second

# Create a list to store slide images
slide_images = []

# Create slides from the text list
for text in text_list:
    # Create a blank slide image
    slide_image = Image.new("RGB", (slide_width, slide_height), background_color)
    draw = ImageDraw.Draw(slide_image)

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Calculate text position
    text_width, text_height = draw.textsize(text, font=font)
    text_position = ((slide_width - text_width) // 2, (slide_height - text_height) // 2)

    # Draw the text on the slide
   # Draw the text on the slide
    draw.text(text_position, text, font=font, fill=text_color)

    # Append the slide image to the list after converting to a NumPy array
    slide_images.append(np.array(slide_image))

# Create a video from the slide images
video_clip = ImageSequenceClip(slide_images, fps=fps)

# Save the video
video_clip.write_videofile(output_file)

# Optional: Display the video
video_clip.preview()
