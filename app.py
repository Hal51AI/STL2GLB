import trimesh
import tempfile
import atexit
import shutil
import pathlib
import gradio as gr


def cleanup_temp_directories():
    print("Deleting temporary files")
    for temp_dir in temp_directories:
        try:
            shutil.rmtree(temp_dir)
        except FileNotFoundError:
            print(f"Could not delete directory {temp_dir}")


def stl2glb(glb_file):
    if not glb_file.endswith(".stl"):
        raise gr.Error("Please upload a .stl file")

    temp_dir = pathlib.Path(tempfile.mkdtemp())
    temp_directories.append(temp_dir)

    mesh = trimesh.load(glb_file)
    glb = trimesh.exchange.gltf.export_glb(mesh)

    output_file = (temp_dir / glb_file).with_suffix(".glb")
    with open(output_file, "wb") as f:
        f.write(glb)

    return str(output_file)


if __name__ == "__main__":
    temp_directories = []
    atexit.register(cleanup_temp_directories)

    demo = gr.Interface(
        fn=stl2glb,
        inputs=gr.Model3D(label="STL File"),
        outputs=gr.Model3D(label="GLB File"),
        examples=["space_shuttle.stl"],
        title="STL2GLB Converter",
        description="Convert a .stl file to a .glb file",
        analytics_enabled=False,
    )
    demo.launch(share=False)
