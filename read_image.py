import firebase_admin
from firebase_admin import credentials, storage
from django.shortcuts import render

# Initialize Firebase SDK
cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'your-bucket-name'})

# Get a reference to the Firebase storage bucket
bucket = storage.bucket()

def index(request):
    # Get a list of all images in the Firebase storage bucket
    blob_list = list(bucket.list_blobs())

    # Filter the list to only include image files
    image_list = [blob for blob in blob_list if blob.content_type.startswith('image/')]

    # Get the download URLs for the images
    image_urls = [blob.generate_signed_url(expiration=datetime.timedelta(days=1), method='GET') for blob in image_list]

    # Render the index.html template with the image URLs
    return render(request, 'index.html', {'image_urls': image_urls})
