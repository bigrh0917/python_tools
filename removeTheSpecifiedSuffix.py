import os

# The directory where the file with the suffix needs to be deleted.
directory = "I:\\Java\\学习资料\\黑马Java2022在线就业课V12.5版本\\03阶段三：JavaWeb\day05-Mybatis\\04-讲义\\assets"  # Replace with your directory path

# Specify the suffix to be deleted.
suffix_to_remove = "【瑞客论坛 www.ruike1.com】"

# Document type
document_type = '.png'

# Loop over files in a directory
for filename in os.listdir(directory):
    if filename.endswith(f"{suffix_to_remove}{document_type}"):
        # Construct a new filename, removing the specified suffix part
        new_filename = filename.replace(f"{suffix_to_remove}{document_type}", f"{document_type}")

        # Build the complete old file path and new file path
        old_filepath = os.path.join(directory, filename)
        new_filepath = os.path.join(directory, new_filename)

        # Rename a file
        os.rename(old_filepath, new_filepath)
        print(f"rename: {old_filepath} to {new_filepath}")
