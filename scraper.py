from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from time import sleep
import os
import requests
import argparse

def main(profile):
    if not os.path.exists('video_urls.txt'):
        print('[*] Output file with video URLs not found, now grabbing all video URLs')
        driver = webdriver.Firefox()
        driver.get(profile)
        scroll_down(driver)
        urls = grab_urls(driver)
        videos = grab_video_urls(driver, urls)
        videos_str = [ f'{i[0]}|{i[1]}' for i in videos ]

        with open('video_urls.txt','w') as f:
            f.write('\n'.join(videos_str))

        driver.quit()

    if not os.path.exists('video_out'):
        print('[*] No video_out directory found, creating one now')
        os.makedirs('video_out')
    else:
        print('[!] video_out directory already exists, exiting to prevent overwriting of videos. Please move/delete the folder before running again')
        return

    lines = []
    with open('video_urls.txt', 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        title, url = line.strip().split('|')
        while True:
            print(f'[*] Downloading {title} from {url}')
            try:
                with requests.get(url, stream=True, allow_redirects=True) as r:
                    r.raise_for_status()
                    with open(f'video_out/{title}.mp4', 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            f.write(chunk)
                break
            except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError):
                print('[!] Connection error, automatically retrying')
                continue

def scroll_down(driver):
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(8)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            print('[*] Done scrolling down')
            break
        last_height = new_height

def grab_urls(driver):
    url_elements = driver.find_elements_by_css_selector('.bd .video-list-container a.title')
    urls = [url_element.get_attribute('href').split('?')[0] for url_element in url_elements] # grabs the non-wayback url
    urls = [f'https://web.archive.org/web/{url}' for url in urls]
    print('[*] Done grabbing urls')
    return urls

def grab_video_urls(driver, urls):
    video_urls = []
    for url in urls:
        title = f"{url.split('/')[-1]}-{url.split('/')[-2]}" # format name-id
        while True:
            try:
                print(url)
                driver.get(url)
                video = driver.find_element_by_css_selector('.ui-player > video:nth-child(2)')
                video_urls.append( (title, f"https://web.archive.org/web/{'/'.join(video.get_attribute('poster').split('/')[:-1])}/720.mp4") )
                print(f'{title} {video_urls[-1]}')
                break
            except NoSuchElementException:
                print(f'[!] {title} not archived - skipping')
                break
            except WebDriverException:
                print(f'[!] WebDriverException, retrying')
                continue
    return video_urls

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('profile', help='plays.tv profile URL from web.archive.org (should end with /u/<your username>)')
    args = parser.parse_args()

    main(args.profile)
