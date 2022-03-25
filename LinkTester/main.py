from os import getlogin
import pandas as pd
import urllib.parse
import urllib.request
import logging

logging.basicConfig(filename='links.log', filemode='w', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('LINKS')


def urlcheck():
    with open('.\Links.csv') as csvfile:
        df = pd.DataFrame(csvfile, columns=['Link'])
        for ind in df.index:
            try:
                row = str(df['Link'][ind])
                row = row.strip("\n")
                row = urllib.parse.quote(row, safe='-/:')
                print(row)
                urllib.request.urlopen(row)
            except Exception as e:
                logger.error(f"URL inativa - {row}")
                print(e)


if __name__ == '__main__':
    urlcheck()
