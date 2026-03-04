from PIL import Image
import os

def convert_to_ico(source_path, target_path):
    if not os.path.exists(source_path):
        print(f"Error: {source_path} not found.")
        return
        
    img = Image.open(source_path)
    # Standard ICO sizes
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(target_path, format='ICO', sizes=sizes)
    print(f"Successfully converted {source_path} to {target_path}")

if __name__ == "__main__":
    convert_to_ico("logo.png", "logo.ico")
