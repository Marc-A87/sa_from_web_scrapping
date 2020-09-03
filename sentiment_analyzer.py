import re
import os
import shutil
from tqdm import tqdm
import nltk
#nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import statistics

print("\n\n")

sid = SentimentIntensityAnalyzer()

# Generate dictionary {Author : {Album : Path to txt file containing lyrics of song}}


# For each key-value pair, open each *.txt file 
song_lyrics = []
for line in open('test_song.txt', 'r'):
    song_lyrics.append(line.strip())


# Cleaning text, removing unwanted characters and formatting
REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
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
    if len(line) > 0 and line != 'repeat chorus' and line != 'chorus':
        print(evaluated_lines+1)
        print(line)
        line_results = sid.polarity_scores(line)
        print(line_results)

        # Increasing total of each value and append lists
        song_neg_value += line_results["neg"]
        song_neg_value_list.append(float(line_results["neg"]))

        song_neutral_value += line_results["neu"]
        song_neutral_value_list.append(float(line_results["neu"]))

        song_pos_value += line_results["pos"]
        song_pos_value_list.append(float(line_results["pos"]))

        song_compound_value += line_results["compound"]
        song_compound_value_list.append(float(line_results["compound"]))

        print('\n')

        evaluated_lines += 1


    else:
        pass


print(f'VALUES FOR SONG: test_song')
print(f'Total negative value: {song_neg_value}')
print(f'Total neutral value: {song_neutral_value}')
print(f'Total positive value: {song_pos_value}')
#print(f'Total compound value: {song_compound_value}')
print('\n')
print(f'Total evaluated lines: {evaluated_lines}')
print('\n')
print(f'Mean compound value: {statistics.mean(song_compound_value_list)}')
print('\n')

if statistics.mean(song_compound_value_list) > 0:
    print('Song trending towards POSITIVITY')

else:
    print('Song trending towards NEGATIVITY')


print('\n')