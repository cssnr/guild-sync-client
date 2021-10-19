from slpp import slpp
import os
import requests
import time
import urllib3

urllib3.disable_warnings()

#GUILD_SYNC_URL = 'http://192.168.1.51:8000/client'
GUILD_SYNC_URL = 'https://192.168.1.51/client'
GUILD_SYNC_DB = {}
headers = dict


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
    lua_file = r'C:\Program Files (x86)\World of Warcraft\_classic_\WTF\Account\SMASHED926\SavedVariables\GuildSync.lua'
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
        print('Sync complete.')


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
            print('Caught Exception: {}'.format(error))
            time.sleep(5)
            continue
