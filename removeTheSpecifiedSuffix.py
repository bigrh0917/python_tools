import os

# The directory where the file with the suffix needs to be deleted.
directory = "E:\\05阶段五：项目实战-瑞吉外卖\\05-瑞吉外卖-项目优化\\03-讲义\\瑞吉外卖项目优化-day02\\assets"  # Replace with your directory path

# Specify the suffix to be deleted.
suffix_to_remove = "【瑞客论坛 www.ruike1.com】"

# Document type
document_type = ['.wmv', '.png', '.txt', '.pdf','.zip']

# Loop over files in a directory
for filename in os.listdir(directory):
    for suffix in document_type:
        if filename.endswith(f"{suffix_to_remove}{suffix}"):
            # Construct a new filename, removing the specified suffix part
            new_filename = filename.replace(f"{suffix_to_remove}{suffix}", f"{suffix}")

            # Build the complete old file path and new file path
            old_filepath = os.path.join(directory, filename)
            new_filepath = os.path.join(directory, new_filename)

            # Rename a file
            os.rename(old_filepath, new_filepath)
            print(f"rename: {old_filepath} to {new_filepath}")
