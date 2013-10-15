#! /usr/bin/python

#Simple python program
import os
import time
import subprocess
home = os.getenv("HOME")

def update_tle():
    # Open list of satellites to copy TLEs
    satlist_filename = os.getcwd() + '/id_list'
    satlist_file = open(satlist_filename)
    satlist = (satlist_file.readlines())
    satlist_file.close()

    # Open the TLE file to be read by predict
    tle_dest_filename = os.getcwd() + '/predict.tle'
    tle_dest_file = open(tle_dest_filename,'w')

    for satid in satlist:
        tle_source_filename = home + '/.config/Gpredict/satdata/' + satid.rstrip('\n') + '.sat'
        tle_source_file = open(tle_source_filename)
        tle_source_data = tle_source_file.read()
        tle_source_file.close()
        sat_TLE1 = (tle_source_data.split('\n')[5])[5:]
        sat_name = sat_TLE1[2:7]
        sat_TLE2 = (tle_source_data.split('\n')[6])[5:]
        tle_dest_file.write(sat_name + '\n' + sat_TLE1 + '\n' + sat_TLE2 + '\n')
        tle_dest_file.flush()
    tle_dest_file.close()


def main():
    reset_hour = 4
    while True:

        update_tle()
        with open('/dev/null', "w") as fnull:
            predict_service = subprocess.Popen(['predict', '-s', '-t', os.getcwd() + '/predict.tle'], stdout = fnull, stderr = fnull)

        time.sleep(3600)

        while not time.gmtime().tm_hour == reset_hour:
            time.sleep(3600)

        predict_service.terminate()        

if __name__ == "__main__":
    main()

