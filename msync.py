import os
import sys
import uuid

p = ""


def print_usage():
    print("Usage: msync <mode> <arguments>")
    print("\t msync -c <world_folder>:    Create a new link from world_folder to saves")
    print("\t msync -l:                   List all links in saves")
    print("\t msync -q <id>:              Query the first matching link")
    print("\t msync -d <id>:              Delete the first matching link. NO UNDO!")
    exit()


if len(sys.argv) <= 1:
    print_usage()


def msync_create(path):
    if not os.path.exists(path):
        print("Folder not found!")
        exit()

    if not os.path.isdir(path):
        print("Path must be a folder!")
        exit()

    location = "msynclink_" + str(uuid.uuid4()).replace('-', '_')

    os.symlink(path, os.environ["appdata"] + "/.minecraft/saves/" + location, True)

    print("Successfully created link in world folder '" + location + "'")


def get_ids():
    return list(map(lambda x: x[len("msynclink_"):],
               filter(lambda x: x.startswith("msynclink_"), os.listdir(os.environ["appdata"] + "/.minecraft/saves/"))))


mode = sys.argv[1]

if mode == '-c':
    if len(sys.argv) < 3:
        print("Mode -c needs <world_folder> argument")
        exit()

    msync_create(sys.argv[2])

elif mode == '-l':
    links = get_ids()

    print(f"Found {len(links)} links in with the following IDs:")
    print()

    for link in links:
        print("\t", link)

elif mode == '-q':
    if len(sys.argv) < 3:
        print("Mode -q needs <id> argument")
        exit()

    links = get_ids()

    links = list(filter(lambda x: x.startswith(sys.argv[2]), links))

    if len(links) > 1:
        print("Query is not unique")
        exit()
    if len(links) < 1:
        print("No matches found!")
        exit()

    print("Match found!")
    print("\t id:   " + links[0])
    print("\t path: " + os.environ["appdata"] + "/.minecraft/saves/msynclink_" + links[0])

elif mode == '-d':
    if len(sys.argv) < 3:
        print("Mode -d needs <id> argument")
        exit()

    links = get_ids()
    links = list(filter(lambda x: x.startswith(sys.argv[2]), links))

    if len(links) > 1:
        print("Query is not unique")
        exit()
    if len(links) < 1:
        print("No matches found!")
        exit()

    os.unlink(os.environ["appdata"] + "/.minecraft/saves/msynclink_" + links[0])

    print("Successfully deleted link with id " + links[0])

else:
    print_usage()
