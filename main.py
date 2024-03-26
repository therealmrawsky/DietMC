import zipfile
import os
import random
import string
from PIL import Image
import shutil

def unpack_zipfile(zip_file_path, extract_to_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_path)

def compress_images(directory, max_size=(1024, 1024), quality=5):
    total_saved_bytes = 0
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    with Image.open(file_path) as img:
                        img.thumbnail(max_size)
                        original_size = os.path.getsize(file_path)
                        img.save(file_path, optimize=True, quality=quality)
                        new_size = os.path.getsize(file_path)
                        total_saved_bytes += (original_size - new_size)
                        print(f"Compressed {file} saved to {file_path}")
                except Exception as e:
                    print(f"Ignoring {file}: {e}")
    return total_saved_bytes

def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_path))

def rename_to_jar(zip_file_path):
    new_name = os.path.splitext(zip_file_path)[0] + '.jar'
    os.rename(zip_file_path, new_name)

def replace_splashes_txt(temp_dir):
    for root, _, files in os.walk(temp_dir):
        for file in files:
            if file == 'splashes.txt':
                try:
                    splashes_file_path = os.path.join(root, file)
                    with open(splashes_file_path, 'w') as splashes_file:
                        splashes_file.write("Optimized to the extreme with DietMC")
                    print(f"Replaced splashes.txt at: {splashes_file_path}")
                except Exception as e:
                    print(f"Error replacing splashes.txt at {splashes_file_path}: {e}")

def main():
    minecraft_directory = input("Enter the location of Minecraft directory: ")
    for root, _, files in os.walk(minecraft_directory):
        for file in files:
            if file.endswith('.jar'):
                jar_file_path = os.path.join(root, file)
                temp_dir = os.path.join(root, "temp_" + ''.join(random.choices(string.digits, k=5)))
                try:
                    unpack_zipfile(jar_file_path, temp_dir)
                    replace_splashes_txt(temp_dir)
                    saved_bytes = compress_images(temp_dir)
                    zip_output_path = os.path.join(root, "output.zip")
                    zip_folder(temp_dir, zip_output_path)
                    changed = os.path.getsize(jar_file_path) - os.path.getsize(zip_output_path)
                    original_file_name = os.path.splitext(jar_file_path)[0]
                    os.rename(zip_output_path, original_file_name + '.jar')
                    shutil.rmtree(temp_dir)
                    print(f"Compressed {file} saved {changed} bytes")
                except Exception as e:
                    print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    main()
