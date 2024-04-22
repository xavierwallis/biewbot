from multiprocessing.pool import ThreadPool

from psutil import process_iter
from sys import platform
from selenium import webdriver

from time import sleep
from random import random

base_duration_seconds = 60 * 3
random_duration_seconds = 60
macos: bool = platform == 'darwin'

def batch_proxies( batch_size: int = 12 ) -> list[str]:
    with open( 'proxies.txt', 'r' ) as file:
        index: int = 0
        try:
            while batch := file.readlines()[index:index + batch_size]:
                index += batch_size
                yield [ proxy.strip() for proxy in batch ]
        except IndexError:
            print( 'No more proxies' )
    return []


def add_view( proxy: str ) -> None:
    sleep( int( abs( random() * 12 - 6 ) ) )
    options = webdriver.SafariOptions() if macos else webdriver.ChromeOptions()
    options.add_argument( f'--proxy-server={proxy}' )  # None return
    #options.add_argument( '--headless' )
    service = None if macos else webdriver.ChromeService( executable_path='./chromedriver.exe' )
    driver = webdriver.Safari( options = options ) if macos else webdriver.Chrome( service = service, options = options )
    driver.get( 'https://www.youtube.com/watch?v=0B-n8-6ksBs' )  # None return
    sleep(
        base_duration_seconds * 4 + (random() * random_duration_seconds - random_duration_seconds / 2)
    )  # None return
    driver.quit()  # None return


def garbage_collector() -> None:
    for proc in process_iter():
        if proc.name() == 'Safari' or proc.name() == 'safaridriver':
            proc.kill()  # None return


def main() -> None:
    index: int = 0
    while proxies := list(batch_proxies())[0]:
        print( f'batch: { index + 1 }' )
        index += 1

        try:
            ThreadPool( len( proxies ) ).map( add_view, proxies )  # None return
        except Exception as error:
            print( error )

        if macos: garbage_collector()  # None return


if __name__ == '__main__':
    main()
