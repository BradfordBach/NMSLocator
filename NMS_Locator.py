import json
import os
import datetime
import time
import pyperclip

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
    if galactic_address in location_log:
        return True

def enter_address_into_log(galactic_address, dt):
    with open(log_loc, "a") as log:
        log.write(dt.strftime("%B %d %I:%M:%S %p") + ',' + galactic_address + '\n')

def format_galaxtic_coord(x, y, z, ssi):
    fmt = "{0:0{1}X}"
    parts = [str(fmt.format(x + 2047, 4)), str(fmt.format(y + 127, 4)), str(fmt.format(z + 2047, 4)), str(fmt.format(ssi,4))]
    return(':'.join(parts))

def load_log():
    log_dir = os.getenv('LOCALAPPDATA') + os.sep + 'Programs' + os.sep + "NMS Locator"
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
            location_log.append(line.split(',')[1])
            line = log.readline().strip()

    return location_log, log_dir + os.sep + "location_log.log"

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

location_log, log_loc = load_log()
save = get_latest_save_file()
mod_times = []
print("Waiting for new locations every 15 seconds.\nNew locations will be copied to clipboard and displayed...")
run_location_gatherer()
