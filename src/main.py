import os
import shutil
from copystatic import copy_files
from markdown_blocks import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    os.makedirs(dir_path_public)

    print("Copying static files to public directory...")
    copy_files(dir_path_static, dir_path_public)
    
    print("Generating HTML pages...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

main()