import cv2
import numpy as np
import argparse
import os
import json
from tqdm import tqdm
from scipy.spatial import Delaunay

def chunk_image(image, chunk_size, overlap):
    chunks = []
    height, width = image.shape[:2]
    step = chunk_size - overlap
    for y in range(0, height - overlap, step):
        for x in range(0, width - overlap, step):
            x_end = x + chunk_size if (x + chunk_size) <= width else width
            y_end = y + chunk_size if (y + chunk_size) <= height else height
            chunk = image[y:y_end, x:x_end]
            chunks.append(chunk)
    return chunks

def generate_point_cloud(chunk, z_scale=1.0):
    height, width = chunk.shape[:2]
    x, y = np.meshgrid(np.arange(width), np.arange(height))
    z = chunk.astype(float) * z_scale
    x, y, z = x.flatten(), y.flatten(), z.flatten()
    points = np.vstack((x, y, z)).T
    return points

def generate_faces_normals_polygons(points):
    tri = Delaunay(np.array(points)[:, :2])
    faces = tri.simplices
    # Calculate normals
    normals = np.cross(points[faces[:, 1]] - points[faces[:, 0]], points[faces[:, 2]] - points[faces[:, 0]])
    normals /= np.linalg.norm(normals, axis=1)[:, np.newaxis]
    # Calculate polygons
    polygons = np.repeat(np.arange(len(faces)), 3)
    return faces.tolist(), normals.tolist(), polygons.tolist()

def process_image(image_path, output_dir, chunk_size, overlap, z_scale, downsample, positive_z_only, flip_x, flip_y, flip_z, export_processed_image):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        print(f"Error loading image: {image_path}")
        return
    
    # Convert to grayscale if color image
    if len(image.shape) == 3 and image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Downsample if required
    if downsample:
        downsampled_image = cv2.resize(image, None, fx=0.5, fy=0.5)
    else:
        downsampled_image = image
    
    # Apply Gaussian blur for smoothing
    blurred_image = cv2.GaussianBlur(downsampled_image, (5, 5), 0)
    
    # Export processed image if requested
    if export_processed_image:
        processed_image_path = os.path.join(output_dir, f"processed_{os.path.basename(image_path)}")
        cv2.imwrite(processed_image_path, blurred_image)
        print(f"Exported processed image to {processed_image_path}")
    
    # Chunk the image
    chunks = chunk_image(blurred_image, chunk_size, overlap)
    
    mesh_data = []
    for i, chunk in enumerate(tqdm(chunks, desc="Processing chunks")):
        # Generate point cloud
        points = generate_point_cloud(chunk, z_scale)
        
        # Flip coordinates if necessary
        if flip_x:
            points[:, 0] = -points[:, 0]
        if flip_y:
            points[:, 1] = -points[:, 1]
        if flip_z:
            points[:, 2] = -points[:, 2]
        
        # Generate faces, normals, and polygons
        faces, normals, polygons = generate_faces_normals_polygons(points)
        
        mesh_data.append({
            "index": i,
            "vertices": points.tolist(),
            "faces": faces,
            "normals": normals,
            "polygons": polygons
        })
    
    # Save mesh data to JSON file
    output_json_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(image_path))[0]}.json")
    with open(output_json_path, "w") as json_file:
        json.dump(mesh_data, json_file)
    print(f"Exported mesh data to {output_json_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate 3D meshes from images or depth maps.")
    parser.add_argument("input_path", help="Input image or directory of images.")
    parser.add_argument("output_dir", help="Directory to save the generated mesh data.")
    parser.add_argument("--chunk_size", type=int, default=256, help="Size of the chunks.")
    parser.add_argument("--overlap", type=int, default=32, help="Overlap size between chunks.")
    parser.add_argument("--z_scale", type=float, default=1.0, help="Scale for depth values.")
    parser.add_argument("--downsample", action="store_true", help="Downsample input images.")
    parser.add_argument("--positive_z_only", action="store_true", help="Disable negative Z values.")
    parser.add_argument("--flip_x", action="store_true", help="Flip X coordinates.")
    parser.add_argument("--flip_y", action="store_true", help="Flip Y coordinates.")
    parser.add_argument("--flip_z", action="store_true", help="Flip Z coordinates.")
    parser.add_argument("--export_processed_image", action="store_true", help="Export processed image.")
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    if os.path.isdir(args.input_path):
        filenames = [f for f in os.listdir(args.input_path) if os.path.isfile(os.path.join(args.input_path, f))]
        for filename in tqdm(filenames, desc="Processing directory"):
            file_path = os.path.join(args.input_path, filename)
            process_image(file_path, args.output_dir, args.chunk_size, args.overlap, args.z_scale, args.downsample, args.positive_z_only, args.flip_x, args.flip_y, args.flip_z, args.export_processed_image)
    else:
        process_image(args.input_path, args.output_dir, args.chunk_size, args.overlap, args.z_scale, args.downsample, args.positive_z_only, args.flip_x, args.flip_y, args.flip_z, args.export_processed_image)

if __name__ == "__main__":
    main()
