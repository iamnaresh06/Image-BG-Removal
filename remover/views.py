from django.conf import settings
import os
from rembg import remove

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


def remove_background(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']

        # Define paths for uploaded and processed images
        upload_folder = settings.MEDIA_ROOT / 'uploaded_images'
        processed_folder = settings.MEDIA_ROOT / 'processed_images'

        # Ensure directories exist
        os.makedirs(upload_folder, exist_ok=True)
        os.makedirs(processed_folder, exist_ok=True)

        input_path = upload_folder / image_file.name
        output_path = processed_folder / f"processed_{image_file.name}"

        # Save uploaded file
        with open(input_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        # Process image using rembg
        with open(input_path, 'rb') as inp_file:
            input_image = inp_file.read()
            output_image = remove(input_image)

        with open(output_path, 'wb') as out_file:
            out_file.write(output_image)

        # Construct URLs for displaying in template
        output_url = settings.MEDIA_URL + f"processed_images/processed_{image_file.name}"

        return render(request, 'result.html', {'output_image': output_url})

    return render(request, 'index.html', {'error': 'Invalid file upload'})
