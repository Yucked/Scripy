import requests
import random
from random import randint
import string

user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
               'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
               'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1']

countries = ['AF', 'AX', 'AL', 'DZ', 'AS', 'AD', 'AO', 'AI', 'AQ', 'AG', 'AR', 'AM', 'AW', 'AU', 'AT', 'AZ', 'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ',
             'BM', 'BT', 'BA', 'BW', 'BV', 'BR', 'IO', 'BN', 'BG', 'BF', 'BI', 'KH', 'CM', 'CA', 'CV', 'KY', 'CF', 'TD', 'CL', 'CN', 'CX', 'CC', 'CO', 'KM',
             'CG', 'CK', 'CR', 'CI', 'HR', 'CU', 'CW', 'CY', 'CZ', 'DK', 'DJ', 'DM', 'DO', 'EC', 'EG', 'SV', 'GQ', 'ER', 'EE', 'ET', 'FK', 'FO', 'FJ', 'FI',
             'FR', 'GF', 'PF', 'TF', 'GA', 'GM', 'GE', 'DE', 'GH', 'GI', 'GR', 'GL', 'GD', 'GP', 'GU', 'GT', 'GG', 'GN', 'GW', 'GY', 'HT', 'HM', 'VA', 'HN',
             'HK', 'HU', 'IS', 'IN', 'ID', 'IQ', 'IE', 'IM', 'IL', 'IT', 'JM', 'JP', 'JE', 'JO', 'KZ', 'KE', 'KI', 'KW', 'KG', 'LA', 'LV', 'LB', 'LS', 'LR',
             'LY', 'LI', 'LT', 'LU', 'MO', 'MG', 'MW', 'MY', 'MV', 'ML', 'MT', 'MH', 'MQ', 'MR', 'MU', 'YT', 'MX', 'MC', 'MN', 'ME', 'MS', 'MA', 'MZ', 'MM',
             'NA', 'NR', 'NP', 'NL', 'NC', 'NZ', 'NI', 'NE', 'NG', 'NU', 'NF', 'MP', 'NO', 'OM', 'PK', 'PW', 'PA', 'PG', 'PY', 'PE', 'PH', 'PN', 'PL', 'PT',
             'PR', 'QA', 'RE', 'RO', 'RU', 'RW', 'BL', 'KN', 'LC', 'MF', 'PM', 'VC', 'WS', 'SM', 'ST', 'SA', 'SN', 'RS', 'SC', 'SL', 'SG', 'SX', 'SK', 'SI',
             'SB', 'SO', 'ZA', 'GS', 'SS', 'ES', 'LK', 'SD', 'SR', 'SJ', 'SZ', 'SE', 'CH', 'SY', 'TJ', 'TH', 'TL', 'TG', 'TK', 'TO','TT', 'TN', 'TR', 'TM',
             'TC', 'TV', 'UG', 'UA', 'AE', 'GB', 'US', 'UM', 'UY', 'UZ', 'VU', 'VN', 'WF', 'EH', 'YE', 'ZM', 'ZW']

def get_browser_id(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def get_session_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=25))

def get_headers(country):
    headers = {'User-Agent': random.choice(user_agents),
               'Cache-Control': 'max-age=0, no-cache',
               'Origin': 'https://store.steampowered.com',
               'Pragma': 'no-cache',
               'Cookie': 'browserid={}; steamCountry={}; sessionid={};'.format(get_browser_id(20), country, get_session_id()),
               'Content-Length': '24',
               'DNT': '1',
               'Connection': 'keep-alive'}

    return headers

def get_proxy_data():
    result = requests.get('http://pubproxy.com/api/proxy?type=http')
    json_result = result.json()['data'][0]
    protocol = json_result['type']
    proxy = {protocol : '{}://{}'.format(protocol, json_result['ipPort'])}
    return proxy, json_result['country']

try:
    while True:
        username = input('Please enter username:')
        data = {'accountname': username,'count': '100'}

        proxy_data = get_proxy_data()
        result = requests.post("https://store.steampowered.com/join/checkavail/", data = data, headers = get_headers(proxy_data[1]), proxies = proxy_data[0])
        result_json = result.json()
        available = result_json.get('bAvailable')
        suggestions = len(result_json.get('rgSuggestions'))
        is_avail = available and suggestions == 0
        
        print('{}: {}'.format(u'\u2713', username) if is_avail else '{}: {}'.format(u'\u274C', username))
except KeyboardInterrupt:
    print('Exited!')
