#!/students/rchan85/myenvs/myenv/bin/python3

import sqlite3

from myairfieldpack import MYDBNAME, CSVFILE

csv_file = CSVFILE
dbname = MYDBNAME

### creates table for airfield info
def create_airfield_db(dbname):
    with sqlite3.connect(dbname) as conn:
        curs = conn.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS airfieldtable(
                "ident" TEXT,
                "type" TEXT,
                "name" TEXT,
                "gps_code" TEXT,
                "iata_code" TEXT,
                "local_code" TEXT
            );
          """
        curs.execute(sql)

### populates table with airfield info (codes, names)
def populate_airfield_db(dbname, csv_file):
    with sqlite3.connect(dbname) as conn:
        curs = conn.cursor()

        with open(csv_file, 'rt') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('id'):
                    continue
                ident, type, name, gps_code, iata_code, local_code = line.split(',')
                sql = """
                    INSERT INTO airfieldtable
                    VALUES(?,?,?,?,?,?)
                    """
                curs.execute(sql, (ident, type, name, gps_code, iata_code, local_code))


### searches table for codes matching user input
def search_airfield(input_code, dbname):
    with sqlite3.connect(dbname) as conn:
        curs = conn.cursor()
        sql = """SELECT * FROM airfieldtable
                 WHERE ident LIKE ?
                 OR gps_code LIKE ?
                 OR iata_code LIKE ?
              """
        code = (input_code, input_code, input_code,)
        curs.execute(sql, code)
        x = curs.fetchall()
        return x[0][0]
      
### searches table and returns name matching user input
def search_airfield_name(input_code, dbname):
    with sqlite3.connect(dbname) as conn:
        curs = conn.cursor()
        sql = """SELECT * FROM airfieldtable
                 WHERE ident LIKE ?
                 OR gps_code LIKE ?
                 OR iata_code LIKE ?
              """
        code = (input_code, input_code, input_code,)
        curs.execute(sql, code)
        x = curs.fetchall()
        return x[0][2]

if __name__ == '__main__':
    create_airfield_db(dbname)
    populate_airfield_db(dbname, csv_file)