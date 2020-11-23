TouchVPNSessionDefaults = {
    'max_download_delay': 1.5,
    'firefox_profile_dir': r"C:\\Users\\Kazi Samin Mubasshir\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\3hreiy45.default-release",
    'touchvpn_loc': r"C:\\Users\\Kazi Samin Mubasshir\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\3hreiy45.default-release\extensions\\touch-vpn@anchorfree.com.xpi",
    'start_with_vpn': False
}

TorSeleniumSessionDefaults = {
    'max_download_delay': 0.3,
    'firefox_profile_dir': r"C:\Users\Kazi Samin Mubasshir\AppData\Roaming\Mozilla\Firefox\Profiles\3hreiy45.default-release",
    'password': 'samin',
    'start_with_tor': False
}

MAX_RETRIES = 10                    # max no. of retries if a page throws errors
SAVE_RAW_HTML = True                # whether to save htmls
MAX_CONCURRENT_REQUESTS = 3         # no. of threads
SAVE_CRAWLER_STATE_INTERVAL = 2000  # no. of request after which crawler state should be saved