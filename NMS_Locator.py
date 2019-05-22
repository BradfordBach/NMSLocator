import json
import os
import datetime
import time
import pyperclip
import winsound
import configparser
from shutil import copyfile

def get_current_location():
    with open(save, "r", encoding='utf-8') as save_file:
        save_file_string = save_file.read()[:-1]
    parsed_save = json.loads(save_file_string)

    json_player_data = parsed_save['6f=']["yhJ"]["oZw"]

    Player_State = {'x':json_player_data["dZj"], 'y':json_player_data['IyE'], 'z':json_player_data["uXE"], 'ssi':json_player_data['vby']}
    galactic_address = format_galaxtic_coord(Player_State['x'], Player_State['y'], Player_State['z'], Player_State['ssi'])

    if not check_if_address_exists(galactic_address):
        time_logged = datetime.datetime.now()
        enter_address_into_log(galactic_address, time_logged)
        print(time_logged.strftime("%B %d %I:%M:%S %p -> "), end='')
        print(galactic_address)
        pyperclip.copy(galactic_address)

        if config.getboolean('SETTINGS', 'PLAY_NOTIFICATION'):
            winsound.PlaySound('notification.wav', winsound.SND_FILENAME)

def get_file_mod_time():
    return os.path.getmtime(save)

def get_latest_save_file():
    all_save_files = []
    for(dirpath, dirnames, filenames) in os.walk(os.getenv('APPDATA') + os.sep + "HelloGames" + os.sep + "NMS"):
        for file in filenames:
            if file[-3:] == ".hg" and file[:3] != "mf_":
                all_save_files.append(os.path.join(dirpath, file))
    latest_save = max(all_save_files, key=os.path.getmtime)
    return latest_save

def check_if_address_exists(galactic_address):
    if any(galactic_address in entry for entry in location_log):
        return True

def is_date_in_log(date):
    for entry in location_log:
        if entry[0].date() == date.date():
            return True
    return False

def enter_address_into_log(galactic_address, dt):
    with open(log_loc, "a") as log:
        log.write(dt.strftime("%B %d %Y %I:%M:%S %p") + ',' + galactic_address + '\n')
    with open(log_dir + os.sep + "bulk.log", 'a') as bulk:
        if is_date_in_log(dt):
            bulk.write(galactic_address + '\n')
        else:
            bulk.write('\n' + dt.strftime("%B %d %Y") + '\n')
            bulk.write(galactic_address + '\n')

    location_log.append([dt, galactic_address])

def format_galaxtic_coord(x, y, z, ssi):
    fmt = "{0:0{1}X}"
    parts = [str(fmt.format(x + 2047, 4)), str(fmt.format(y + 127, 4)), str(fmt.format(z + 2047, 4)), str(fmt.format(ssi,4))]
    return(':'.join(parts))

def load_log():
    try:
        os.makedirs(log_dir)
    except FileExistsError:
        pass
    try:
        open(log_dir + os.sep + "location_log.log", 'r')
    except IOError:
        open(log_dir + os.sep + "location_log.log", 'w')

    location_log = []
    with open(log_dir + os.sep + "location_log.log") as log:
        line = log.readline().strip()
        while line:
            split_line = line.split(',')
            location_log.append([datetime.datetime.strptime(split_line[0], "%B %d %Y %I:%M:%S %p"), split_line[1]])
            line = log.readline().strip()

    return location_log, log_dir + os.sep + "location_log.log"

def create_bulk_log():
    if not os.path.isfile(log_dir + os.sep + "bulk.log"):
        try:
            open(log_dir + os.sep + "bulk.log", 'a')
        except IOError:
            open(log_dir + os.sep + "bulk.log", 'w')

        # convert existing location log into the new bulk format, this is only ever done once and only for people who used v0.2
        if os.path.getsize(log_dir + os.sep + "bulk.log") == 0:
            with open(log_dir + os.sep + "bulk.log", 'a') as bulk:
                location_dict = {}
                for location in location_log:
                    if location[0].strftime("%B %d %Y") not in location_dict:
                        location_dict[location[0].strftime("%B %d %Y")] = []
                    location_dict[location[0].strftime("%B %d %Y")].append(location[1])
                first = True
                for date, addresses in location_dict.items():
                    if first:
                        bulk.write(date + '\n')
                        first = False
                    else:
                        bulk.write('\n' + date + '\n')
                    for address in addresses:
                        bulk.write(address + '\n')

def add_years_to_location_log():
    # Add years to location_log file, because I forgot to do this on the first release
    if os.path.isfile(log_dir + os.sep + "location_log.log"):
        temp_log = []
        with open(log_dir + os.sep + "location_log.log", "r") as log:
            line = log.readline().strip()
            try:
                while line:
                    split_line = line.split(',')
                    temp_log.append([datetime.datetime.strptime(split_line[0], "%B %d %I:%M:%S %p"), split_line[1]])
                    line = log.readline().strip()

                    copyfile(log_dir + os.sep + "location_log.log", log_dir + os.sep + "location_log_backup.log")

                with open(log_dir + os.sep + "location_log.log", "w") as log:
                    for location in temp_log:
                        location[0] = location[0].replace(year=2019)
                        log.write(location[0].strftime("%B %d %Y %I:%M:%S %p") + ',' + location[1] + '\n')

            except ValueError:
                pass

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def run_location_gatherer():
    try:
        while True:
            if get_file_mod_time() not in mod_times:
                mod_times.append(get_file_mod_time())
                get_current_location()
            if len(mod_times) >= 200:
                mod_times.clear()
            time.sleep(15)
    except KeyboardInterrupt:
        pass

log_dir = os.getenv('LOCALAPPDATA') + os.sep + 'Programs' + os.sep + "NMS Locator"

config = load_config()
add_years_to_location_log()
location_log, log_loc = load_log()
create_bulk_log()
save = get_latest_save_file()
mod_times = []
print("Waiting for new locations every 15 seconds.\nNew locations will be copied to clipboard and displayed...")
run_location_gatherer()
