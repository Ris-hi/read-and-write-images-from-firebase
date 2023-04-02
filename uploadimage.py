from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import firebase_admin
from firebase_admin import credentials, storage

def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)

        # Initialize Firebase credentials and upload the file to Firebase Storage
        # firebase credentials is to be put in here 
        cred = credentials.Certificate("path/to/firebase/credentials.json")
        #change the name acc to ur system
        firebase_admin.initialize_app(cred, {'storageBucket': '<your-bucket-name>'})
        bucket = storage.bucket()
        blob = bucket.blob(filename)
        with open(uploaded_file_url[1:], 'rb') as file:
            blob.upload_from_file(file)

        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url
        })

    return render(request, 'upload.html')
