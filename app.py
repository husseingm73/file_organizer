""" 
A file organization utility that categorizes and moves files into appropriate folders 
based on their extensions.

This script provides functionality to organize files in a specified directory by moving them 
into categorized folders based on their file extensions. It supports both actual file operations 
and dry runs for testing purposes.

Functions:
    define_options(): Process command line arguments and validate directory path
    load_config(config_path): Load categorization rules from a JSON configuration file
    file_organizer(path, dry_run, config): Organize files into appropriate folders
    main(): Entry point of the script

Configuration:
    The script expects a JSON configuration file that defines file extension mappings to 
    category folders. For example:
    {
        "Documents": [".pdf", ".doc", ".txt"],
        "Images": [".jpg", ".png", ".gif"],
        ...
    }

Example Usage:
    python app.py -p /path/to/directory --dry-run
    python app.py -p /path/to/directory -c custom_config.json

Dependencies:
    - argparse
    - json
    - pathlib

Notes:
    - Creates category folders automatically if they don't exist.
    - Moves unrecognized file types to an 'Others' folder.
    - Provides detailed output of file operations.
    - Supports dry run mode for testing.
"""

import argparse    # Module for parsing command-line arguments.
import json        # Module to handle JSON files.
import os          # Module to work with operating system functionalities.
import shutil      # Module to perform file operations such as moving files.
from pathlib import Path  # Module for handling filesystem paths in an object-oriented way.

def define_options():
    """
    Process command line arguments and validate the provided directory path.
    
    This function sets up and processes command line arguments for the file organizer,
    including:
        - Target directory path (with default as the current working directory)
        - Dry run flag to simulate moves without performing file operations
        - Configuration file path for extension mappings
    
    Returns:
        dict: A dictionary containing:
            - "path": The validated directory path as a Path object.
            - "dry-run": A boolean flag indicating if it's a dry run.
            - "config": The path to the configuration file.
    
    Raises:
        SystemExit: If the specified directory does not exist.
    """
    # Create an argument parser instance.
    parser = argparse.ArgumentParser()
    
    # Add the directory path argument, defaulting to the current working directory.
    parser.add_argument('-p', '--path', default=os.getcwd(), 
                        help="Target directory path which organization will happen")
    
    # Add a flag for dry-run mode where files are not actually moved.
    parser.add_argument('--dry-run', action="store_true", 
                        help="Perform a dry run without moving files to ensure functionality")
    
    # Add an argument for specifying the configuration file path.
    parser.add_argument('-c', '--config', default="config.json", 
                        help="Path to the configuration file")
    
    # Parse all command line arguments.
    args = parser.parse_args()
    
    # Convert the provided directory string into a Path object.
    path = Path(args.path)
    
    # Provide feedback to the user about the selected directory.
    print(f"The directory is now selected as: {path.name}")
    
    # Check if the directory exists; if not, exit with an error message.
    if not path.exists():
        print("The entered directory dose not exists")
        raise SystemExit(1)
    
    # Return a dictionary of options to be used by the program.
    return {
        "path": path,
        "dry-run": args.dry_run,
        "config":  args.config
    }

def load_config(config_path):
    """
    Loads and parses a JSON configuration file.
    
    Args:
        config_path (str): Path to the JSON configuration file.
    
    Returns:
        dict: A dictionary with file extension groups, where keys are category names
              and values are lists of extensions.
    
    Raises:
        FileNotFoundError: If the configuration file does not exist.
        JSONDecodeError: If the configuration file contains invalid JSON.
    """
    # Open the configuration file and load its JSON content.
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def file_organizer(path, dry_run, config):
    """
    Organizes files in a directory by moving them into categorized folders based on their extensions.
    
    This function performs the following steps:
        1. Loads extension mappings from the configuration file.
        2. Iterates over all files in the specified directory.
        3. Checks each file's extension against configured groups.
        4. Moves the file into the matching category folder, creating the folder if necessary.
        5. If no match is found, moves the file into an 'Others' folder.
    
    Args:
        path (str): The directory path where files are to be organized.
        dry_run (bool): If True, displays the actions without moving files.
        config (str): Path to the JSON configuration file with extension mappings.
    
    Example:
        >>> file_organizer('/path/to/directory', False, 'config.json')
        'example.pdf' is identified as a Document and moved accordingly.
    """
    # Load the extension groups from the configuration file.
    extension_groups = load_config(config)
    
    # Convert the provided path string to a Path object for easier manipulation.
    directory = Path(path)
    
    # Create the 'Others' folder (if not in dry-run) to hold files that do not match any category.
    if not dry_run:
        others = directory / "Others"
        os.makedirs(others, exist_ok=True)
    else:
        print('[DRY RUN] Others folder will be created to move uncategorized formats into itself')
    
    # Iterate over all items in the directory.
    # Converting the iterator to a list safeguards against modifying the directory during iteration.
    for content in list(directory.iterdir()):
        # Process only files.
        if content.is_file():
            moved = False  # Flag to track if the current file has been categorized/moved.
            # Iterate through each category and its associated list of extensions.
            for cat, exts in extension_groups.items():
                # If the current file's extension matches one of the extensions in the category:
                if content.suffix in exts:
                    target_dir = directory / cat
                    if dry_run:
                        # In dry run mode, just report what would happen.
                        print(f'{cat} folder created')
                        print(f'[DRY RUN] {content.name} will be moved into {target_dir}')
                    else:
                        # Create the target directory if it does not exist.
                        os.makedirs(target_dir, exist_ok=True)
                        # Move the file to its respective category folder.
                        shutil.move(str(content), str(target_dir))
                        print(f"'{content.name}' is one of {cat} so it will move to {target_dir}")
                    moved = True  # Mark the file as processed.
                    break  # Exit the loop once a matching category is found.
            # If no category matched the file's extension, move it to the 'Others' folder.
            if not moved:
                if dry_run:
                    print(f'[DRY RUN] {content.name} will be moved into Others')
                else:
                    shutil.move(str(content), str(others))
                    print(f"'{content.name}' did not match any group so it will move to {others}")

def main():
    """
    Main entry point for the script.
    
    This function retrieves the command line options, then calls the file organizer
    function to process and organize files based on their extensions.
    """
    # Obtain command-line options and validated directory path.
    options = define_options()
    # Organize files using the provided path, dry-run flag, and configuration file.
    file_organizer(options['path'], options['dry-run'], options['config'])

if __name__ == '__main__':
    # If the script is executed directly, run the main function.
    main()