import re
import os
import shutil
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

# Mimicking a browser request
headers = {"User-Agent": "Mozilla/5.0"}

# Creating dict for removing restricted char from potential filenames to be created
remove_punctuation_map = dict((ord(char), None) for char in '\/*?:"<>|')

# Defining working directory
path = os.getcwd()

working_directory = path+"\\temp"

# Delete if previous version exists
try:
    shutil.rmtree(working_directory)
except:
    pass
    
# Creating temp directory for storing generated *.txt files 
os.mkdir('temp')


# Creating band list
bands_list = [
    "iron maiden"
]

# Capitalizing first letter of each word
bands_list_cap = []

for band in tqdm(bands_list):
    bands_list_cap.append(band.title())

bands_root_url = []

for band in tqdm(bands_list):
    # Keeping first letter for alphabetical categorization
    # Removing spaces in bands name
    bands_root_url.append(
        str(f'http://www.darklyrics.com/{band[0]}/{band.replace(" ","")}.html')
    )

# Creating dictionnary
bands_dict = dict(zip(bands_list_cap, bands_root_url))

# Creating full track-listing links for each artist in scope

current_artist_albums_links = []
final_artists_list = []
full_tracklist_dict = {}

for key, value in tqdm(bands_dict.items()):

    current_artist_albums_links = []

    # print(value)

    # request page
    current_page = requests.get(value, headers=headers)

    # soupify
    current_soup = BeautifulSoup(current_page.content, "html.parser")

    # Finding div containing albums
    albums_div = current_soup.findAll("div", attrs={"class": "album"})
    # print(albums_div)
    # Appending all links found in identified divs
    for div in albums_div:
        # albums_links.append(div.findAll('a'))
        for link in div.find_all("a"):

            unformatted_link = "http://www.darklyrics.com/" + link.get("href")
            formatted_link = unformatted_link.replace("/..", "")

            current_artist_albums_links.append(formatted_link)

    full_tracklist_dict[key] = current_artist_albums_links
    print(f"{len(current_artist_albums_links)} songs found for artist {key}")


# Keep one link per album (full_tracklist_dict kept for future reference)

single_link_dict = {}
first_links_for_album_in_artist = []

for key in tqdm(full_tracklist_dict):
    first_links_for_album_in_artist = []
    # print(key)
    full_tl = full_tracklist_dict.get(key)
    for l in full_tl:

        if l[-2:] == "#1":
            first_links_for_album_in_artist.append(l)

    single_link_dict[key] = first_links_for_album_in_artist


# Parsing artist and album name
for key, value in tqdm(single_link_dict.items()):

    os.chdir(working_directory)

    current_artist = key
    album = value

    print(f"Current artist: {current_artist}")

    for album in tqdm(value):
        # matching album
        match = re.search(r"http://www.darklyrics.com/lyrics/*/(.*?).html", album)
        temp_album = match.group(1)
        current_album = temp_album.split("/")[1].lstrip().split(" ")[0]
        print(f"Current album: {current_album}")

        if os.path.exists(current_artist):
            os.chdir(f"{working_directory}\\{current_artist}\\")
            os.mkdir(current_album)
            os.chdir(f"{working_directory}\\{current_artist}\\{current_album}\\")
        else:
            os.mkdir(current_artist)
            os.chdir(f"{working_directory}\\{current_artist}\\")
            os.mkdir(current_album)
            os.chdir(f"{working_directory}\\{current_artist}\\{current_album}\\")

        r = requests.get(str(album) + """#1""", headers=headers)

        soup = BeautifulSoup(r.text, "html.parser")
        albums = soup.findAll("div", {"class": "lyrics"})
        A = str(albums[0].get_text())

        # Temp output file for further parsing
        text_file = open(r"Output.txt", "w", encoding="utf-8")
        text_file.write(A)
        text_file.close()

        ##Read temp output file line by line and parse by using regex on the Song title e.g 1,2,3.
        readfile = open(r"Output.txt", "r", encoding="utf-8")
        lines = readfile.readlines()
        readfile.close()

        # Create temp file to avoid error for first text_file.close()
        Single_Song_Output = []
        text_file = open(r"temp.txt", "w", encoding="utf-8")

        for line in lines:
            if re.search("[0-9][.] .", line):
                if not os.path.exists(r"{}.txt".format(line)):
                    text_file.close()

                    # removing forbidden characters from filename
                    line = line.translate(remove_punctuation_map)
                    text_file = open(
                        r"{}.txt".format(line.strip()), "w", encoding="utf-8"
                    )
                # print('NEW SONG!!!!!!\n')
                # print(line)
            else:
                text_file.write(line)


print("Processing complete")
