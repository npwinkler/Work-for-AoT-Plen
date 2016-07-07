/* Weather System */

TASK/GOAL: USE KPL to get weather data from NOAA et al and put it into the stream so that we can allow users to access it through AoNodes infrastructure....

OBSTACLE/CHALLENGE/HURDLES: 

REVISING/UPDATING DATA.....(QC replaces METAR after a day, i.e. when QC observation events come in, go into the archive & change the corresponding observation events that we got from METAR)
/* METAR real-time, QUALITY CONTROL day-late....SAME TIMESTAMPS -> this + _____ tells us how we know which METAR obs to replace with which QC obs) */ 


ARCHICTECTURE: TWO KINESIS STREAMS 
1) 'livestream' of METAR -> archiver & streamer
2) 'UPDATE delayed' stream of QCLD -> archiver (don't report live because who cares when they 'come in'...)

WHAT CODE NEEDS TO DO:
/* hit up some files, pick out (both hourly & daily) data & send to the two streams */
0) set up these two streams
1) 'slurp up data' from the same sites E
2) 'Transform' T
3) use KPL to send it off to the appropriate streams L

What to go through weather.py & weather_metar.py for:
UNDERSTAND FILE FORMATS
See/understand/re-use/etc....the Transform stage of data from website -> data for our use....





