import os
import fnmatch

# The directory containing .py files
source_dir = os.path.join(os.getcwd(), 'services')

# The target file for concatenation
target_file_path = os.path.join(os.getcwd(), 'all_services.py')

# Open the target file in write mode
with open(target_file_path, 'w') as target_file:

    # Iterate through all files in the source directory
    for root, dirs, files in os.walk(source_dir):
        for file in files:

            # If the file is a .py file and not 'service_io.py'
            if fnmatch.fnmatch(file, '*.py') and file != 'service.py' and file != 'input_config.py':

                # Open the source .py file in read mode
                with open(os.path.join(root, file), 'r') as source_file:

                    # Skip the first 8 lines, then write remaining lines to target file
                    lines = source_file.readlines()[12:]
                    target_file.writelines(lines)

                    # Add a newline to separate each file content
                    target_file.write('\n')