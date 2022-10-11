import os
from Google import Create_Service

from Apple import logIn



# Deckares the applications scope
SCOPES =  ['https://www.googleapis.com/auth/photoslibrary',
          'https://www.googleapis.com/auth/photoslibrary.sharing']
API_VERSION = "v1"
API_NAME= "photosLibrary"


CLIENT_FILE = "credentials.json" # specifies locaiton of client ID

############################# Connection Functions #############################

def getGoogleAuthenticatedService(): # Modified
    # Calls Create_Service function in Google.py
    return Create_Service(CLIENT_FILE ,API_NAME, API_VERSION, SCOPES) 


def getiCloudConnection():
    # Calls logIn funciton in Apple.py
    return logIn()

############################# Connection Functions #############################


def filesToTransferGoogle(icloud, googlePhotos):
    toTransfer = []
    for photo in googlePhotos:
        if photo not in icloud:
            toTransfer.append(photo)
    print(f'There are {len(toTransfer)} files to upload')
    



def iCloudPhotos(connection):
    allPhotos = []
    for photo in connection.photos.albums['All Photos']:
        allPhotos.append(photo.filename)
    return allPhotos


def googlePhotos(connection):
    allPhotos = []

    response = connection.mediaItems().list(pageSize=100).execute()

    lst_medias = response.get('mediaItems')
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        response = connection.mediaItems().list(
            pageSize=100, 
            pageToken=nextPageToken
        ).execute()

        lst_medias.extend(response.get('mediaItems'))
        nextPageToken = response.get('nextPageToken')


    for photo in lst_medias:
        allPhotos.append(photo.get('filename'))


    return allPhotos


if __name__ == '__main__':
    transferLocation = input("\nWhere do you want to transfer from (Google or iCloud)?: ").lower()
    deliveryLocation = input("\nWhere do you want to deliver to (Google or iCloud)?: ").lower()

    # Defines list of all services
    services = ("google", "icloud")

    # Data validation to ensure transferlocation is valid
    while transferLocation not in services:
        print("\nInvalid input. Please try again")
        transferLocation = input("Where do you want to transfer from (Google or iCloud): ").lower()

    # Data validation to make sure that delivery location is valid and is not equal to transferLocation
    while deliveryLocation == transferLocation:
        print("\nDelivery location can not be same as Transfer Location")
        deliveryLocation = input("\nWhere do you want to deliver to (Google or iCloud)?: ").lower()
        while deliveryLocation not in services:
            print("\nInvalid input. Please try again")
            deliveryLocation = input("\nWhere do you want to deliver to (Google or iCloud)?: ").lower()



    match transferLocation:
        case "google":
            googlePhotosConnection = getGoogleAuthenticatedService()
        case "icloud":
            iCloudConnection = getiCloudConnection()

    match deliveryLocation:
        case "google":
            googlePhotosConnection = getGoogleAuthenticatedService()
        case "icloud":
            iCloudConnection = getiCloudConnection()


    # TRANSFER LOGIC:
    # The application will get a list of every file name in the delivery location
    # Then it will get a list of every file name in the transfer locaiton
    # It will run the transfer location file names and compare it to delivery location file names
    # Any file names that dont match will be transfered
    if transferLocation == "google":
        iCloudAllPhotos = iCloudPhotos(iCloudConnection)
        googleAllPhotos = googlePhotos(googlePhotosConnection)
        filesToTransferGoogle(iCloudAllPhotos, googleAllPhotos)
    
    