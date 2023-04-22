#Find a zip archive with a name "Photos###.zip" and extract it to the tmp directory
#Find all the photos in the tmp directory
#Combine the photos into a PDF using img2pdf
#Delete the tmp directory
#Delete the zip archive
#Put the PDF in the downloads directory

import os
import zipfile
import glob
import shutil
import img2pdf

#Find all the zip archives in the downloads directory
zip_files = glob.glob(os.path.expanduser("~/Downloads/Photos-*.zip"))

#If there are no zip archives, exit
if len(zip_files) == 0:
    exit()

for zip_file in zip_files:
    #Extract the zip archive
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall("tmp")

    #Find all the photos and reverse the list
    photos = glob.glob("tmp/*.jpg")
    #sort the photos by name
    photos.sort()

    #Combine the photos into a PDF
    with open("Photos.pdf", "wb") as f:
        f.write(img2pdf.convert(photos, rotation=img2pdf.Rotation.ifvalid))

    #Delete all files in the tmp directory
    shutil.rmtree("tmp")

    #Make a new tmp directory
    os.mkdir("tmp")

    #Delete the zip archive
    os.remove(zip_file)

    #Find a name Photos###.pdf that doesn't exist
    i = 0
    while os.path.exists(os.path.expanduser("~/Downloads/Photos-{}.pdf".format(i))):
        i += 1

    #Move the PDF to the downloads directory
    shutil.move("Photos.pdf", os.path.expanduser("~/Downloads/Photos-{}.pdf".format(i)))
