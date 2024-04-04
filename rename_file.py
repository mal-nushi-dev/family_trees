import os
import re
import glob


def rename_file(family_name):
    """
    Renames a family's Genealogy csv file by removing the unique
        identifier after the family name.

    The function searches for files in the current directory that match
        the pattern '{family_name}-Genealogy-*.csv'.
    It then renames these files to '{family_name}-Genealogy.csv', overwriting
        any existing files with the same name.

    Parameters:
    family_name (str): The family name to search for in the file names.

    Returns:
    None

    Raises:
    OSError: If there is an error renaming the file.
    """
    # Pattern to match a specific family's Genealogy csv file
    pattern = f'{family_name}-Genealogy-*.csv'

    # Search for files in the directory matching that file pattern
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
    rename_file(family_name="Nushi")
