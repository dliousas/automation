import os
import shutil
import re
import platform

# Define the folder path for downloads and the destination path
if platform.system() == "Darwin": # macOS or Linux
    downloads_path = os.path.expanduser("~/Downloads")
    destination_path = os.path.expanduser("~/Library/CloudStorage/OneDrive-UniversityofMassachusetts/Spring_2023")
    jobs_path = os.path.expanduser("~/Library/CloudStorage/OneDrive-UniversityofMassachusetts/Jobs")
else: 
    # Windows
    downloads_path = os.path.join(os.getenv("USERPROFILE"), "Downloads")
    destination_path = os.path.join(os.getenv("USERPROFILE"), "OneDrive - University of Massachusetts", "Spring_2023")
    jobs_path = os.path.join(os.getenv("USERPROFILE"), "OneDrive - University of Massachusetts", "Jobs")

# Define the mapping of words/numbers to new names and their corresponding folder names
mapping = {
    "383": "CS383",
    "354": "MIE354",
    "344": "MIE344",
    "313": "MIE313",
    "351": "ENGIN351H",
    "greek": "Greek",
    "rocket": "Rocket"
}

# Loop through all files in the downloads folder
for filename in os.listdir(downloads_path):
    # Ignore subfolders
    if os.path.isdir(os.path.join(downloads_path, filename)):
        continue

    # Replace spaces with underscores in the filename
    new_filename = filename.replace(" ", "_")
    #If the filename contains _job.
    if "_job." in new_filename:
        # Get the company name from the filename, which is from the start of the filename to the first underscore
        company_name = new_filename.split("_")[0]

        # Delete "_job" from the filename
        new_filename = new_filename.replace("_job", "")
        
        # Create a new folder for the company if it doesn't exist
        if not os.path.exists(os.path.join(jobs_path, company_name)):
            os.makedirs(os.path.join(jobs_path, company_name))
        # Replace the company name with the string "Liousas-Demetri"
        new_filename = new_filename.replace(company_name, "Liousas-Demetri")

        # Define a function to find the lowest version number for the file name that doesn't exist
        def get_valid_file_name(init_path):
            #Split path into path and extension
            path, ext = os.path.splitext(init_path)
            def get_valid_file_name_helper(num):
                # Check if file path+num+ext exists
                full_path = path + "_" + str(num).zfill(2) + ext
                if not os.path.exists(full_path):
                    #return path with 5 digits using leading zeros
                    return full_path
                # If file exists, increment num and try again
                return get_valid_file_name_helper(num+1)
            return get_valid_file_name_helper(0)
        
        # Get the valid file name
        new_filename = get_valid_file_name(os.path.join(jobs_path, company_name, new_filename))
        
        # Move the file to the company folder
        shutil.move(os.path.join(downloads_path, filename), new_filename)
        print(f"Moved {filename} to {new_filename}")

        continue

    # Check if the filename contains any of the words/numbers in the mapping
    for key, value in mapping.items():
        if key.lower() in new_filename.lower():
            # Replace the word/number with the new name, only if there is an underscore before the word/number
            #new_filename = re.sub(re.escape(key), value, new_filename, flags=re.IGNORECASE)
            new_filename = re.sub(rf'_{re.escape(key)}', f"_{value}", new_filename, flags=re.IGNORECASE)

            # Check if the new filename starts with 'L' followed by a number using regex
            if re.match(r'^L\d+', new_filename):
                # Add "Lectures" folder to the folder path
                value = os.path.join(value, "Lectures")
            #Check if the new filename starts with 'SP' followed by a number using regex
            elif re.match(r'^SP\d+', new_filename):
                # Add "Solutions" folder to the folder path
                value = os.path.join(value, "Special_Problems")
            #Check if the new filename starts with 'P' followed by a number using regex
            elif re.match(r'^P\d+', new_filename):
                # Add "Practice" folder to the folder path
                value = os.path.join(value, "Projects")
            #Check if the new filename starts with Q followed by a number using regex
            elif re.match(r'^Q\d+', new_filename):
                # Add "Quizzes" folder to the folder path
                value = os.path.join(value, "Quizzes")
            #Check if the new filename starts with 'HW' followed by a number using regex
            elif re.match(r'^HW\d+', new_filename):
                # Add "HW{number}" folder to the folder path
                match = re.search(r'^HW(\d+)', new_filename)
                hw_number = match.group(1)
                value = os.path.join(value, f"HW{hw_number}")
            #Check if the new filename starts with 'E' followed by a number using regex
            elif re.match(r'^E\d+', new_filename):
                # Add "Exams" folder to the folder path
                match = re.search(r'^E(\d+)', new_filename)
                exam_number = match.group(1)
                value = os.path.join(value, f"Exam{exam_number}")

            # Move the file to the corresponding folder
            folder_path = os.path.join(destination_path, value)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
            shutil.move(os.path.join(downloads_path, filename), os.path.join(folder_path, new_filename))
            print(f"Moved {filename} to {os.path.join(folder_path, new_filename)}")

# Print message when done organizing files
print("Finished organizing files!")
