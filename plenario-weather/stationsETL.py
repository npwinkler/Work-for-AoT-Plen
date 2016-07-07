class WeatherStationsETL(object):
    """ 
    Download, transform and create table with info about weather stations
    """

    def __init__(self):
        self.stations_ftp = \
            'ftp.ncdc.noaa.gov'
        self.stations_file = \
            '/pub/data/noaa/isd-history.csv'

    def initialize(self):
        self._extract()
        self._transform()
        self._make_station_table()
        try:
            self._load()
        except:
            print 'weather stations already exist, updating instead'
            self._update_stations()

    def update(self):
        self._extract()
        self._transform()
        # Doing this just so self.station_table is defined
        self._make_station_table()
        self._update_stations()

    def _extract(self):
        """ Download CSV of station info from NOAA """

        try:
            ftp = FTP(self.stations_ftp) 
            ftp.login()
            stations = StringIO()
            ftp.retrbinary('RETR %s' % self.stations_file, stations.write)
            self.station_raw_info = stations
            self.station_raw_info.seek(0)
        except:
            self.station_info = None
            raise WeatherError('Unable to fetch station data from NOAA.')

    def _transform(self):
        reader = UnicodeCSVReader(self.station_raw_info)
        header = ['wban_code', 'station_name', 'country', 
                  'state', 'call_sign', 'location', 'elevation', 
                  'begin', 'end']
        reader.next()
        self.clean_station_info = StringIO()
        all_rows = []
        wbans = []

        for row in reader:
            wban = row[1]
            name = row[2]
            country = row[3]
            state = row[4]
            call_sign = ''
            lat = row[6].replace('+', '')
            lon = row[7].replace('+', '')
            elev = row[8].replace('+', '')
            begin = parser.parse(row[9]).isoformat()
            end = parser.parse(row[10]).isoformat()
            
            if wban == '99999':
                continue
            elif wban in wbans:
                continue
            elif lat and lon:
                location = 'SRID=4326;POINT(%s %s)' % (lon, lat)
                wbans.append(wban)
                all_rows.append([wban, name, country, state, 
                    call_sign, location, elev, begin, end])
        writer = UnicodeCSVWriter(self.clean_station_info)
        writer.writerow(header)
        writer.writerows(all_rows)
        self.clean_station_info.seek(0)

    def _make_station_table(self):
        self.station_table = Table('weather_stations', Base.metadata,
                Column('wban_code', String(5), primary_key=True),
                Column('station_name', String(100), nullable=False),
                Column('country', String(2)),
                Column('state', String(2)),
                Column('call_sign', String(5)),
                Column('location', Geometry('POINT', srid=4326)),
                Column('elevation', Float),
                Column('begin', Date),
                Column('end', Date))
        self.station_table.create(engine, checkfirst=True)

    def _load(self):
        names = [c.name for c in self.station_table.columns]
        ins_st = "COPY weather_stations FROM STDIN WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',')"
        conn = engine.raw_connection()
        cursor = conn.cursor()
        cursor.copy_expert(ins_st, self.clean_station_info)
        conn.commit()
        return 'bluh'
    
    def _update_stations(self):
        reader = UnicodeCSVDictReader(self.clean_station_info)
        conn = engine.connect()
        for row in reader:
            station = session.query(self.station_table).filter(self.station_table.c.wban_code == row['wban_code']).all()
            if not station:
                ins = self.station_table.insert().values(**row)
                conn.execute(ins)


        
        
