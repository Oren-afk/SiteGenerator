import os
import shutil

def copy_files(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.makedirs(destination, exist_ok=True)
    for filename in os.listdir(source):
        from_path = os.path.join(source, filename)
        dest_path = os.path.join(destination, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files(from_path, dest_path)
