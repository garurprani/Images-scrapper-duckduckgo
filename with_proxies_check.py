import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import random
from colorama import Fore, Back, Style, init
import time
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)

def get_random_proxy(proxies_df):
    random_row = proxies_df.sample()
    ip = random_row.iloc[0]['ip']
    port = random_row.iloc[0]['port']
    username = random_row.iloc[0]['username']
    password = random_row.iloc[0]['password']
    proxy_url = f"http://{username}:{password}@{ip}:{port}"
    return {
        'http': proxy_url,
        'https': proxy_url
    }

def header_msg():
    if action_choice == '1':
        os.system('cls')
        print(Fore.MAGENTA + " Welcome to the Duck IMAGE Fetcher!")
        print(Fore.WHITE + Back.LIGHTBLACK_EX + " ~~~~~~~> ", Fore.BLACK + Back.MAGENTA + " scripted by @garurprani ")
        print("------------------------------------")
        print()


def fetch_duckduckgo_image_urls(query, num_images=300, proxies_df=None):
    base_url = 'https://duckduckgo.com/'
    search_url = f"{base_url}?q={query}&iax=images&ia=images"
    image_urls = []

    try:
        while len(image_urls) < num_images:
            user_agent = UserAgent().random
            headers = {
                "User-Agent": user_agent
            }
            if proxies_df is not None:
                proxies = get_random_proxy(proxies_df)
            else:
                proxies = None

            response = requests.get(search_url, headers=headers, proxies=proxies, verify=True)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            vqd_pattern = re.compile(r'vqd=([\d-]+)')
            script_tags = soup.find_all('script')
            for script in script_tags:
                match = vqd_pattern.search(str(script))
                if match:
                    vqd = match.group(1)
                    break
            else:
                raise ValueError("vqd parameter not found in DuckDuckGo search page HTML.")

            page = 1
            while len(image_urls) < num_images:
                api_url = f"{base_url}i.js?q={query}&o=json&p={page}&s={len(image_urls)}&u=bing&f=,,,,,&l=us-en&vqd={vqd}&product_ad_extensions_exp=b"

                response = requests.get(api_url, headers=headers, proxies=proxies)
                if response.status_code == 200:
                    data = response.json()
                    new_image_urls = [result['image'] for result in data['results'] if 'image' in result]
                    image_urls.extend(new_image_urls)
                    if not new_image_urls:
                        break
                    page += 1
                else:
                    raise ValueError(Fore.RED + f"[-] Failed to fetch image URLs. Status code: {response.status_code}")

                time.sleep(random.uniform(1, 3))

            return len(image_urls[:num_images])

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[-] Error fetching data from DuckDuckGo: {e}")
        return 0
    except Exception as e:
        print(f"Exception occurred: {e}")
        return 0

def fetch_images_for_keywords_in_excel(excel_file, proxies_file, use_multithreading=False):
    print()
    os.system('cls')
    print(Fore.MAGENTA + " Welcome to the Duck IMAGE Fetcher!")
    print(Fore.WHITE + Back.LIGHTBLACK_EX + " ~~~~~~~> ", Fore.BLACK + Back.MAGENTA + " scripted by @garurprani ")
    print("------------------------------------")
    print()
    print(Fore.BLUE + "[+] Loading Excel file...")
    try:
        df = pd.read_excel(excel_file, engine='openpyxl')
        proxies_df = pd.read_excel(proxies_file, engine='openpyxl', names=['ip', 'port', 'username', 'password'])
    except Exception as e:
        print(Fore.RED + f"[-] Error loading Excel file: {e}")
        return
    print(Fore.BLACK + Back.GREEN + "[+] Excel file loaded successfully. ")
    print()

    directory = os.path.join(os.getcwd(), 'output')
    if not os.path.exists(directory):
        os.makedirs(directory)

    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column].dtype):
            continue

        column_name = column
        keyword_counts = {}

        if use_multithreading:
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = []
                for idx, keyword in enumerate(df[column], start=1):
                    if pd.isna(keyword):
                        continue

                    print(Fore.BLUE + "[+]" + Fore.GREEN + f" Fetching images for keyword '{keyword}' in column '{column_name}'...")
                    futures.append(
                        executor.submit(fetch_duckduckgo_image_urls, keyword, 300, proxies_df)
                    )

                for future in as_completed(futures):
                    try:
                        image_count = future.result()
                        if image_count:
                            keyword_counts[df[column][idx]] = image_count

                    except Exception as e:
                        print(Fore.RED + f"[+] Failed to fetch images: {e}")

        else:
            for idx, keyword in enumerate(df[column], start=1):
                if pd.isna(keyword):
                    continue

                print(Fore.BLUE + "[+]" + Fore.GREEN + f" Fetching images for keyword '{keyword}' in column '{column_name}'...")
                try:
                    image_count = fetch_duckduckgo_image_urls(keyword, 300, proxies_df)
                    keyword_counts[keyword] = image_count

                    time.sleep(random.uniform(1, 3))

                except Exception as e:
                    print(Fore.RED + f"[+] Failed to fetch images for '{keyword}' in column '{column_name}': {e}")

        all_keyword_counts_df = pd.DataFrame({'Keyword': list(keyword_counts.keys()), 'URL Count': list(keyword_counts.values())})
        all_keyword_counts_filename = os.path.join(directory, f"{column_name}_url_counts.xlsx")
        all_keyword_counts_df.to_excel(all_keyword_counts_filename, index=False)
        print(Fore.GREEN + f"Saved URL counts to '{all_keyword_counts_filename}'")

