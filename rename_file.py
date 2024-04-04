import os
import glob
from typing import Optional


def rename_file(family_name: str) -> Optional[str]:
    """
    Searches for and renames a CSV file associated with a family's genealogy.

    This function looks for CSV files in the current directory with a name
    following the pattern '{family_name}-Genealogy-*.csv'. It renames the
    first matching file to '{family_name}-Genealogy.csv', overwriting an
    existing file with that name. The function is case-insensitive to the
    family name but will capitalize it in the new filename.

    Parameters:
        family_name (str): The base name of the family to be used in
                           searching and renaming the file.

    Returns:
        Optional[str]: The new filename if a file was successfully
                       renamed, None otherwise.

    Raises:
        OSError: If the file cannot be renamed due to system-related errors
                 such as permission issues or the file being in use.

    Note:
        This function will rename the first file that matches the pattern
        and stop. If multiple files match, subsequent files
        will not be processed.
    """
    # Capitalize the family name to ensure consistent file matching
    family_name = family_name.capitalize()

    # Pattern to match a specific family's Genealogy csv file
    pattern = f'{family_name}-Genealogy-*.csv'

    # Use glob to find all files in the current dir that match the pattern
    files = glob.glob(pattern)

    if not files:
        print(f"No matching files found for family name: '{family_name}'.")
        return None

    # Only processing the first matching file
    file = files[0]
    print(f"Processing '{file}'...")

    # Construct the new file name
    new_filename = f"{family_name}-Genealogy.csv"

    # Rename the file and overwrite any existing files
    try:
        os.rename(file, new_filename)
        print(f"Renamed '{file}' to '{new_filename}'")
        return new_filename
    except OSError as e:
        print(f"Error renaming file '{file}': {e}")
        raise


if __name__ == "__main__":
    # Specify the family name here
    renamed_file = rename_file(family_name="nushi")
    if renamed_file:
        print(f"File successfully renamed to: {renamed_file}")
    else:
        print("No file was renamed.")
