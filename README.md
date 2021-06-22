# **Song-Transposer**

### **Python script that takes a song with chords as a string, and transposes chords to any musical key specified by the user.**

Uses pandas to identify which lines are composed of Chords, then runs a transposition function only on those lines. 
This ensures that any lines containing lyrics are ignored and 'Blowing in the wind' does not become 'Flowing in the wind'.

I have also created a web app so anyone can use this tool. Try copying the song below and pasting into the input box to transpose.

Link to app - http://sjmccoy.pythonanywhere.com/chords

```
[Verse]
G        C            D        G
How many roads must a man walk down,
           C          G
Before you call him a man
G        C           D          G
How many seas must a white dove sail,
           C             D
Before she sleeps in the sand
         G        C              D           G
Yes, and how many times must the cannonballs fly,
               C       G
Before they're forever banned
 
[Chorus]
C            D        G                C
The answer my friend is blowin' in the wind
              D              G
The answer is blowin' in the wind
 
[Harmonica Refrain]
| C  D  | G  C  | C  D  | G     |
 
[Verse]
         G        C           D         G
Yes, and how many years can a mountain exist,
             C             G
Before it is washed to the sea
         G        C              D      G
Yes, and how many years can some people exist,
               C             D
Before they're allowed to be free
         G        C           D            G
Yes, and how many times can a man turn his head,
                     C           G
And pretend that he just doesn't see
 
[Chorus]
C            D        G                C
The answer my friend is blowin' in the wind
              D              G
The answer is blowin' in the wind
 
[Harmonica Refrain]
| C  D  | G  C  | C  D  | G     |
 
[Verse]
         G        C            D        G
Yes, and how many times must a man look up,
              C       G
Before he can see the sky
         G        C         D       G
Yes, and how many ears must one man have,
              C           D
Before he can hear people cry
         G        C              D            G
Yes, and how many deaths will it take till he knows,
              C           G
That too many people have died
 
[Chorus]
C            D          G              C
The answer my friend is blowin' in the wind
              D              G
The answer is blowin' in the wind
 
[Harmonica Outro]
| C  D  | G  C  | C  D  | G     |
```

**How it works**

First, all lines are separated into a list and are designated as chords or non-chord lines. This is the trickiest part since it is difficult to develop rules that will consistently identify lines that are chords even when there is some text in the line. Take for instance [this](https://tabs.ultimate-guitar.com/tab/taylor-swift/22-chords-1189512) version of 22 by Taylor Swift. The author has included * symbols next to the chords, which causes ultimate-guitar to not recognize certain chords. If you try to use their transposition tool, it will miss these chords and return a broken song. My transposer tool attempts to remedy this by ignoring certain symbols and words that are often written next to chords. 

Next it uses pattern matching to translate chords to different keys specified by the user. This tool uses increments of half-steps, so to transpose from the key of A to the key of E would be 7 half-steps up or 5 half-steps down.

Finally, my tool attempts to identify the key of the song using the chords that are present. This is still a bit of a work-in-progress because the musical theory involved goes beyond my self-taught musician knowledge, and things like key changes within songs further complicate the issue. For now it uses the circle of fifths and the list of chords present to return a list of the possible keys
