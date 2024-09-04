from bs4 import BeautifulSoup

import requests
import sys
import os

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

    print(f"recursive: {recursive}")
    print(f"dept: {depth}")
    print(f"save_path: {save_path}")
    print(f"url: {url}")


if __name__ == '__main__':
    main()
