import os
from PIL import Image
import pillow_heif
import ffmpeg
from moviepy.editor import VideoFileClip

def convert_files(input_folder, output_folder, progress_callback, log_callback):
    total_files = sum([len(files) for _, _, files in os.walk(input_folder)])
    processed_files = 0

    for root, _, files in os.walk(input_folder):
        rel_path = os.path.relpath(root, input_folder)
        output_dir = os.path.join(output_folder, rel_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for filename in files:
            if filename.startswith('._'):
                log_callback(f"Skipping hidden metadata file: {filename}", "skipped")
                continue

            input_file_path = os.path.join(root, filename)
            try:
                if filename.lower().endswith(".heic"):
                    convert_image(input_file_path, output_dir, filename, log_callback)
                elif filename.lower().endswith(".mov"):
                    convert_video(input_file_path, output_dir, filename, log_callback)
            except Exception as e:
                log_callback(f"Error converting {filename}: {str(e)}", "failed")

            processed_files += 1
            progress_callback(int((processed_files / total_files) * 100))

def convert_image(input_path, output_dir, filename, log_callback):
    output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.jpg')

    try:
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
        log_callback(f"Image {filename} converted to {output_path}.", "success")
    
    except ValueError as e:
        log_callback(f"Error using pillow-heif for {filename}: {str(e)}. Trying ffmpeg.", "failed")
        try:
            ffmpeg.input(input_path).output(output_path).run()
            log_callback(f"Image {filename} converted to {output_path} using ffmpeg.", "success")
        except ffmpeg.Error as e:
            log_callback(f"ffmpeg failed to convert {filename}: {e.stderr}", "failed")
            raise ValueError(f"Both pillow-heif and ffmpeg failed to convert {filename}")

def convert_video(input_path, output_dir, filename, log_callback):
    output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.mp4')

    try:
        video = VideoFileClip(input_path)
        video.write_videofile(output_path, codec="libx264")
        log_callback(f"Video {filename} converted to {output_path}.", "success")
    except Exception as e:
        log_callback(f"Error converting video {filename}: {str(e)}", "failed")
        raise ValueError(f"Failed to convert {filename}: {str(e)}")
