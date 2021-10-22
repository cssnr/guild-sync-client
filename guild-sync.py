import json
import os
import requests
import time
import urllib3
import tkinter as tk
from slpp import slpp
from tkinter import filedialog, simpledialog

urllib3.disable_warnings()
headers = dict
settings = dict
GUILD_SYNC_DB = {}
# GUILD_SYNC_URL = 'https://dev.guildsync.cc/client'
GUILD_SYNC_URL = 'https://dev01.cssnr.com/client'


def auth():
    print('Authenticating...')
    global headers
    headers = {'Access-Key': settings['access_key']}
    r = requests.post(GUILD_SYNC_URL + '/auth/', headers=headers, verify=False)
    if not r.ok:
        print('Login Error: ')
        r.raise_for_status()
    else:
        if r.content.decode('utf-8') == 'auth-fail':
            print('Auth Failure!')
            raise Exception('AuthFailure')
        print(r.content.decode('utf-8'))


def load_settings():
    global settings
    settings = {'access_key': '', 'lua_file': ''}
    data_folder = os.path.join(os.environ['APPDATA'], 'GuildSync')
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    settings_file = os.path.join(data_folder, 'settings.json')
    if not os.path.exists(settings_file):
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(settings))
    else:
        with open(settings_file, 'r', encoding='utf-8') as f:
            settings = json.loads(f.read().strip())

    if not settings['lua_file']:
        print('Please select your WTF Account Username folder.')
        print('Example for username: Test123')
        print(r'C:\Program Files (x86)\World of Warcraft\_classic_\WTF\Account\Test123')
        root = tk.Tk()
        root.withdraw()
        wow_dir = ''
        while not os.path.isdir(os.path.join(wow_dir, 'SavedVariables')):
            print('This directory seems invalid, try again...')
            wow_dir = filedialog.askdirectory(initialdir=r'C:\Program Files (x86)\World of Warcraft\_classic_\WTF\Account')
        lua_file = os.path.join(wow_dir, r'SavedVariables\GuildSync.lua')
        settings['lua_file'] = lua_file

    if not settings['access_key']:
        access_key = None
        while access_key is None:
            # access_key = input('\nAccess Key: ').strip()
            root = tk.Tk()
            root.withdraw()
            access_key = simpledialog.askstring(title="Access Key",
                                              prompt="Access Key from Website:")
        settings['access_key'] = access_key
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(settings))

    while not os.path.isfile(settings['lua_file']):
        print(f'Database file does not exist yet: {lua_file}')
        print(f'You must run the in-game addon, wait 30 seconds for a sync, and logout of the game.')
        print('Will check again in 30 seconds...')
        time.sleep(30)


def main():
    f = open(settings['lua_file'], 'r', encoding='utf-8')
    s = f.read()
    extra = s.split('{')[0]
    out = s.replace(extra, "")
    # extra = out.split('GuildDiscordSyncTime')[1]
    # extra = 'GuildDiscordSyncTime' + extra
    # out = out.replace(toRemove, "")
    data = slpp.decode(out)
    # print(data)
    if GUILD_SYNC_DB != data:
        print('Changes detected, syncing database now...')
        GUILD_SYNC_DB.clear()
        GUILD_SYNC_DB.update(data)
        r = requests.post(GUILD_SYNC_URL + '/upload/',
                          json=GUILD_SYNC_DB,
                          headers=headers,
                          verify=False)
        if not r.ok:
            print('Error sending data to server...')
            print(r.status_code)
            print(r.content)
        if r.content.decode('utf-8') == 'auth-fail':
            print('Auth Failure!')
            raise Exception('AuthFailure')
        print('Sync complete, sleeping until new cahnges detected...')


if __name__ == '__main__':
    load_settings()
    auth()
    print(f"Using .lua file: {settings['lua_file']}")
    while True:
        try:
            main()
            time.sleep(30)
        except (KeyboardInterrupt, SystemExit):
            print('Caught exit signal. Shutting down...')
            raise
        except Exception as error:
            print(f'Caught Exception: {error}')
            time.sleep(5)
            continue
