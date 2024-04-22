from requests import get
from pandas import DataFrame, read_html
from bs4 import BeautifulSoup
from re import sub as replace

def main() -> None:
    request = get( 'http://free-proxy.cz/en/proxylist/country/all/https/ping/all' )
    instance = BeautifulSoup( request.text, 'html.parser' )
    dataframe: DataFrame = read_html( str(instance.find( 'table', { 'id': 'proxy_list' } )) )[0]
    proxies: DataFrame = dataframe[['IP address', 'Port']]
    ips_to_decode = proxies['IP address'].apply( lambda ip: replace( r'.*\"(.*)\".*', r'\1', ip ) )
    print( ips_to_decode )




if __name__ == '__main__':
    main()