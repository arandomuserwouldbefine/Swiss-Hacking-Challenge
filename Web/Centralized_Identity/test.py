import os

def replace_spaces_in_png_filenames():
    # Get the current working directory
    current_directory = os.getcwd()
    
    # Iterate through each file in the directory
    for filename in os.listdir(current_directory):
        # Check if the file is a PNG file and contains spaces in the name
        if filename.endswith(".png") and ' ' in filename:
            # Create the new filename by replacing spaces with underscores
            new_filename = filename.replace(' ', '_')
            
            # Get the full path for the old and new filenames
            old_filepath = os.path.join(current_directory, filename)
            new_filepath = os.path.join(current_directory, new_filename)
            
            # Rename the file
            os.rename(old_filepath, new_filepath)
            
            # Print a message indicating the file has been renamed
            print(f'Renamed: {filename} to {new_filename}')

# Run the function
replace_spaces_in_png_filenames()
