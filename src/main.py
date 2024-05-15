import os, shutil

#Recursive function that copies the content of a directory to another directory, including all files and subdirectories.
#Delete the contents of public directory prior to copying. 

def copy_process(static, dest):
    for object in os.listdir(static):
        static_path = os.path.join(static, object)
        dest_path = os.path.join(dest, object)
        if os.path.isdir(static_path):
            os.makedirs(dest_path)
            copy_process(static_path, dest_path)
        else:
            shutil.copyfile(static_path, dest_path)

def copy_directory(static, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
        copy_process(static, dest)
    else:
        raise ValueError('Destination directory does not exist')

def main():
    

main()