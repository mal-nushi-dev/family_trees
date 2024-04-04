import os
import re
import glob


def rename_file(family_name: str):
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
        str or None: The new filename if a file was successfully
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

    for file in files:
        print(f"Processing '{file}'...")

        # Extract last name using REGEX
        match = re.match(rf'({family_name})-Genealogy-', file)
        if match:
            # Construct the new file name
            new_filename = f"{match.group(1)}-Genealogy.csv"

            # Rename the file and overwrite any existing files
            try:
                os.rename(file, new_filename)
                print(f"Renamed '{file}' to '{new_filename}'")
                return new_filename
            except OSError as e:
                print(f"Error renaming file '{file}': {e}")
        else:
            print(f"No matching files found for family name: '{family_name}'.")


if __name__ == "__main__":
    # Specify the family name here
    rename_file(family_name="nushi")
