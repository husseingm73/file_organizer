import argparse
import json
import os
import shutil
from pathlib import Path

def define_options():
    """Process command line arguments and validate the provided directory path.
    This function sets up and processes command line arguments for the file organizer,
    including the target directory path, dry run option, and configuration file path.
    Returns:
        tuple: A tuple containing:
            - Path: The validated target directory path
            - bool: Flag indicating whether to perform a dry run
            - str: Path to the configuration file
    Raises:
        SystemExit: If the specified directory path does not exist
    Command Line Arguments:
        -p, --path: Target directory path (default: current working directory)
        --dry-run: Flag to perform a dry run without moving files
        -c, --config: Path to the configuration file (default: "config.json")
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', default=os.getcwd(), help="Target directory path which organization will happen")
    parser.add_argument('--dry-run', action="store_true", help="Perform a dry run without moving files to ensure functionality")
    parser.add_argument('-c', '--config', default="config.json", help="Path to the configuration file")
    args = parser.parse_args()
    
    path = Path(args.path)
    
    print("The directory is now selected as: {}".format(path.name))
    
    if not path.exists():
        print("The entered directory dose not exists")
        raise SystemExit(1)
    
    return path, args.dry_run, args.config

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def make_folders(path, dry_run, config):
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
    extension_groups = load_config(config)
    directory = Path(path)
    
    if not dry_run:
        others = directory / "Others"
        os.makedirs(others, exist_ok=True)
    else:
        print(f'[DRY RUN] Others folder will be create to move uncategorized formats into itself')
    
    dirs = []
    
    # Get a list of files to avoid modifying the directory during iteration.
    for content in list(directory.iterdir()):
        if content.is_file():
            moved = False
            for cat, exts in extension_groups.items():
                if content.suffix in exts:
                    target_dir = directory / cat
                    if dry_run:
                        print(f'{cat} folder created')
                        print(f'[DRY RUN] {content.name} will be move into {target_dir}')
                    else:
                        os.makedirs(target_dir, exist_ok=True)
                        shutil.move(str(content), str(target_dir))
                        print(f"'{content.name}' is one of {cat} so it will move to {target_dir}")
                    moved = True
                    break
            if not moved:
                if dry_run:
                    print(f'[DRY RUN] {content.name} will be move into Others')
                else:
                    shutil.move(str(content), str(others))
                    print(f"'{content.name}' did not match any group so it will move to {others}")

def main():
    path, dry_run, config = define_options()
    make_folders(path, dry_run, config)

if __name__ == '__main__': main()
