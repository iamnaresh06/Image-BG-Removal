from django.conf import settings
import os
from rembg import remove, new_session
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from PIL import Image
import io

def index(request):
    return render(request, 'index.html')


def remove_background(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        refine_edges = request.POST.get('refine_edges') == 'on'

        # Define paths
        upload_folder = settings.MEDIA_ROOT / 'uploaded_images'
        processed_folder = settings.MEDIA_ROOT / 'processed_images'

        # Ensure directories exist
        os.makedirs(upload_folder, exist_ok=True)
        os.makedirs(processed_folder, exist_ok=True)

        input_path = upload_folder / image_file.name
        output_filename = f"processed_{image_file.name.split('.')[0]}.png"
        output_path = processed_folder / output_filename

        # Save uploaded file
        with open(input_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        # Process image
        with open(input_path, 'rb') as inp_file:
            input_image = inp_file.read()
            
            # Use basic or advanced removal based on user choice
            if refine_edges:
                # Alpha matting for finer edge details (hair, etc)
                output_image = remove(
                    input_image, 
                    alpha_matting=True,
                    alpha_matting_foreground_threshold=240,
                    alpha_matting_background_threshold=10,
                    alpha_matting_erode_size=10
                )
            else:
                output_image = remove(input_image)

        with open(output_path, 'wb') as out_file:
            out_file.write(output_image)

        # URLs
        original_url = settings.MEDIA_URL + f"uploaded_images/{image_file.name}"
        output_url = settings.MEDIA_URL + f"processed_images/{output_filename}"

        context = {
            'output_image': output_url,
            'original_image': original_url,
            'filename': output_filename
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
