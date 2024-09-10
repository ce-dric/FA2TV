import os
from tqdm import tqdm
from PIL import Image
import pillow_heif
from moviepy.editor import VideoFileClip

def convert_image(input_folder, output_folder):
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".heic")]
    
    for filename in tqdm(image_files, desc="Converting images"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + "_converted.jpg")
        
        heif_file = pillow_heif.read_heif(input_path)
        image = Image.frombytes(
            heif_file.mode, 
            heif_file.size, 
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        image.save(output_path, format="JPEG")
        print(f"Image {filename} converted to {output_path}")

def convert_video(input_folder, output_folder):
    video_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".mov")]
    
    for filename in tqdm(video_files, desc="Converting videos"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + "_converted.mp4")
        
        video = VideoFileClip(input_path)
        video.write_videofile(output_path, codec="libx264")
        print(f"Video {filename} converted to {output_path}")

def convert_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    convert_image(input_folder, output_folder)
    convert_video(input_folder, output_folder)

input_folder = "data"
output_folder = "output"

convert_files(input_folder, output_folder)
