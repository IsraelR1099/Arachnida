from PIL import Image
from PIL.ExifTags import TAGS
import os
import sys

def parse_arguments():
    delete = False
    images = []
    extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    for file in sys.argv[1:]:
        if file == '--delete' or file == '-d':
            delete = True
        elif os.path.isfile(file) and file.lower().endswith(extensions):
            images.append(file)
        else:
            print(f'File not found: {file}')
    return images, delete


def convert_ifd_rational(value):
    """Helper function to handle IFDRational types"""
    if isinstance(value, tuple) and len(value) == 2:
        return float(value[0]) / float(value[1])
    return value


def print_basic_info(image, image_file):
    """
    Display basic image info in a formatted table
    """
    print(f"{'='*50}")
    print(f"\033[1;32;40m{'Filename:'.ljust(25)} {os.path.basename(image_file)}\033[0m")
    print(f"{'Image format:'.ljust(25)} {image.format}")
    print(f"{'Mode:'.ljust(25)} {image.mode}")
    print(f"{'Size:'.ljust(25)} {image.size}")
    print(f"{'Width:'.ljust(25)} {image.width}")
    print(f"{'Height:'.ljust(25)} {image.height}")
    print(f"{'='*50}")


def print_exif_data(tag, value, readable_exif):
    if tag == 'GPSInfo':
        gps_info = readable_exif['GPSInfo']
        try:
            lat_degrees = convert_ifd_rational(gps_info[2][0])
            lat_minutes = convert_ifd_rational(gps_info[2][1])
            lat_seconds = convert_ifd_rational(gps_info[2][2])
            lon_degrees = convert_ifd_rational(gps_info[4][0])
            lon_minutes = convert_ifd_rational(gps_info[4][1])
            lon_seconds = convert_ifd_rational(gps_info[4][2])
            geo_coords = '{0}º {1}\' {2:.2f}" {3}, {4}º {5}\' {6:.2f}" {7}'.format(
                int(lat_degrees), int(lat_minutes),
                (float(lat_seconds)), gps_info[1],
                int(lon_degrees), int(lon_minutes),
                float(lon_seconds), gps_info[3]
            )
            print(f"{tag.ljust(25)} {geo_coords}")
        except KeyError:
            print(f"{tag.ljust(25)} Invalid GPS data")
    else:
        print(f'{tag.ljust(25)}:')
        for subtag, subvalue in value.items():
            subtag_name = TAGS.get(subtag, subtag)
            print(f'{subtag_name.ljust(25)}: {subvalue}')


def delete_exif(images):
    """
    Function to clear metadata from a specified image
    """
    for image_file in images:
        image = Image.open(image_file)
        exif_data = image._getexif()
        if exif_data is not None:
            data = list(image.getdata())
            # Create new image with same mode and same size but without
            # metadata
            image_no_metadata = Image.new(image.mode, image.size)
            image_no_metadata.putdata(data)
            # Save the new image over the original file.
            image_no_metadata.save(image_file)
            print(f"Metada succesfully cleared from '{image_file}'")
        else:
            print(f"No metadata found in '{image_file}'")


def scorpion():
    images, delete = parse_arguments()
    if len(images) == 0:
        print("No image provided.")
        sys.exit(0)
    print(f'Found {len(images)} images: {images}')

    for image_file in images:
        image = Image.open(image_file)
        exif_data = image._getexif()
        print_basic_info(image, image_file)
        if exif_data is not None:
            readable_exif = {}
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if isinstance(value, bytes):
                    print(f"{str(tag_name).ljust(25)} [Binary data]")
                else:
                    readable_exif[tag_name] = value
            for tag, value in readable_exif.items():
                if isinstance(value, dict):
                    print_exif_data(tag, value, readable_exif)
                else:
                    print(f"{str(tag).ljust(25)} {value}")
        else:
            print('No EXIF data found')

    if delete:
        delete_exif(images)

if __name__ == '__main__':
    scorpion()
