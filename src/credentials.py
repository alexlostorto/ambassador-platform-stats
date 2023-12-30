# Relative files
import os

# Environment variables
from dotenv import load_dotenv


def getCredentials():
    load_dotenv()
    token = os.getenv('TOKEN')
    dialog = os.getenv('DIALOG')

    if token is None:
        print("[ERROR] TOKEN is not set")
        exit(1)

    if dialog is None:
        print("[ERROR] DIALOG is not set")
        exit(1)

    return token, dialog
