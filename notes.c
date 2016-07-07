/* Weather System */

/*TASK/GOAL: Remove weather access from Plenario (Weather) API and instead USE KPL to  allow users to access weather data in a format the same as how we do it for/in AoT stuf....

OBSTACLE/CHALLENGE/HURDLES: REVISING/UPDATING DATA.....METAR IS REAL-TIME, QUALITY CONTROL IS A DAY-LATE....BUT HAS THE SAME TIMESTAMPS.....

TWO KINESIS STREAMS 
1) LIVESTREAM OF METAR
2) UPDATE/DELAYED STREAM OF QCLD WILL HAVE OUR ARCHIVER RUNNING ON IT


SUBTASKS:
dig into ETL
UNDERSTAND FILE FORMATS OF QCLD AND METAR.....

'dogfooding' the interface....






/* Weather.py & weather_metar.py */
/* What weather.py does:

hits up some filesystems and picks out recent data.... */



