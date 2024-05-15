import os, shutil

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

def main():
    copy_directory('./static', '../public')
    

main()