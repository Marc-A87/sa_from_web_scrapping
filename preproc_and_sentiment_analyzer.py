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

print(f"{len(all_song_links)} text files identified will be analyzed.")


print("\n\n")
sid = SentimentIntensityAnalyzer()

print(all_song_links[0])


# Open each *.txt file

for lyrics_file in all_song_links[0:5]:
    song_lyrics = []
    for line in open(lyrics_file, "r"):
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
            #print(evaluated_lines + 1)
            #print(line)
            line_results = sid.polarity_scores(line)
            #print(line_results)

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

  
