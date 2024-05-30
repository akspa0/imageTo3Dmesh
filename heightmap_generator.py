import os
import argparse
import numpy as np
from PIL import Image
from tqdm import tqdm
import scipy.ndimage

def create_height_map(image):
    normalized_image = np.array(image.convert('L')) / 255.0
    height_maps = []

    # Map grayscale values to the desired depth ranges
    depth_0_0_5 = normalized_image.copy()
    depth_0_0_5[depth_0_0_5 > 0.5] = 0.5
    height_map_0_0_5 = (depth_0_0_5 / 0.5) * 127

    depth_0_5_1 = normalized_image.copy()
    depth_0_5_1[depth_0_5_1 <= 0.5] = 0.5
    height_map_0_5_1 = ((depth_0_5_1 - 0.5) / 0.5) * 127 + 128

    height_maps.append(height_map_0_0_5.astype(np.uint8))
    height_maps.append(height_map_0_5_1.astype(np.uint8))
    height_maps.append((normalized_image * 255).astype(np.uint8))

    return height_maps

def process_images(image_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    image_files = [f for f in os.listdir(image_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for image_file in tqdm(image_files, desc='Processing Images'):
        image = Image.open(os.path.join(image_path, image_file))
        height_maps = create_height_map(image)
        levels = ['low', 'mid', 'high']
        for level, height_map in zip(levels, height_maps):
            output_file = os.path.join(output_dir, f"{os.path.splitext(image_file)[0]}_{level}.png")
            Image.fromarray(height_map).save(output_file)

def main():
    parser = argparse.ArgumentParser(description="Generate grayscale height maps from images")
    parser.add_argument("image_path", help="Path to the directory containing input image files")
    parser.add_argument("--output-dir", "-o", default="height_maps", help="Output directory for height maps (default: height_maps)")
    args = parser.parse_args()

    process_images(args.image_path, args.output_dir)

if __name__ == "__main__":
    main()
