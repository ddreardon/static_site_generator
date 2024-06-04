import os, shutil
from htmlnode import *

#Recursive function that copies the content of a directory to another directory, including all files and subdirectories.
#Delete the contents of public directory prior to copying. 

def copy_process(src, dest):
    for object in os.listdir(src):
        src_path = os.path.join(src, object)
        dest_path = os.path.join(dest, object)
        if os.path.isdir(src_path):
            os.makedirs(dest_path)
            copy_process(src_path, dest_path)
        else:
            shutil.copyfile(src_path, dest_path)

def copy_directory(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
        os.makedirs(dest)
        copy_process(src, dest)
    else:
        raise ValueError('Destination directory does not exist')

def extract_title(markdown):
#function which grabs the text of the h1 header of a markdown file and returns it as a string.
#raises an exception when no h1 header is found.
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:]
    raise Exception('No h1 header found')

def generate_page(from_path, template_path, dest_path):
#prints a message saying that the page is being generated
#reads the contents of the file and stores it as a variable
#reads the template file and stores it as a variable
#uses the markdown_to_html_node function and .to_html() method to convert markdown file to html
#uses the extract_title function to extract the title of the file
#replaces the title and content placeholders in the template with the title and html content
#writes the new html file at dest_path, creating any new directories if necessary

    print(f'Generating page {from_path} to {dest_path} using {template_path}')
    with open(from_path, 'r') as file:
        content = file.read()
    with open(template_path, 'r') as file:
        template = file.read()
    html_content = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    template = template.replace('{{ Title }}', title).replace('{{ Content }}', html_content)
    with open(dest_path, 'w') as file:
        file.write(template)
    
    

def main():
    copy_directory('./src/static', './public')
    generate_page('./content/index.md', './template.html', './public/index.html')
    

main()