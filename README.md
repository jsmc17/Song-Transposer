# **Song-Transposer**
### **Python script that takes a song with chords as a string, and transposes chords to any musical key specified by the user.**

Uses pandas to identify which lines are composed of Chords, then runs a transposition function only on those lines. 
This ensures that any lines containing lyrics are ignored and 'Blowing in the wind' does not become 'Flowing in the wind'.
