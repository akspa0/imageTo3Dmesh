import os
import json
import argparse
import trimesh

def export_to_formats(mesh_data, output_dir):
    for chunk in mesh_data:
        vertices = chunk["vertices"]
        faces = chunk["faces"]

        # Create a trimesh object
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

        # Export to various formats
        obj_path = os.path.join(output_dir, f"chunk_{chunk['index']}.obj")
        stl_path = os.path.join(output_dir, f"chunk_{chunk['index']}.stl")
        ply_path = os.path.join(output_dir, f"chunk_{chunk['index']}.ply")

        mesh.export(file_obj=obj_path, file_type="obj")
        mesh.export(file_obj=stl_path, file_type="stl_ascii")  # Export as ASCII STL
        mesh.export(file_obj=ply_path, file_type="ply")

def main():
    parser = argparse.ArgumentParser(description="Convert JSON mesh data to various formats.")
    parser.add_argument("input_json", help="Input JSON file containing mesh data.")
    parser.add_argument("output_dir", help="Directory to save the exported meshes.")
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    with open(args.input_json, "r") as json_file:
        mesh_data = json.load(json_file)

    export_to_formats(mesh_data, args.output_dir)

if __name__ == "__main__":
    main()
