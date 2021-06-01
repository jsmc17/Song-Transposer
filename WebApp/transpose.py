import pandas as pd
import numpy as np
import re


chords_regex = ['F(?!#)', 'F#','G(?!#)', 'G#', 'A(?!#)', 'A#', 'B', 'C(?!#)', 'C#', 'D(?!#)', 'D#','E']
regex_index = ['f^', 'f#^','g^', 'g#^', 'a^', 'a#^', 'b^', 'c^', 'c#^', 'd^', 'd#^','e^',
               'f^', 'f#^','g^', 'g#^', 'a^', 'a#^', 'b^', 'c^', 'c#^', 'd^', 'd#^','e^']


regex1_output = ['f\^', 'f#\^','g\^', 'g#\^', 'a\^', 'a#\^', 'b\^', 'c\^', 'c#\^', 'd\^', 'd#\^','e\^']
regex2_output = ['F', 'F#','G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#','E']

keez = {'A': ['D', 'Bm', 'A', 'F#m', 'E', 'C#m'],
 'A#': ['D#', 'Cm', 'A#', 'Gm', 'F', 'Dm'],
 'A#m': ['F#', 'D#m', 'C#', 'A#m', 'G#', 'Fm'],
 'Am': ['F', 'Dm', 'C', 'Am', 'G', 'Em'],
 'B': ['E', 'C#m', 'B', 'G#m', 'F#', 'D#m'],
 'Bm': ['G', 'Em', 'D', 'Bm', 'A', 'F#m'],
 'C': ['F', 'Dm', 'C', 'Am', 'G', 'Em'],
 'C#': ['F#', 'D#m', 'C#', 'A#m', 'G#', 'Fm'],
 'C#m': ['A', 'F#m', 'E', 'C#m', 'B', 'G#m'],
 'Cm': ['G#', 'Fm', 'D#', 'Cm', 'A#', 'Gm'],
 'D': ['G', 'Em', 'D', 'Bm', 'A', 'F#m'],
 'D#': ['G#', 'Fm', 'D#', 'Cm', 'A#', 'Gm'],
 'D#m': ['B', 'G#m', 'F#', 'D#m', 'C#', 'A#m'],
 'Dm': ['A#', 'Gm', 'F', 'Dm', 'C', 'Am'],
 'E': ['A', 'F#m', 'E', 'C#m', 'B', 'G#m'],
 'Em': ['C', 'Am', 'G', 'Em', 'D', 'Bm'],
 'F': ['A#', 'Gm', 'F', 'Dm', 'C', 'Am'],
 'F#': ['B', 'G#m', 'F#', 'D#m', 'C#', 'A#m'],
 'F#m': ['D', 'Bm', 'A', 'F#m', 'E', 'C#m'],
 'Fm': ['C#', 'A#m', 'G#', 'Fm', 'D#', 'Cm'],
 'G': ['C', 'Am', 'G', 'Em', 'D', 'Bm'],
 'G#': ['C#', 'A#m', 'G#', 'Fm', 'D#', 'Cm'],
 'G#m': ['E', 'C#m', 'B', 'G#m', 'F#', 'D#m'],
 'Gm': ['D#', 'Cm', 'A#', 'Gm', 'F', 'Dm']}

root_chords = [ 'F','C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'F','C', 'Dm', 'Am', 'Em', 'Bm', 'F#m', 'C#m', 'G#m', 'D#m', 'A#m', 'Fm', 'Cm', 'Gm', 'Dm', 'Am']
sevenths = ['C7', 'C#7', 'D7', 'D#7','E7', 'F7', 'F#7','G7', 'G#7', 'A7','A#7', 'B7']

def transpose(song, modifier):
    #transposition function - takes string and modifier # and outputs transposed string
    for i in range(12):
        p = re.compile(chords_regex[i])
        song = p.sub(regex_index[i+modifier], song)
    for i in range(12):
        p = re.compile(regex1_output[i])
        song = p.sub(regex2_output[i], song)
    return(song)

def key_identify(chords):
  cl =  re.split(' |\n|/|\t', chords) # chord list
  rcl = [re.sub('sus|aug|add|maj|dim|\d', '', chord) for chord in cl ] # root chord list
  ccl = [chord for chord in rcl if chord in root_chords] #clean chord list - removes white space, any other text
  ucl = list(set(ccl)) # unique chord list

  possible_keys = []         # 1st key check - looks to see if ALL chords in song are present in 6 circle of fifths chords for each possible key
  for k,v in keez.items():
    if all(elem in v for elem in ucl):
      possible_keys.append(k)
  possible_keys

  if len(possible_keys) == 0:   #2nd key check - only runs if no possible keys found in first check
    cc = {} # chord count - for each possible key, how many of 6 chords are present in song
    ct = 0
    for k,v in keez.items():
      cc[k] = sum(elem in ucl for elem in keez[k])
      if cc[k] > ct:
        ct = cc[k]

    print(ucl)
    print(cc)

    # Find item with Max Value in Dictionary
    itemMaxValue = max(cc.items(), key=lambda x: x[1])
    print('Maximum Value in Dictionary : ', itemMaxValue[1])
    # Iterate over all the items in dictionary to find keys with max value
    for key, value in cc.items():
        if value == itemMaxValue[1]:
            possible_keys.append(key)

  # Finding most likely key from list of possible keys
  first_chord = ccl[0]
  last_chord = ccl[-1]
#   seven = list(set([chord for chord in cl if chord in sevenths])) # list of dominant 7th chords in song



  if first_chord in possible_keys:
    msg = f'First chord in possible keys\nLikely key: {first_chord}'
    return msg, possible_keys
  elif last_chord in possible_keys:
    msg = f'Last chord in possible keys\nLikely key: {first_chord}'
    return msg, possible_keys
  else:
    msg = 'Cannot figure out most likely key. Try from list of possible'
    return msg, possible_keys

def dframe(song_by_lines, stps):
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
    - df['text'].str.count('#|m|b|x|X|1|2|3|4|5|6|7|8|9') \
    - df['text'].str.count('%|-|–') \
    - df['text'].str.count('\(') \
    - df['text'].str.count('\)') \
    - df['text'].str.count('\|') \
    - df['text'].str.count('<|>') \
    - df['text'].str.count('\.') \
    - df['text'].str.count('\,') \
    - df['text'].str.count('\r') \
    - df['text'].str.count('\+') \
    - df['text'].str.count('sus|aug|add|Sus|Aug|Add')*3\
    - df['text'].str.count('maj|dim|Maj|Dim')*2\
    - df['text'].str.count('Intro|intro')*5\
    - df['text'].str.count('Outro|outro')*5\
    - df['text'].str.count('Repeat|repeat')*6\
    - df['text'].str.count('Riff|riff')*4\
    - df['text'].str.count('once|Once|twice|Twice')*4\
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




    strang1 = transpose(strang,stps)

    m, key = key_identify(strang1)

    lizt = strang1.split('\n')

    ser = pd.Series(lizt, index = ser1.index)
    ser2 = df['text'][df['CHORD']==0]
    ser3 = pd.concat([ser,ser2])

    lizt = ser3.sort_index()
    output = '\n'.join(lizt)
    return output, m, key