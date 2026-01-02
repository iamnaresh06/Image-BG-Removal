from django.conf import settings
import os
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from PIL import Image
import io
from rembg import remove, new_session

# Pre-initialize session with explicit model to speed up requests
REMBG_SESSION = new_session("u2net")

def perform_bg_removal(image_data):
    return remove(image_data, session=REMBG_SESSION)

def index(request):
    return render(request, 'index.html')


def remove_background(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        refine_edges = request.POST.get('refine_edges') == 'on'

        fs = FileSystemStorage()
        
        # Save uploaded file using Django's storage to handle naming/conflicts
        input_name = fs.save(f'uploaded_images/{image_file.name}', image_file)
        input_path = fs.path(input_name)
        
        # Determine output filename
        base_name = os.path.splitext(os.path.basename(input_name))[0]
        output_name = f"processed_images/processed_{base_name}.png"
        
        # Process image
        with open(input_path, 'rb') as inp_file:
            input_image_data = inp_file.read()
            
            if refine_edges:
                output_image_data = remove(
                    input_image_data, 
                    session=REMBG_SESSION,
                    alpha_matting=True,
                    alpha_matting_foreground_threshold=240,
                    alpha_matting_background_threshold=10,
                    alpha_matting_erode_size=10
                )
            else:
                output_image_data = perform_bg_removal(input_image_data)

        # Save processed file
        if fs.exists(output_name):
            fs.delete(output_name)
        processed_name = fs.save(output_name, ContentFile(output_image_data))

        # Generate URLs and ensure forward slashes for the browser
        original_url = fs.url(input_name).replace('\\', '/')
        output_url = fs.url(processed_name).replace('\\', '/')

        context = {
            'output_image': output_url,
            'original_image': original_url,
            'filename': os.path.basename(processed_name)
        }
        return render(request, 'result.html', context)

    return render(request, 'index.html', {'error': 'Invalid file upload'})


def download_file(request):
    filename = request.GET.get('filename')
    file_format = request.GET.get('format', 'png').lower()
    bg_color = request.GET.get('color', 'transparent')

    if not filename:
        return HttpResponse("Filename not provided", status=400)

    file_path = settings.MEDIA_ROOT / 'processed_images' / filename
    if not os.path.exists(file_path):
        return HttpResponse("File not found", status=404)

    try:
        img = Image.open(file_path).convert("RGBA")

        # Apply background color if not transparent
        if bg_color != 'transparent':
            # Create a solid color background
            background = Image.new("RGBA", img.size, bg_color)
            # Composite image over background
            final_img = Image.alpha_composite(background, img)
            img = final_img

        # Format handling
        output_io = io.BytesIO()
        
        if file_format == 'jpg' or file_format == 'jpeg':
            # JPEG does not support transparency, convert to RGB
            img = img.convert("RGB")
            img.save(output_io, format='JPEG', quality=95)
            mime_type = 'image/jpeg'
            download_name = f"{filename.split('.')[0]}.jpg"
        elif file_format == 'webp':
            img.save(output_io, format='WEBP', quality=95)
            mime_type = 'image/webp'
            download_name = f"{filename.split('.')[0]}.webp"
        else:
            # Default to PNG
            img.save(output_io, format='PNG')
            mime_type = 'image/png'
            download_name = f"{filename.split('.')[0]}.png"

        output_io.seek(0)
        response = FileResponse(output_io, content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename="{download_name}"'
        return response

    except Exception as e:
        return HttpResponse(f"Error processing image: {str(e)}", status=500)
