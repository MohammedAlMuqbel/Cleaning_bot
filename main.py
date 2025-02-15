import os
import argparse

parser=argparse.ArgumentParser(
    description="Clean up directory and put files into acoording folders"

)

parser.add_argument(
    "--path",
    type=str,
    default=".",
    help="Directory path of the cleaned up directory"

)

args=parser.parse_args()
path=args.path

print(f"Cleaning up directory {path}")

# get all files from the given directory
dir_content=os.listdir(path)
path_dir_content=[os.path.join(path,doc) for doc in dir_content]
docs=[doc for doc in path_dir_content if os.path.isfile(doc)]
folders=[folder for folder in path_dir_content if os.path.isdir(folder)]
moved=0
created_folder=[]
print(f"Cleaning up{len(docs)} of {len(dir_content)} elements")

# go through all files and move them into according folders
for doc in docs:
    # separate name from file extension
    full_doc_path,filetype=os.path.splitext(doc)
    doc_path=os.path.dirname(full_doc_path)
    doc_name=os.path.basename(full_doc_path)

    # skip this python file when it is in the directory
    if doc_name=="main" or doc_name.startswith('.'):
        continue

    # get the subfolder name and create folder if not exist
    subfolder_path=os.path.join(path,filetype[1:].lower())  # .txt

    if subfolder_path not in folders and subfolder_path not in created_folder:
        try:
            os.mkdir(os.path.join(path,subfolder_path))
            created_folder.append(subfolder_path)
            print(f"Folder {subfolder_path} created")
        except FileExistsError as err:
            print(f"Folder already exist at{subfolder_path}...{err}")

    # get the new folder path and move the file
    new_doc_path=os.path.join(subfolder_path,doc_name)+filetype
    os.rename(doc,new_doc_path)
    moved+=1

    print(f"Moved file {doc} to {new_doc_path}")

print(f" Renamed {moved} of {len(docs)} files")