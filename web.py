from bs4 import BeautifulSoup
import requests
import sys
import os


def main():

    recursive = False
    depth = 5
    save_path = "./data/"
    url = None

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if "r" in arg:
            recursive = True
        elif "l" in arg and len(arg) <= 2:
            if i + 1 < len(sys.argv):
                try:
                    depth = int(sys.argv[i + 1])
                    if depth < 0:
                        print("Error: depth must be a positive number")
                        sys.exit(1)
                    i += 1
                except ValueError:
                    print("Error: depth must be a number")
                    sys.exit(1)
            else:
                print("Error: No depth value provided after -l.")
                sys.exit(1)
        elif "p" in arg and len(arg) <= 2:
            if i + 1 < len(sys.argv):
                save_path = sys.argv[i + 1]
                if not os.path.isdir(save_path):
                    print(f"Error: The specified path {save_path} is not a valid directory.")
                    sys.exit(1)
                i += 1
            else:
                print("Error: No path value provided after -p.")
                sys.exit(1)
        else:
            if not arg.startswith("-"):
                url = arg
        i += 1

    print(f"Recursive: {recursive}")
    print(f"Depth: {depth}")
    print(f"Path: {save_path}")
    print(f"URL: {url}")


if __name__ == '__main__':
    main()


"""URL_BASE = 'https://scrapepark.org/courses/spanish/'
response = requests.get(URL_BASE)
html_got = response.text

soup = BeautifulSoup(html_got, "html.parser")
type(soup)

tag_h2 = soup.find('h2')
print(tag_h2.text)

tag_all_h2 = soup.find_all('h2')
for tag in tag_all_h2:
    print(tag.get_text(strip=True))

images = soup.find_all(src=True)
for image in images:
    if image['src'].endswith(".jpg"):
        print(image)"""
