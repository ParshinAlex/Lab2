import pandas as pd
import os, os.path
import glob
import requests
import datetime

main_folder = "D:\Python\Lab2\collected_data"
minYear = 1982
maxYear = 2020


# Accessory functions

def clean_data(directory, index):
    os.chdir(directory)
    for file in glob.glob(os.path.join(directory, "province_{}*.csv".format(index))):
        os.remove(file)


def get_index():
    print('Please, insert index of a province: ')
    index = int(input())
    while True:
        if (index > 27) or (index < 1):
            print('Invalid input. Please, try again:')
        else:
            return index


def get_year():
    print('Please, insert year: ')
    year = int(input())
    while True:
        if (year < minYear) or (year > maxYear):
            print('Invalid input. Please, try again:')
        else:
            return year


def prepare_data(line):
    if '<pre>' in line:
        buffer = line.split('<pre>')
        line = buffer[1]
    if '</pre>' in line:
        return ''
    if '-1.00' in line:
        return ''
    return (line + '\n')


# Downloading functions

def download_province(folder, index):
    url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1={}&year2={}&type=Mean".format(
        index, minYear, maxYear)
    response = requests.get(url)
    path = os.path.join(folder,
                        "province_{}_{}.csv".format(index, datetime.datetime.today().strftime("%d-%m-%Y %H-%M")))
    with open(path, 'w') as file:
        file.write("Year,Week,SMN,SMT,VCI,TCI,VHI\n")
        for line in response.iter_lines(chunk_size=512, decode_unicode=True):
            file.write(prepare_data(line))
        file.close()
    print('Province {} is ready to use.'.format(index))


def download_all_provinces():
    for i in range(1, 28):
        clean_data(main_folder, i)
        download_province(main_folder, i)


# Getting/Printing DataFrame functions

def get_df(folder, index):
    df = pd.DataFrame(columns=['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI'])
    os.chdir(folder)
    csv_path = glob.glob('province_{}_*.csv'.format(index))
    df = pd.read_csv(csv_path[0], index_col=False)
    # df['Province'] = index     # Remove / add id of a province
    return df


def get_merged_df(folder):
    df = pd.DataFrame(columns=['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI'])
    os.chdir(folder)
    for file in glob.glob(os.path.join(folder, "province_*.csv")):
        temp = pd.read_csv(file, header=0, index_col=False)
        # temp['Province'] = file.split('_')[2]      # Remove / add id of a province
        df = df.append(temp, ignore_index=True)
    return df


def print_df(dataframe):
    print(dataframe)

# Main function

def main():
    while True:
        print('----------------------------------------------')
        print('This is the main menu of a Laboratory Work 1. \n'
              '1. Download one province \n'
              '2. Download all provinces \n'
              '3. Create and print DataFrame of one province \n'
              '4. Create and print DataFrame of all provinces\n'
              '0. Exit\n'
              'Please, choose number: \n')
        key = int(input())
        if key == 0:
            break
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
        else:
            print('Invalid input. Please, try again.')


if __name__ == '__main__':
    main()