def check_proxy(proxy):
    ip = proxy['ip']
    port = proxy['port']
    username = proxy['username']
    password = proxy['password']
    proxy_url = f"http://{username}:{password}@{ip}:{port}"
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }
    url = 'https://www.duckduckgo.com/'
    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        if response.status_code == 200:
            print(Fore.GREEN + f"[+] Proxy {ip}:{port} is working.")
            return True
        else:
            print(Fore.RED + f"[-] Proxy {ip}:{port} is dead. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        print(Fore.RED + f"[-] Proxy {ip}:{port} is dead.")
        return False

def remove_dead_proxies(proxies_df):
    print(Fore.BLUE + "[+] Checking proxies...")
    
    # Use ThreadPoolExecutor for concurrent proxy checking
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(check_proxy, row.to_dict()): index for index, row in proxies_df.iterrows()}
        
        dead_proxies = []
        for future in as_completed(futures):
            index = futures[future]
            if not future.result():
                dead_proxies.append(index)

    if dead_proxies:
        print(Fore.YELLOW + "\n[?] Remove dead proxies (Y/N)")
        choice = input(Fore.BLUE + "[=] Enter your choice: " + Fore.GREEN).strip().lower()
        if choice == 'y':
            proxies_df.drop(index=dead_proxies, inplace=True)
            print(Fore.GREEN + "[+] Dead proxies removed successfully.")
        else:
            print(Fore.YELLOW + "[!] Dead proxies were not removed.")
    else:
        print(Fore.GREEN + "[+] All proxies are working.")

def check_proxies_and_remove_dead(proxies_file):
    try:
        proxies_df = pd.read_excel(proxies_file, engine='openpyxl', names=['ip', 'port', 'username', 'password'])
    except Exception as e:
        print(Fore.RED + f"[-] Error loading proxies file: {e}")
        return

    remove_dead_proxies(proxies_df)
    proxies_df.to_excel(proxies_file, index=False)

if __name__ == "__main__":
    os.system('cls')
    print(Fore.MAGENTA + " Welcome to the Duck IMAGE Fetcher!")
    print(Fore.WHITE + Back.LIGHTBLACK_EX + " ~~~~~~~> ", Fore.BLACK + Back.MAGENTA + " scripted by @garurprani ")
    print("------------------------------------")
    print()

    print(Fore.BLUE + "[*] " + Fore.GREEN + "Choose an option:")
    print()
    print(Fore.WHITE + Back.LIGHTBLACK_EX + " 1 ", Fore.BLACK + Back.BLUE + " Enter the path to your Excel file              ")
    print(Fore.WHITE + Back.LIGHTBLACK_EX + " 2 ", Fore.BLACK + Back.BLUE + " Use default (Excel file in the same directory) ")
    print()
    choice = input(Fore.BLUE + "[=] " + Fore.GREEN + "Enter your choice (1 or 2): ").strip()

    if choice == '1':
        os.system('cls')
        print(Fore.MAGENTA + " Welcome to the Duck IMAGE Fetcher!")
        print(Fore.WHITE + Back.LIGHTBLACK_EX + " ~~~~~~~> ", Fore.BLACK + Back.MAGENTA + " scripted by @garurprani ")
        print("------------------------------------")
        print()
        excel_file = input(Fore.BLUE + "[=] " + Fore.GREEN + "Enter the path to your Excel file: ").strip()
        proxies_file = input(Fore.BLUE + "[=] " + Fore.GREEN + "Enter the path to your proxies file: ").strip()
    elif choice == '2':
        excel_file = 'keywords.xlsx'
        proxies_file = 'proxies.xlsx'
    else:
        print(Fore.RED + "[-] Invalid choice. Exiting.")
        exit()

    print()
    os.system('cls')
    print(Fore.MAGENTA + " Welcome to the Duck IMAGE Fetcher!")
    print(Fore.WHITE + Back.LIGHTBLACK_EX + " ~~~~~~~> ", Fore.BLACK + Back.MAGENTA + " scripted by @garurprani ")
    print("------------------------------------")
    print()
    print(Fore.BLUE + "[*] " + Fore.GREEN + "Choose an option: ")
    print()
    print(Fore.WHITE + Back.LIGHTBLACK_EX + " 1 ", Fore.BLACK + Back.BLUE + " Check proxies ")
    print(Fore.WHITE + Back.LIGHTBLACK_EX + " 2 ", Fore.BLACK + Back.BLUE + " Start fetching images ")
    print()
    action_choice = input(Fore.BLUE + "[=] " + Fore.GREEN + "Enter Your Choice: ").strip().lower()

    if action_choice == '1':
        os.system('cls')
        print(Fore.MAGENTA + " Welcome to the Duck IMAGE Fetcher!")
        print(Fore.WHITE + Back.LIGHTBLACK_EX + " ~~~~~~~> ", Fore.BLACK + Back.MAGENTA + " scripted by @garurprani ")
        print("------------------------------------")
        print()
        check_proxies_and_remove_dead(proxies_file)
    elif action_choice == '2':
        fetch_images_for_keywords_in_excel(excel_file, proxies_file, use_multithreading=True)
    else:
        print(Fore.RED + "[-] Invalid choice. Exiting.")

    fetch_images_for_keywords_in_excel(excel_file, proxies_file, use_multithreading=True)
