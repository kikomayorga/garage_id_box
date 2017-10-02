import time ## Delays
from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

fecha = time.strftime('%m-%d-%Y')

from pydrive.drive import GoogleDrive

# Create GoogleDrive instance with authenticated GoogleAuth instance.
drive = GoogleDrive(gauth)

folder_metadata = {'title' : str(fecha),"parents":  [{"id": "0B1zkhucfn1WKTUtlTEJwci0wSmM"}],  'mimeType' : 'application/vnd.google-apps.folder'}
folder = drive.CreateFile(folder_metadata)
folder.Upload()

file1 = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": "0B1zkhucfn1WKTUtlTEJwci0wSmM"}]})
file1.SetContentFile('Data/'+str(fecha)+'.svg')
file1.Upload()

file2 = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": "0B1zkhucfn1WKTUtlTEJwci0wSmM"}]})
file2.SetContentFile('Data/'+str(fecha)+'.txt')
file2.Upload()
