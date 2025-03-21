import os
import shutil
from pathlib import Path

def define_path(path = '/home/husseingm/Downloads/'):
    """
    Changes the current working directory to the specified path and returns it.

    Args:
        path (str, optional): The directory path to change to. 
            Defaults to '/home/husseingm/Downloads/'.

    Returns:
        str: The path that was set as the current working directory.

    Raises:
        OSError: If the specified path does not exist or is not accessible.
    """
    os.chdir(path)
    print("Target path is selected as: {}".format(path))
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
    """
    Main function for the file organizer application.
    This function orchestrates the file organization process by:
    1. Defining the target directory path
    2. Getting unique file extensions in the directory
    3. Creating folders for each extension type
    4. Moving files into their respective folders
    The function executes these steps in sequence using helper functions:
    - define_path(): Gets the directory path to organize
    - get_extensions(): Identifies unique file extensions
    - make_folders(): Creates folders for each extension
    - move_files(): Moves files into appropriate folders
    Returns:
        None
    """
    
    path = define_path()
    
    extensions = get_extensions(path)
    
    make_folders(path, extensions)
    
    move_files(path)

if __name__ == '__main__': main()
