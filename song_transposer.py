import pandas as pd
import numpy as np
import re
import pyperclip

chords_regex = ['F(?!#)', 'F#','G(?!#)', 'G#', 'A(?!#)', 'A#', 'B', 'C(?!#)', 'C#', 'D(?!#)', 'D#','E']
regex_index = ['f^', 'f#^','g^', 'g#^', 'a^', 'a#^', 'b^', 'c^', 'c#^', 'd^', 'd#^','e^',
               'f^', 'f#^','g^', 'g#^', 'a^', 'a#^', 'b^', 'c^', 'c#^', 'd^', 'd#^','e^']


regex1_output = ['f\^', 'f#\^','g\^', 'g#\^', 'a\^', 'a#\^', 'b\^', 'c\^', 'c#\^', 'd\^', 'd#\^','e\^']
regex2_output = ['F', 'F#','G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#','E']


def transpose(song, modifier):
    #transposition function - takes string and modifier # and outputs transposed string
    for i in range(12):
        p = re.compile(chords_regex[i])
        song = p.sub(regex_index[i+modifier], song)
    for i in range(12):
        p = re.compile(regex1_output[i])
        song = p.sub(regex2_output[i], song)
    return(song)

def dframe(song_by_lines):
    df = pd.DataFrame(data = song_by_lines)
    df.columns = ['text']

    # adding new columns to dataframe (NCTC, NSTC, percent, dash_count)
    # features of columns will be used to determine if CHORD column will be 1 or 0
    # rows with 1 are lines of chords
    # rows with 0 are not chords (lyrics, spaces, tabs, parts of a song['outro', 'intro', etc...])
    df['length'] = df['text'].apply(len)
    df['NCTC'] = df['length'] \
    - df['text'].str.count('A|B|C|D|E|F|G') \
    - df['text'].str.count(' ') \
    - df['text'].str.count('\t') \
    - df['text'].str.count('/') \
    - df['text'].str.count('#|m|b|x|1|2|3|4|5|6|7|8|9') \
    - df['text'].str.count('%|-|–') \
    - df['text'].str.count('\(') \
    - df['text'].str.count('\)') \
    - df['text'].str.count('\|') \
    - df['text'].str.count('<|>') \
    - df['text'].str.count('\.') \
    - df['text'].str.count('\r') \
    - df['text'].str.count('sus|aug|add')*3\
    - df['text'].str.count('maj|dim')*2\
    - df['text'].str.count('Intro|intro')*5\
    - df['text'].str.count('Outro|outro')*5\
    - df['text'].str.count('Riff|riff')*4\
    - df['text'].str.count('once')*4\
    #subtracting count of nonchord text characters (NCTC)

    df['NSTC'] = df['length'] - df['text'].str.count(' ') - df['text'].str.count('\t')
    #subtracting count of non space or tab characters (NSTC)

    df['percent'] = df['NCTC']/df['length']
    # - % of total characters that are nonchord text characters - threshhold set at 10% of this value
    df['dash_count'] = df['text'].str.count('-')
    # - dash count - helps identify lines of guitar tableture

    df['CHORD'] = np.where((df['percent']<=.1)&(df['dash_count']<10)&(df['NSTC']>0),1,0)
    # - creates column that indicates whether our algorithm selects a line as a CHORD line... 1 for y -  0 for n


    # converting rows with chords from DF to string to be read by transposition function
    ser1 = df['text'][df['CHORD']==1]
    lizt = list(ser1)
    strang = '\n'.join(lizt)


    strang1 = transpose(strang,mod)

    lizt = strang1.split('\n')

    ser = pd.Series(lizt, index = ser1.index)
    ser2 = df['text'][df['CHORD']==0]
    ser3 = pd.concat([ser,ser2])

    lizt = ser3.sort_index()
    output = '\n'.join(lizt)
    return output




print('''Welcome to Simple Song Transposer.
-To begin, copy the song you wish to transpose to the clipboard (Ctrl + C).
-Then when prompted for a modifier enter any integer from 1-11(positive or negative).
-This will be the number of steps up or down the song will be transposed.
-------------------------------------------------------------------------''')

while True:
    
    try:
        inp = input('Enter modifier')
        mod = int(inp)
    except ValueError:
        print('Must enter a number')
    if inp.lower() == 'q':
        break
    song = pyperclip.paste()
    lizt = song.split('\n')

    #
    try:
        output = dframe(lizt)
        print(output)
        pyperclip.copy(output)

        print('''\n-------------------------------------------------------------------------
-Transposed Song copied to clipboard.
-Enter another modifier to transpose again:
-Enter 'Q' to quit.
''')
    except ValueError:
        print('''Song Transposer did not detect any chords.
Try to re-copy song to the clipboard and try again.
''')

