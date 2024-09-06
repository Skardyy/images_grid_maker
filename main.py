import os
from PIL import Image
import math

def closest_grid_dimensions(number, aspect_ratio):
    best_cols, best_rows = 1, number  # Initialize with the worst case
    min_aspect_diff = float('inf')  # Initialize with an infinitely large difference
    
    # Iterate over possible number of columns from 1 to the number of items
    for cols in range(1, number + 1):
        # Calculate the corresponding number of rows needed for the given number of columns
        rows = math.ceil(number / cols)
        
        # Calculate the actual aspect ratio for these dimensions
        actual_aspect_ratio = cols / rows
        aspect_diff = abs(actual_aspect_ratio - aspect_ratio)  # Calculate the difference from the desired aspect ratio
        
        # If the current aspect ratio is closer to the desired aspect ratio, update the best dimensions
        if aspect_diff < min_aspect_diff:
            best_cols, best_rows = cols, rows
            min_aspect_diff = aspect_diff
    
    return best_cols, best_rows

def create_image_grid(input_dir, output_file, grid_ratio=(7, 13), img_size=(400, 400)):
    # Get list of image files
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.jfif'))]
    total_images = len(image_files)

    # Calculate grid dimensions
    grid_height, grid_width = closest_grid_dimensions(total_images, grid_ratio[0] / grid_ratio[1])
    # grid_height = math.isqrt(total_images * grid_ratio[0] // grid_ratio[1])
    # grid_width = grid_height * grid_ratio[1] // grid_ratio[0]

    # Adjust grid size if necessary
    while grid_height * grid_width < total_images:
        grid_width += 1

    # Create a new image with the calculated grid size
    grid_img = Image.new('RGB', (grid_width * img_size[0], grid_height * img_size[1]))

    # Place images in the grid
    for idx, img_file in enumerate(image_files):
        if idx >= grid_width * grid_height:
            break
        with Image.open(os.path.join(input_dir, img_file)) as img:
            # Resize image to 400x400
            img_resized = img.resize(img_size, Image.Resampling.LANCZOS)
            x = (idx % grid_width) * img_size[0]
            y = (idx // grid_width) * img_size[1]
            grid_img.paste(img_resized, (x, y))

    # Save the result
    grid_img.save(output_file)
    print(f"Grid created with dimensions: {grid_width}x{grid_height}")

# Usage
input_directory = './images'
output_file = 'output_grid.jpg'
create_image_grid(input_directory, output_file)
