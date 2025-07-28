import os
from pillow_heif import register_heif_opener
from PIL import Image
from tqdm import tqdm

register_heif_opener()

input_folder = "HEIC to JPEG\input"
output_folder = "HEIC to JPEG\output"
os.makedirs(output_folder, exist_ok=True)

# Get all HEIC files
heic_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".heic")]

# Show progress bar
for filename in tqdm(heic_files, desc="Converting & Resizing", unit="file"):
    input_path = os.path.join(input_folder, filename)
    output_filename = os.path.splitext(filename)[0] + ".jpg"
    output_path = os.path.join(output_folder, output_filename)

    try:
        image = Image.open(input_path).convert("RGB")
        image = image.resize((640, 640))
        image.save(output_path, "JPEG", quality=95)
    except Exception as e:
        tqdm.write(f"Failed: {filename} — {e}")
