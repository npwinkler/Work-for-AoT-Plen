# What this file does is _______________ 
# "ETL stuff"....



import requests
import os
import sys
import tarfile
import zipfile
import re
from ftplib import FTP
#from cStringIO import StringIO
from StringIO import StringIO
from csvkit.unicsv import UnicodeCSVReader, UnicodeCSVWriter, \
    UnicodeCSVDictReader, FieldSizeLimitError
from dateutil import parser
from datetime import datetime, date, timedelta
from dateutil import relativedelta
import operator

import calendar
from plenario.database import session as session, app_engine as engine, \
    Base
from plenario.settings import DATA_DIR
import sqlalchemy
from sqlalchemy import Table, Column, String, Date, DateTime, Integer, Float, \
    VARCHAR, BigInteger, and_, select, text, distinct, func
from sqlalchemy.dialects.postgresql import ARRAY
from geoalchemy2 import Geometry
from uuid import uuid4
from metar.metar import ParserError

from weather_metar import getMetar, getMetarVals, getAllCurrentWeather, getCurrentWeather

# from http://stackoverflow.com/questions/7490660/converting-wind-direction-in-angles-to-text-words
def degToCardinal(num):
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return arr[(val % 16)]


class WeatherError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
        self.message = message
