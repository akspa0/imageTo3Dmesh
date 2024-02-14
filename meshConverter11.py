import os
import json
import argparse
import trimesh
from tqdm import tqdm

def export_to_formats(mesh_data, output_dir, file_name):
    for chunk in tqdm(mesh_data, desc=f"Converting {file_name}"):
        vertices = chunk["vertices"]
        faces = chunk["faces"]

        # Create a trimesh object
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

        # Export to various formats
        obj_path = os.path.join(output_dir, f"{file_name}_chunk_{chunk['index']}.obj")
        stl_path = os.path.join(output_dir, f"{file_name}_chunk_{chunk['index']}.stl")
        ply_path = os.path.join(output_dir, f"{file_name}_chunk_{chunk['index']}.ply")

        mesh.export(file_obj=obj_path, file_type="obj")
        mesh.export(file_obj=stl_path, file_type="stl_ascii")  # Export as ASCII STL
        mesh.export(file_obj=ply_path, file_type="ply")

def main():
    parser = argparse.ArgumentParser(description="Convert JSON mesh data to various formats.")
    parser.add_argument("input_path", help="Path to the input JSON file or directory containing mesh data.")
    parser.add_argument("output_dir", help="Directory to save the exported meshes.")
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    if os.path.isdir(args.input_path):
        # If input path is a directory, process all JSON files in the directory
        json_files = [f for f in os.listdir(args.input_path) if f.endswith('.json')]
        for json_file in json_files:
            input_file = os.path.join(args.input_path, json_file)
            file_name = os.path.splitext(json_file)[0]  # Extract base filename without extension
            with open(input_file, "r") as f:
                mesh_data = json.load(f)
            export_to_formats(mesh_data, args.output_dir, file_name)
    elif os.path.isfile(args.input_path) and args.input_path.endswith('.json'):
        # If input path is a JSON file, process that file
        file_name = os.path.splitext(os.path.basename(args.input_path))[0]  # Extract base filename without extension
        with open(args.input_path, "r") as f:
            mesh_data = json.load(f)
        export_to_formats(mesh_data, args.output_dir, file_name)
    else:
        print("Error: Input path should be a JSON file or directory containing JSON files.")

if __name__ == "__main__":
    main()
