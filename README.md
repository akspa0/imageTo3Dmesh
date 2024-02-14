# Image to 3D Mesh Converter

This script converts input images into 3D mesh data represented in JSON format. It generates a mesh by dividing the image into chunks, creating a point cloud for each chunk, and then triangulating the point cloud to form the mesh.

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- NumPy
- SciPy
- tqdm

## Usage

1. **Installation**: Make sure you have Python installed. Install the required packages using pip:
   
   ```
   pip install opencv-python numpy scipy tqdm
   ```

2. **Running the Script**: Run the script `image_to_3d_mesh.py` with the following command-line arguments:

   ```
   python image_to_3d_mesh.py input_path output_dir [--options]
   ```

   - `input_path`: Path to the input image or directory containing images.
   - `output_dir`: Directory to save the generated mesh data and optionally the processed images.
   - Options:
     - `--chunk_size`: Size of the chunks (default: 256).
     - `--overlap`: Overlap size between chunks (default: 32).
     - `--z_scale`: Scale for depth values (default: 1.0).
     - `--downsample`: Downsample input images (default: False).
     - `--positive_z_only`: Disable negative Z values (default: False).
     - `--flip_x`: Flip X coordinates (default: False).
     - `--flip_y`: Flip Y coordinates (default: False).
     - `--flip_z`: Flip Z coordinates (default: False).
     - `--export_processed_image`: Export processed image (default: False).

3. **Output**: The script generates JSON files containing mesh data for each input image in the specified output directory. Optionally, processed images (blurred and/or downsampled) can be exported alongside the JSON files.

## Examples

1. Convert a single image:

   ```
   python image_to_3d_mesh.py input_image.png output_directory --export_processed_image
   ```

2. Convert all images in a directory:

   ```
   python image_to_3d_mesh.py input_directory output_directory --flip_x --flip_z
   ```

3. Convert images with specific options:

   ```
   python image_to_3d_mesh.py input_directory output_directory --downsample --positive_z_only
   ```

## Notes

- Ensure input images are in a format supported by OpenCV (e.g., PNG, JPEG).
- Adjust options such as chunk size, overlap, and coordinate flipping based on the desired output.

---

# Mesh Data Converter

This script converts JSON mesh data into various 3D mesh formats using the Trimesh library.

## Usage

```bash
python mesh_converter.py input_json output_dir
```

- `input_json`: Path to the input JSON file containing mesh data.
- `output_dir`: Directory to save the exported meshes.

## Dependencies

- Python 3.x
- Trimesh library

## Installation

You can install Trimesh via pip:

```bash
pip install trimesh
```

## Example

```bash
python mesh_converter.py mesh_data.json exported_meshes
```

This will convert the mesh data from `mesh_data.json` into OBJ, STL (ASCII), and PLY formats, saving them in the `exported_meshes` directory.

## License

This script is released under the MIT License. See `LICENSE` for more information.