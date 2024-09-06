from PIL import Image
from PIL.ExifTags import TAGS
import os
import sys


def convert_ifd_rational(value):
    """Helper function to handle IFDRational types"""
    if isinstance(value, tuple) and len(value) == 2:
        return float(value[0]) / float(value[1])
    return value


def scorpion():
    images = []
    extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    for file in sys.argv[1:]:
        if os.path.isfile(file) and file.lower().endswith(extensions):
            images.append(file)
        else:
            print(f'File not found: {file}')

    print(f'Found {len(images)} images: {images}')

    for image_file in images:
        image = Image.open(image_file)
        exif_data = image._getexif()
        print(f"\033[1;32;40mFilename: {os.path.basename(image_file)}\033[0m")
        print(f"Image format: {image.format}")
        print(f"Mode: {image.mode}")
        print(f"Size: {image.size}")
        print(f"Image width: {image.width}")
        print(f"Image height: {image.height}")
        if exif_data is not None:
            readable_exif = {}
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                readable_exif[tag_name] = value
            for tag, value in readable_exif.items():
                if isinstance(value, dict):
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
                                int(lat_degrees), int(lat_minutes), (float(lat_seconds)), gps_info[1], int(lon_degrees), int(lon_minutes), float(lon_seconds), gps_info[3]
                            )
                            print(f"\t{tag}: {geo_coords}")
                        except KeyError:
                            print(f"   {tag}: Invalid GPS data")
                    else:
                        print(f'{tag}:')
                        for subtag, subvalue in value.items():
                            subtag_name = TAGS.get(subtag, subtag)
                            print(f'  {subtag_name}: {subvalue}')
                else:
                    print(f"  {tag}: {value}")
        else:
            print('No EXIF data found')


if __name__ == '__main__':
    scorpion()
