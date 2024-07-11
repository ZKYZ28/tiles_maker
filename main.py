import os
import argparse
from PIL import Image

def image_to_tiles(image_path, output_dir, zoom_levels):
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Le fichier spécifié n'existe pas : {image_path}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image = Image.open(image_path)
    width, height = image.size

    for z in range(zoom_levels + 1):
        num_tiles = 2 ** z
        tile_size = 256

        zoom_dir = os.path.join(output_dir, str(z))
        if not os.path.exists(zoom_dir):
            os.makedirs(zoom_dir)

        resized_image = image.resize((num_tiles * tile_size, num_tiles * tile_size), Image.Resampling.LANCZOS)

        for y in range(num_tiles):
            y_dir = os.path.join(zoom_dir, str(y))
            if not os.path.exists(y_dir):
                os.makedirs(y_dir)

            for x in range(num_tiles):
                left = x * tile_size
                upper = y * tile_size
                right = left + tile_size
                lower = upper + tile_size

                tile = resized_image.crop((left, upper, right, lower))
                tile_path = os.path.join(y_dir, f"{x}.png")
                tile.save(tile_path, "PNG")
                print(f"Saved tile {z}/{y}/{x}.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate image tiles for different zoom levels.')
    parser.add_argument('image_path', type=str, help='Path to the source image')
    parser.add_argument('output_dir', type=str, help='Directory to save the tiles')
    parser.add_argument('zoom_levels', type=int, help='Number of zoom levels')

    args = parser.parse_args()
    image_to_tiles(args.image_path, args.output_dir, args.zoom_levels)
