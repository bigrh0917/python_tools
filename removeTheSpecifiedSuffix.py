import os

# The directory where the file with the suffix needs to be deleted.
directory = "E:\\java\\牛客论坛项目"  # Replace with your directory path

# Specify the suffix to be removed.
suffix_to_remove = "【瑞客论 坛 www.ruike1.com】"

# Document type
document_type = ['.wmv', '.png', '.txt', '.pdf','.zip']

# Function to recursively process files in directories
def process_directory(dir_path):
    # Loop over all entries in the directory
    for entry in os.listdir(dir_path):
        # Build the full path
        full_path = os.path.join(dir_path, entry)
        
        # If it's a directory, recursively process it
        if os.path.isdir(full_path):
            process_directory(full_path)
        # If it's a file, check if it needs to be renamed
        elif os.path.isfile(full_path):
            for suffix in document_type:
                if entry.endswith(f"{suffix_to_remove}{suffix}"):
                    # Construct a new filename, removing the specified suffix part
                    new_filename = entry.replace(f"{suffix_to_remove}{suffix}", f"{suffix}")

                    # Build the new file path
                    new_filepath = os.path.join(dir_path, new_filename)

                    # Rename the file
                    os.rename(full_path, new_filepath)
                    print(f"rename: {full_path} to {new_filepath}")
                    break  # Once renamed, no need to check other suffixes

# Start processing from the root directory
process_directory(directory)
