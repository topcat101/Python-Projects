import os
import boto3
import shutil
import time
import glob

Destination = ("C:/Users/Thomas/Desktop/CV Upload/CV-NewLocation/")
Doc_File = ("C:/Users/Thomas/Desktop/CV Upload/")
# Root_Path = input('') #Specify the root path (C:, D:, E:, etc, etc)
Root_Path = ('C:') #For the time of testing
s3 = boto3.resource('s3')
Client = boto3.client('s3')


def Copy_Paste_CV(Doc_File_Location, Root_Path):
    # This function copies the most recently created .docx file from the specified location to a destination.
    if (Root_Path in Doc_File_Location[:2]):
        try:
            List_Files = glob.glob(Doc_File_Location + "*.docx")
            Last_File_Created = max(List_Files, key = os.path.getctime)
            # This gets the most recently added file in the folder.
        except:
            print("No .docx files found in the specified directory.")

        try:
            Source = (Last_File_Created)
            shutil.copy(Source, Destination)
            #Copies and Pastes the file in a desired location. Staging this to be ready for when its uploaded.
        except:
            print("Something went wrong")
    else:
        print("Something has went wrong somewhere")


def upload_file_to_s3(bucket):
    # Placeholder for S3 upload logic
    # This function should handle the upload of the file to the specified S3 bucket.
    s3.upload_file(Destination + "*.docx")


def List_Folder_And_Files(bucket_name):
    List_Of_objects = Client.list_objects_v2(Bucket=bucket_name)

    for List_objects in List_Of_objects['Contents']:
        print('File/ Folder:', List_objects['Key'], 'Date&Time:', List_objects['LastModified'])



docx_files = glob.glob(os.path.join(Destination, "*.docx"))
# Get current files with *.docx names within the current folder.

if __name__ == "__main__":
    if docx_files:
        for file in docx_files:
            while True:
                files = os.path.basename(file)
                print(f"{files} exists in the folder, deleting it to ensure a clean slate.")
                os.remove(file)
                break
            # If the file exists, it will delete it to ensure a clean slate for copying files.
        exit()
    
    else:
        Copy_Paste_CV(Doc_File, Root_Path)
        print("No files exist, proceeding to copy file to the folder.")
        # If the destination folder does not exist, it will create it and copy the files.

        New_docx_file = glob.glob(os.path.join(Destination, "*.docx"))
        # Creating new variable of the new document created successfull.
        for new_file in New_docx_file:
            New_File = os.path.basename(new_file)



    if New_File:
        s3.Bucket('duobucketforsharingproject').upload_file(Filename=Destination + New_File, Key=New_File)
        List_Folder_And_Files("duobucketforsharingproject")

    else:
        print("No files to upload to S3 bucket.")








