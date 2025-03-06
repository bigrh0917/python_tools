import os

# The directory where the file with the suffix needs to be deleted.
directory = "C:\\Users\\Administrator\\Desktop\\293-100617601-专栏课-黄佳-LangChain 实战课（完结）"  # Replace with your directory path

# Specify the suffix to be deleted.
suffix_to_remove = "[天下无鱼][shikey.com]"

# Document type
document_type = ['.wmv', '.png', '.txt', '.pdf','.zip','.md','.mp3']

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
