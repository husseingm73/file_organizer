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
    parser.add_argument('-p', '--path', default=os.getcwd())
    args = parser.parse_args()
    
    path = Path(args.path)
    
    print("The directory is now selected as: {}".format(path.name))
    
    if not path.exists():
        print("The entered directory dose not exists")
        raise SystemExit(1)
    
    return path

def make_folders(path):
    """
    Organizes files in a directory by moving them into categorized folders based on their extensions.
    This function creates folders for different file types (e.g., Archives, Documents, Images)
    and moves files into their respective folders based on their extensions. Files with
    unrecognized extensions are moved to an 'Others' folder.
    Args:
        path (str): The directory path where files need to be organized.
    Example:
        >>> make_folders('/path/to/directory')
        'example.pdf' is one of Documents so it will move to /path/to/directory/Documents
        'unknown.xyz' did not match any group so it will move to /path/to/directory/Others
    Note:
        - Creates directories if they don't exist
        - Prints messages indicating where each file is moved
        - Handles various file types including:
            * Archives (.zip, .tar, etc.)
            * Documents (.pdf, .doc, etc.)
            * Images (.jpg, .png, etc.)
            * Videos (.mp4, .avi, etc.)
            * And more...
    Requires:
        - os
        - shutil
        - pathlib.Path
    """
    extension_groups = {
        "Archives": ['.zip', '.tar', '.gz', '.bz2', '.rar', '.7z', '.xz'],
        "Documents": ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.ods'],
        "Images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
        "Videos": ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'],
        "Audio": ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma', '.m4a'],
        "Executables": ['.exe', '.bin', '.sh', '.bat', '.msi', '.apk', '.deb'],
        "Scripts": ['.py', '.js', '.html', '.css', '.php', '.rb', '.pl', '.java', '.c', '.cpp'],
        "Miscellaneous": ['.log', '.tmp', '.bak', '.old', '.json', '.xml', '.csv', '.yaml', '.yml'],
        "Fonts": ['.ttf', '.otf', '.woff', '.woff2'],
        "CAD": ['.dwg', '.dxf'],
        "3D Models": ['.obj', '.fbx', '.stl', '.dae'],
        "Database": ['.sql', '.db', '.sqlite', '.mdb', '.accdb'],
        "System": ['.sys', '.dll', '.ini', '.cfg'],
    }
    directory = Path(path)
    others = directory / "Others"
    os.makedirs(others, exist_ok=True)
    
    # Get a list of files to avoid modifying the directory during iteration.
    for content in list(directory.iterdir()):
        if content.is_file():
            moved = False
            for cat, exts in extension_groups.items():
                if content.suffix in exts:
                    target_dir = directory / cat
                    os.makedirs(target_dir, exist_ok=True)
                    shutil.move(str(content), str(target_dir))
                    print(f"'{content.name}' is one of {cat} so it will move to {target_dir}")
                    moved = True
                    break
            if not moved:
                shutil.move(str(content), str(others))
                print(f"'{content.name}' did not match any group so it will move to {others}")

def main():
    pass

if __name__ == '__main__': main()
