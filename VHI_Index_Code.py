import urllib.request
import pandas as pd
import os, os.path
import glob
import requests
import datetime

main_folder = "D:\Python\Lab2\collected_data"
pd.options.display.max_rows = 50000
minYear = 2005
maxYear = 2020

changedIndex = {1:24, 2:25, 3:5, 4:6, 5:27, 6:23, 7:26, 8:7, 9:11, 10:13, 11:14, 12:15, 13:16, 14:17, 15:18, 16:19, 17:21,
        18:22, 19:8, 20:9, 21:10, 22:1, 23:3, 24:2, 25:4, 26:12, 27:20}

def clean_data(directory, index):
    os.chdir(directory)
    for file in glob.glob(os.path.join(directory, "province{}*.csv".format(index))):
        os.remove(file)

def get_index():
    print('Please, insert index of a province: ')
    index = int(input())
    while True:
        if ((index > 27) or (index < 1)): print('Invalid input. Please, try again:')
        else: return index

def get_year():
    print('Please, insert year: ')
    year = int(input())
    while True:
        if ((year < minYear) or (year > maxYear)): print('Invalid input. Please, try again:')
        else: return year

def prepare_data(line):
    if '<pre>' in line:
        buffer = line.split('<pre>')
        line = buffer[1]
    if '</pre>' in line:
        return ''
    if '-1.00' in line:
        return ''
    return (line + '\n')

def download_province(folder, index):
    url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1={}&year2={}&type=Mean".format(changedIndex[index], minYear, maxYear)
    response = requests.get(url)
    path = os.path.join(folder, "province{}_{}.csv".format(index, datetime.datetime.today().strftime("%d-%m-%Y_%H-%M")))
    with open(path, 'w') as file:
        file.write("Year,Week,SMN,SMT,VCI,TCI,VHI\n")
        for line in response.iter_lines(chunk_size=512, decode_unicode=True):
            file.write(prepare_data(line))
        file.close()
    print('Province {} is ready to use.'.format(index))

def download_all_provinces():
    for i in range (1, 28):
        clean_data(main_folder, i)
        download_province(main_folder, i)

def get_df(folder, index):
    df = pd.DataFrame(columns=['Year','Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI'])
    os.chdir(folder)
    csv_path = glob.glob('province{}*.csv'.format(index))
    df = pd.read_csv(csv_path[0], index_col= False)
    df['provinceID'] = index
    return(df)

def get_merged_df(folder):
    df = pd.DataFrame(columns=['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI'])
    os.chdir(folder)
    csv_paths = glob.glob('province*.csv')
    dfs = []
    for path in csv_paths:
        dfs_x = pd.read_csv(path, index_col=False)
        dfs_x['provinceID'] = path.split("_")[0][8:]
        dfs.append(dfs_x)
    df = pd.concat(dfs)
    return(df)

def vhi_province(folder):
    index = get_index()
    year = get_year()
    df = get_df(folder, index)
    df = df[['Year', 'Week', 'VHI']]
    df = df[df['Year'] == year]
    print_df(df)
    print('Maximum value of VHI:')
    print(df['VHI'].max())
    print('Minimum value of VHI: ')
    print(df['VHI'].min())
    print('Average value of VHI: ')
    print(df['VHI'].mean())

def vhi_province_critical_droughts(folder):
    index = get_index()
    df = get_df(folder, index)
    df = df[['Year', 'Week', 'VHI']]
    modded_df = df[df['VHI'] < 15][['Year', 'Week', 'VHI']]
    modded_df = modded_df.groupby(['Year']).mean()
    print_df(modded_df)

def vhi_province_temperate_droughts(folder):
    index = get_index()
    df = get_df(folder, index)
    df = df[['Year', 'Week', 'VHI']]
    modded_df = df[(df['VHI'] < 35) & (df['VHI'] > 15)][['Year', 'Week', 'VHI']]
    modded_df = modded_df.groupby(['Year']).mean()
    print_df(modded_df)

def custom_function(folder):
    #index = get_index()
    #df = get_df(folder, index)
    df = get_merged_df()
    modded_df = df['VHI'].max()

def print_df(dataframe):
    print(dataframe)

def main():
    for i in range (1, 28): clean_data(main_folder, i)
    while True:
        print('----------------------------------------------')
        print('This is the main menu of a Laboratory Work 1.')
        print('1. Download one province')
        print('2. Download all provinces')
        print('3. Create and print DataFrame of one province')
        print('4. Create and print DataFrame of all provinces')
        print('5. VHI for province (1 year), min / max / average values')
        print('6. VHI for province (all years), critical droughts')
        print('7. VHI for province (all years), temperate droughts')
        print('8. Custom function')
        print('0. Exit')
        print('Please, choose number: ')
        key = int(input())
        if key == 0: break
        elif key == 1:
            index = get_index()
            download_province(main_folder, index)
        elif key == 2:
            download_all_provinces()
        elif key == 3:
            index = get_index()
            print_df(get_df(main_folder, index))
        elif key == 4:
            print_df(get_merged_df(main_folder))
        elif key == 5:
            vhi_province(main_folder)
        elif key == 6:
            vhi_province_critical_droughts(main_folder)
        elif key == 7:
            vhi_province_temperate_droughts(main_folder)
        elif key == 8:
            custom_function(main_folder)
        else: print('Invalid input. Please, try again.')

if __name__ == '__main__':
    main()