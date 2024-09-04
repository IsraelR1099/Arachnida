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
    print(f"recursive: {recursive}")
    print(f"dept: {depth}")
    print(f"save_path: {path}")
    print(f"url: {url}")
    URL_BASE = 'https://scrapepark.org/courses/spanish'
    extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
    response = requests.get(URL_BASE)
    html_response = response.text

    soup = BeautifulSoup(html_response, "html.parser")
    images = soup.find_all(src=True, limit=depth, recursive=recursive)
    for image in images:
        if image['src'].endswith(extensions):
            print(image)


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
