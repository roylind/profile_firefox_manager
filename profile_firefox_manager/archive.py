import os
import zipfile


def folder_to_archive(path_archive: str, path_folder: str):
    if path_archive[-1] == "*":
        path_archive = path_archive[0:len(path_archive)-1] + os.path.basename(path_folder) + ".zip"

    zip_archive = zipfile.ZipFile(path_archive, 'w')

    for folder, _, files in os.walk(path_folder):
        print(folder)
        for file in files:
            zip_archive.write(os.path.join(folder, file),
                              os.path.relpath(os.path.join(folder, file), os.path.dirname(path_folder)),
                              compress_type=zipfile.ZIP_DEFLATED)

    zip_archive.close()


def archive_to_folder(path_archive: str, path_extract: str):
    with zipfile.ZipFile(path_archive, 'r') as zfile:
        zfile.extractall(path_extract)
