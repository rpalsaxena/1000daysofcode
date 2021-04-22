from datetime import date
from nsepy import get_history
import pandas as pd
import os
import datetime
import tqdm

def download_contract(symbol, n, exdate, pexdate,  is_index = False):
    #exdate = datetime.datetime.strptime(ex_date, '%d-%m-%Y').date()
    #pexdate = datetime.datetime.strptime(pex_date, '%d-%m-%Y').date()
    #print(exdate)
    df = get_history(symbol=symbol,
                        start=pexdate,
                        end=exdate,
                        index=  is_index,
                        futures=True,
                        expiry_date= exdate)
    #print(df)
    if not os.path.exists(symbol):
        os.makedirs(symbol)
    df.to_csv('./'+symbol+'/'+symbol+'_'+str(n)+'_'+str(exdate))
    print("  Successfully Saved "+'./'+symbol+'/'+symbol+'_'+str(n)+'_'+str(exdate))

dir_name = './NIFTY/'
#os.chdir(dir_name) # change directory from working dir to dir with files
file_count = 0
for path, dir_list, file_list in os.walk(dir_name):
    file_count = len(file_list)
print("-----------------------------------------")
print("Gonna save with file count :", file_count)
print("-----------------------------------------")

from nsepy.derivatives import get_expiry_date


def get_exdates():
    current_month = datetime.datetime.today().month
    current_year = datetime.datetime.today().year
    current_date = datetime.datetime.today().date()

    cex = list(get_expiry_date(year=current_year, month=current_month))
    pex = list(get_expiry_date(year=current_year, month=current_month - 1))

    cex.sort()

    if cex[-1] < current_date:
        cex = list(get_expiry_date(year=current_year, month=current_month + 1))
        pex = list(get_expiry_date(year=current_year, month=current_month))

    pex.sort()

    return (cex[-1]), (pex[-1])

stk_symbols = ['INFY', 'RELIANCE', 'HINDUNILVR', 'TCS', 'KOTAKBANK', 'BAJAJFINSV',\
              'BAJFINANCE', 'LT', 'HDFCBANK', 'HDFC', 'TATAPOWER', 'INDUSINDBK', \
              'TATASTEEL']
for symbol in tqdm.tqdm(stk_symbols):
    try:
        download_contract(symbol, file_count+1, exdate=get_exdates()[0], pexdate=get_exdates()[1])
    except:
        print("Problem while processing "+symbol+"'s contract "+ str(date)+" value")
        continue
    print("  Successfully Downloaded contracts of"+symbol+"\n")


index = ['NIFTY', 'BANKNIFTY']
for symbol in tqdm.tqdm(index):
    try:
        download_contract(symbol, file_count+1 , exdate=get_exdates()[0], pexdate=get_exdates()[1], is_index= True)
    except:
        print("Problem while processing "+symbol+"'s contract "+ str(get_exdates()[0])+" value")
        continue
    print("  Successfully Downloaded contracts of"+symbol+"\n")