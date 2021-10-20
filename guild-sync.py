import os
import requests
import time
import urllib3
import tkinter as tk
from slpp import slpp
from tkinter import filedialog

urllib3.disable_warnings()
headers = dict
GUILD_SYNC_DB = {}
GUILD_SYNC_URL = 'https://dev.guildsync.cc/client'


def auth():
    print('Authenticating...')
    data_folder = os.path.join(os.environ['APPDATA'], 'GuildSync')
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    data_file = os.path.join(data_folder, 'access-key')
    if not os.path.exists(data_file):
        access_key = input('\nAccess Key: ').strip()
        with open(data_file, 'w', encoding='utf-8') as f:
            f.write(access_key)
    else:
        with open(data_file, 'r', encoding='utf-8') as f:
            access_key = f.read().strip()

    global headers
    headers = {'Access-Key': access_key}
    r = requests.post(GUILD_SYNC_URL + '/auth/', headers=headers, verify=False)
    if not r.ok:
        print('Login Error: ')
        r.raise_for_status()
    else:
        if r.content.decode('utf-8') == 'auth-fail':
            print('Auth Failure!')
            raise Exception('AuthFailure')
        print(r.content.decode('utf-8'))


def main():
    print('Please select your WTF Account folder.')
    print('Example for username "Test123":')
    print(r'C:\Program Files (x86)\World of Warcraft\_classic_\WTF\Account\Test123')
    root = tk.Tk()
    root.withdraw()
    wow_dir = ''
    while not os.path.isdir(os.path.join(wow_dir, 'SavedVariables')):
        print('This directory seems invalid, try again...')
        wow_dir = filedialog.askdirectory(initialdir=r'C:\Program Files (x86)\World of Warcraft\_classic_\WTF\Account')
    lua_file = os.path.join(wow_dir, r'SavedVariables\GuildSync.lua')
    while not os.path.isfile(lua_file):
        print(f'Database file does not exist yet: {lua_file}')
        print(f'You must run the in-game addon, wait 30 seconds for a sync, and logout of the game.')
        print('Will check again in 30 seconds...')
        time.sleep(30)

    print(f'Using .lua file: {lua_file}')
    time.sleep(500)
    f = open(lua_file, 'r', encoding='utf-8')
    s = f.read()

    extra = s.split('{')[0]
    out = s.replace(extra, "")
    # extra = out.split('GuildDiscordSyncTime')[1]
    # extra = 'GuildDiscordSyncTime' + extra
    # out = out.replace(toRemove, "")
    data = slpp.decode(out)
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
    auth()
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
