import argparse
import os
import shutil
from pathlib import Path

def define_path():
    """
    Function to define and validate the path provided through command line arguments.
    This function sets up argument parsing for a directory path, validates its existence,
    and returns the path as a Path object.
    Returns:
        Path: A pathlib.Path object representing the validated directory path.
    Raises:
        SystemExit: If the specified directory path does not exist.
    Example:
        >>> path = define_path()  # When called with -p /some/directory
        The directory is now selected as: directory
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path')
    args = parser.parse_args()
    
    path = Path(args.path)
    
    print("The directory is now selected as: {}".format(path.name))
    
    if not path.exists():
        print("The entered directory dose not exists")
        raise SystemExit(1)
    
    return path

def get_extensions(path):
    """
    Get unique file extensions from a given directory.
    Args:
        path (str or Path): Path to the directory to scan for file extensions.
    Returns:
        set: A set of unique file extensions (without the leading dot) found in the directory.
    Example:
        >>> get_extensions('/path/to/directory')
        {'txt', 'pdf', 'doc'}
    """
    directory = Path(path)
    
    extensions = set(file.suffix[1: ] for file in directory.iterdir() if file.is_file())
    return extensions

def make_folders(directory, extensions):
    """
    Creates folders for each file extension in the specified directory.

    Args:
        directory (Path): The path object representing the target directory where folders will be created
        extensions (list): List of file extensions (without dots) for which folders should be created

    Example:
        If extensions=['pdf', 'txt'], it will create 'pdf' and 'txt' folders in the specified directory

    Note:
        - Uses os.makedirs with exist_ok=True to avoid errors if folders already exist
        - Folder names will match exactly the extension strings provided
    """
    for extension in extensions:
        folder = directory.joinpath(f'{extension}')
        os.makedirs(folder, exist_ok=True)
    
    folders = ', '.join(extensions)
    print(f'{folders}; are created successfully')

def move_files(directory):
    """
    Moves files in the given directory to subdirectories based on their file extensions.

    For example, a file named 'document.pdf' will be moved to a 'pdf' subdirectory.

    Args:
        directory (Path): A pathlib.Path object representing the directory to organize.

    Raises:
        FileNotFoundError: If the specified directory doesn't exist.
        PermissionError: If there are insufficient permissions to move files.
        shutil.Error: If there's an error during the file moving operation.
    """
    for file in directory.iterdir():
        if file.is_file():
            shutil.move(file, f'{directory}/{file.suffix[1: ]}')
    
    print("Files moved to specified folders successfully")

def main():
    pass

if __name__ == '__main__': main()
