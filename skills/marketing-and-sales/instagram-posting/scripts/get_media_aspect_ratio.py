import sys
import os
import json
import subprocess

def get_media_aspect_ratio(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
        
    try:
        # Use ffprobe to get media streams
        cmd = [
            'ffprobe', 
            '-v', 'quiet', 
            '-print_format', 'json', 
            '-show_streams', 
            file_path
        ]
        output = subprocess.check_output(cmd).decode('utf-8')
        data = json.loads(output)
        
        for stream in data.get('streams', []):
            if stream.get('codec_type') == 'video':
                width = stream.get('width')
                height = stream.get('height')
                if width and height:
                    ratio = width / height
                    # Map to Instagram crop options
                    if abs(ratio - 1.0) < 0.05:
                        return "1:1"
                    elif abs(ratio - 0.8) < 0.05:
                        return "4:5"
                    elif abs(ratio - 16/9) < 0.05:
                        return "16:9"
                    elif abs(ratio - 9/16) < 0.05:
                        # For Instagram Reels / Vertical, 9:16 is typical, 
                        # upload screen might use "Original" or "9:16"
                        return "9:16"
                    else:
                        return "Original"
        return "Original"
    except Exception as e:
        # Fallback if ffprobe fails (e.g., for images, though ffprobe works for images too)
        try:
            from PIL import Image
            with Image.open(file_path) as img:
                width, height = img.size
                ratio = width / height
                if abs(ratio - 1.0) < 0.05:
                    return "1:1"
                elif abs(ratio - 0.8) < 0.05:
                    return "4:5"
                elif abs(ratio - 16/9) < 0.05:
                    return "16:9"
                elif abs(ratio - 9/16) < 0.05:
                    return "9:16"
                else:
                    return "Original"
        except Exception as img_e:
            return "Original"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_media_aspect_ratio.py <file_path>")
        sys.exit(1)
    
    print(get_media_aspect_ratio(sys.argv[1]))
