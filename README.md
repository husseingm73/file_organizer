# File Organizer

A simple file organization utility that categorizes and moves files into appropriate folders based on their extensions.

## Description

This script provides functionality to organize files in a specified directory by moving them into categorized folders based on their file extensions. It supports both actual file operations and dry runs for testing purposes.

## Features

- **Categories Files**: Moves files into folders based on their extensions.
- **Dry Run Mode**: Simulates file organization without making any changes.
- **Custom Configuration**: Uses a JSON configuration file to define file extension mappings.
- **Automatic Folder Creation**: Creates category folders automatically if they don't exist.
- **Detailed Output**: Provides detailed feedback on file operations.

## Configuration

The script expects a JSON configuration file that defines file extension mappings to category folders. For example:

```json
{
    "Documents": [".pdf", ".doc", ".txt"],
    "Images": [".jpg", ".png", ".gif"]
}
```

## Dependencies
This was created using standard Python libraries—nothing too complicated! Just make sure you have Python installed on your system, and you’re all set to go!

## Usage

To use the script, run the following command:

```sh
python app.py -p /path/to/directory --dry-run
python app.py -p /path/to/directory -c custom_config.json
```

### Command Line Arguments

- `-p`, `--path`: Target directory path which organization will happen. Defaults to the current working directory.
- `--dry-run`: Perform a dry run without moving files to ensure functionality.
- `-c`, `--config`: Path to the configuration file. Defaults to `config.json`.

## Example

```sh
python app.py -p /path/to/directory --dry-run
```

This command will simulate organizing files in the specified directory without actually moving any files.

## Notes

- Moves unrecognized file types to an 'Others' folder.
- Provides detailed output of file operations.
- Supports dry run mode for testing.

## License

This project is licensed under the MIT License.

## Author

Hussein Ghate
