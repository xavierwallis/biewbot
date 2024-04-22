import pandas
from requests import get
from pandas import DataFrame, read_html, Series
from bs4 import BeautifulSoup
from re import sub as replace
from base64 import b64decode


def gather( page: int = 0 ) -> DataFrame:
    request = get( f'http://free-proxy.cz/en/proxylist/country/all/https/ping/all{ "/" if page else "" }{ page if page else "" }' )
    instance = BeautifulSoup( request.text, 'html.parser' )
    dataframe: DataFrame = read_html( str( instance.find( 'table', { 'id': 'proxy_list' } ) ) )[0]
    proxies: DataFrame = dataframe[['IP address', 'Port']]
    proxies = proxies.rename( columns={ 'IP address': 'ip_address', 'Port': 'port' } )
    proxies = proxies[proxies['port'].str.contains( 'adsbygoogle' ) == False]
    ips_to_decode: Series = proxies.ip_address.apply( lambda ip: replace( r'.*\"(.*)\".*', r'\1', ip ) )
    ip_list = ips_to_decode.apply( lambda x: str( b64decode( x ) )[2:-1] )
    proxies.ip_address = ip_list
    return proxies


def dump( proxies: DataFrame ) -> None:
    with open( 'proxy-dump.txt', 'w+' ) as file:
        for index, row in proxies.iterrows():
            file.write( f'{row.ip_address}:{row.port}\n' )


def main() -> None:
    data_list: list[DataFrame] = list()
    for page in range( 10 ):
        data_list.append( gather( page ) )
    proxies = pandas.concat( data_list )
    print(len(proxies))
    dump( proxies )  # None return


if __name__ == '__main__':
    main()
