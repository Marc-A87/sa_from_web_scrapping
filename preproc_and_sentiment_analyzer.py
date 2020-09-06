import re
import os
import shutil
from tqdm import tqdm
import nltk

# nltk.download('vader_lexicon')
import glob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import statistics

# Creating listing to all text files
root_folder = os.getcwd()

path = ".\\temp"

text_files = glob.glob(path + "/**/*.txt", recursive=True)

all_song_links = []


# Creating list containing all absolute paths
for i in text_files:
    all_song_links.append(root_folder + i[1:])

print(f"\n\n{len(all_song_links)} text files identified will be analyzed.\n")

sid = SentimentIntensityAnalyzer()

# print(all_song_links[0])


# Creating dictionnary holding all compound values of analyzed song, by artist
values_by_artist = {}


# Open each *.txt file
for lyrics_file in tqdm(all_song_links):

    song_lyrics = []

    # identify artist

    current_artist_match = re.search(r"\\temp\\(.*?)\\", lyrics_file)

    try:
        current_artist_name = current_artist_match.group(1)
        # print(f'Current artist: {current_artist_name}')
    except:
        pass

    for line in open(lyrics_file, "r", encoding="utf-8"):
        song_lyrics.append(line.strip())

    # Cleaning text, removing unwanted characters and formatting
    REPLACE_NO_SPACE = re.compile("[.;:!'?,\"()\[\]]")
    REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

    def preprocess_lyrics(lyrics):
        lyrics = [REPLACE_NO_SPACE.sub("", line.lower()) for line in lyrics]
        lyrics = [REPLACE_WITH_SPACE.sub(" ", line) for line in lyrics]

        return lyrics

    lyrics_clean = preprocess_lyrics(song_lyrics)

    song_neg_value = 0.0
    song_neutral_value = 0.0
    song_pos_value = 0.0
    song_compound_value = 0.0

    song_neg_value_list = []
    song_neutral_value_list = []
    song_pos_value_list = []
    song_compound_value_list = []

    evaluated_lines = 0

    for line in lyrics_clean:
        if len(line) > 0 and line != "repeat chorus" and line != "chorus":
            # print(evaluated_lines + 1)
            # print(line)
            line_results = sid.polarity_scores(line)
            # print(line_results)

            # Increasing total of each value and append lists
            song_neg_value += line_results["neg"]
            song_neg_value_list.append(float(line_results["neg"]))

            song_neutral_value += line_results["neu"]
            song_neutral_value_list.append(float(line_results["neu"]))

            song_pos_value += line_results["pos"]
            song_pos_value_list.append(float(line_results["pos"]))

            song_compound_value += line_results["compound"]
            song_compound_value_list.append(float(line_results["compound"]))

            evaluated_lines += 1

        else:
            pass
    """
    print(f"VALUES FOR SONG: {lyrics_file}")
    print(f"Total negative value: {song_neg_value}")
    print(f"Total neutral value: {song_neutral_value}")
    print(f"Total positive value: {song_pos_value}")
    # print(f'Total compound value: {song_compound_value}')
    print(f"Total evaluated lines: {evaluated_lines}")
    print(f"Mean compound value: {statistics.mean(song_compound_value_list)}")

    if statistics.mean(song_compound_value_list) > 0:
        print("Song trending towards POSITIVITY")

    else:
        print("Song trending towards NEGATIVITY\n\n")
    """

    # Adding value to dictionnary

    try:
        values_by_artist.setdefault(current_artist_name, []).append(
            statistics.mean(song_compound_value_list)
        )
    except:
        pass


# print(values_by_artist)


# printing mean compound value by artist:
for key, value in values_by_artist.items():

    artist_trend = ""

    if sum(value) / len(value) > 0.01:
        artist_trend = "POSITIVITY"
    else:
        artist_trend = "NEGATIVITY"

    print(
        f"\t {key} mean compound value = {round(sum(value)/len(value),3)} -> trending towards {artist_trend} ({len(value)} songs analyzed)"
    )

"""
#debug
for key, value in values_by_artist.items():
    print(key)
    print(value[0:10])
"""
