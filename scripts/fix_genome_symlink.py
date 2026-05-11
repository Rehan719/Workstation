import os
import sys
import platform
import shutil
import subprocess

def fix_genome_symlink():
    """
    Ensures a cross-platform link exists from agentic_core/genome to agentic_core/genetic_immune/genome.
    Uses junctions on Windows and symbolic links on Unix.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(base_dir, "agentic_core", "genetic_immune", "genome")
    link_path = os.path.join(base_dir, "agentic_core", "genome")

    print(f"Target: {target_dir}")
    print(f"Link:   {link_path}")

    # Remove existing link/file if it's not a link or pointing to the wrong place
    if os.path.exists(link_path) or os.path.islink(link_path):
        print("Cleaning up existing path at agentic_core/genome...")
        if os.path.islink(link_path):
             os.remove(link_path)
        elif os.path.isdir(link_path):
            if platform.system() == "Windows":
                # Check if it's a junction
                subprocess.call(f'rmdir "{link_path}"', shell=True)
            else:
                shutil.rmtree(link_path)
        else:
            os.remove(link_path)

    os_name = platform.system()
    try:
        if os_name == "Windows":
            print("Detected Windows. Creating Directory Junction...")
            # Use mklink /J for a junction which doesn't require admin privileges
            subprocess.check_call(f'mklink /J "{link_path}" "{target_dir}"', shell=True)
            print("Successfully created Windows Junction.")
        else:
            print(f"Detected {os_name}. Creating Symbolic Link...")
            os.symlink(target_dir, link_path)
            print("Successfully created Symbolic Link.")
    except Exception as e:
        print(f"Failed to create link: {e}")
        if not os.path.exists(link_path):
            print("Falling back to directory copy...")
            shutil.copytree(target_dir, link_path)
            print("Successfully copied directory.")

if __name__ == "__main__":
    fix_genome_symlink()
