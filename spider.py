from bs4 import BeautifulSoup

import requests
import sys
import os


def isInvalid(arg):
    valid_options = "rlp"
    for char in arg:
        if char not in valid_options:
            print(f"Error: Invalid option '-{char}' found.")
            sys.exit(1)


def scrap(recursive, depth, path, url):
    """
        recursive: This parameter controls if the search should
        include only direct children or if it should search through
        all descendants.
        depth: It tells the program to stop after it's found a certain number
        of resulsts.
        """
    # URL_BASE = 'https://scrapepark.org/courses/spanish'
    if path == './data/' and not os.path.exists(path):
        print(f"Creating {path} directory")
        os.makedirs(path)
    URL_BASE = url
    extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
    try:
        response = requests.get(URL_BASE)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: Invalid URL: '{URL_BASE}' or connection issue: {e}.")
        sys.exit(1)
    html_response = response.text

    soup = BeautifulSoup(html_response, "html.parser")
    images = soup.find_all(src=True, limit=depth, recursive=recursive)
    for i, image in enumerate(images):
        image_url = image['src']

        # Handle relative URLs by joining them with the base URL
        if not image_url.startswith(('http://', 'https://')):
            image_url = requests.compat.urljoin(url, image_url)

        # Check if the URL ends with a valid image extension
        if image_url.lower().endswith(extensions):
            name_image = os.path.basename(image_url)
            print(f"Downloading image {name_image} from {image_url}")

            try:
                img_response = requests.get(image_url)
                img_response.raise_for_status()

                # Verify the response content is actually an image
                if "image" in img_response.headers['Content-Type']:
                    image_path = os.path.join(path, name_image)
                    with open(image_path, "wb") as file:
                        file.write(img_response.content)
                else:
                    print(f"Warning: Skipping non-image content from {image_url}")
            except requests.exceptions.RequestException as e:
                print(f"Error: Unable to download image from {image_url}: {e}")
                continue


def main():
    recursive = False
    depth = 5
    save_path = './data/'
    url = None

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg.startswith('-'):
            if any(char in arg for char in "rlp"):
                isInvalid(arg[1:])
                if "r" in arg:
                    recursive = True
                if "l" in arg:
                    if i + 1 < len(sys.argv):
                        try:
                            depth = int(sys.argv[i + 1])
                            if depth < 0:
                                print("Error: depth must be a positive number.")
                                sys.exit(1)
                            i += 1
                        except ValueError:
                            print("Error: depth must be a number.")
                            sys.exit(1)
                    else:
                        print("Error: No depth value provided after -l.")
                        sys.exit(1)
                if "p" in arg:
                    if i + 1 < len(sys.argv):
                        save_path = sys.argv[i + 1]
                        if not os.path.isdir(save_path):
                            print(f"Error: The specified path \'{save_path}\' is not a valid directory.")
                            sys.exit(1)
                        i += 1
                    else:
                        print("Error: No path value provided after -p.")
                        sys.exit(1)
            else:
                print("Error: No valid option.")
                sys.exit(1)
        else:
            url = arg
        i += 1

    scrap(recursive, depth, save_path, url)


if __name__ == '__main__':
    main()
