import logging

from .IO_module import validate_filename, file_exists
from .supabase_module import uploadFile, insertJob

logging.getLogger("httpx").setLevel(logging.CRITICAL)


def loadJob(filename: str):
    # if filename is None:
    #     filename = validate_filename(input("Enter a filename: "))

    # Insert Job
    if file_exists(filename, "./"):
        print("Loading job: " + filename)
        id = insertJob()
        print("Job id: " + id)
        uploadFile(filename, id, 'Job/')
        print("Job loaded successfully")
    else:
        print(f"The file '" + filename + "' does not exist.")
