from PIL import Image
from django.core.exceptions import ValidationError



def validate_team_photo(image):
    # Open the uploaded image
    img = Image.open(image)

    width, height = img.size

    # 1. Validate aspect ratio (must be 1:1)
    if width != height:
        raise ValidationError("Image must have a 1:1 aspect ratio (square).")

    # 2. Validate minimum intrinsic size
    if width < 600 or height < 600:
        raise ValidationError("Image must be at least 600×600 pixels.")

    # Optional: Validate maximum file size (example: 2 MB)
    max_size = 2 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError("Image file size must not exceed 2 MB.")