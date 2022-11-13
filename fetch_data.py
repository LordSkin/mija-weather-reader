import argparse
import MySQLdb
import lywsd03mmc

parser = argparse.ArgumentParser()
parser.add_argument('mac', help='MAC address of LYWSD02 device', nargs='+')
args = parser.parse_args()

for mac in args.mac:
    try:
        client = lywsd03mmc.Lywsd03mmcClient(mac)
        print('Fetching data from {}'.format(mac))
        data = client.data
        print('Temperature: {}°C'.format(data.temperature))
        print('Humidity: {}%'.format(data.humidity))
        print('Battery: {}%'.format(client.battery))
        print()

        sql = """INSERT INTO MijaSensor(deviceName,
          temperature, humidity)
          VALUES ('MijaSensor 1', '{0}', '{1}')"""

        db = MySQLdb.connect("192.168.1.40", "MijaSensor", "xiaomi", "MEASUREMENTS")

        cursor = db.cursor()

        # execute SQL query using execute() method.

        try:
            # Execute the SQL command
            cursor.execute(sql.format(data.temperature, data.humidity))
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()

        # disconnect from server
        db.close()

    except Exception as e:
        print(e)


