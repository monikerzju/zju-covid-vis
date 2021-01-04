import pandas as pd
import math
import os

print('Data are from https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series.')

print_country_name = False
print_global_data = False
print_country_data = True

last_date = '1/2/21'

def list_country():
    df = pd.read_csv('./src/assets/csv/time_series_covid19_confirmed_global.csv')
    countries_col = df['Country/Region']
    last_country = ""
    print('[')
    print("  '全球',")
    for i in range(len(df)):
        if countries_col[i] != last_country:
            print("  '" + countries_col[i].replace("'", "\\'") + "',")
        last_country = countries_col[i]
    print(']')

def format_string(date):
    splitted = date.split("/")
    ret = '20' + splitted[2] + '-'
    if int(splitted[0]) < 10:
        ret += '0'
    ret += splitted[0] + '-'
    if int(splitted[1]) < 10:
        ret += '0'
    ret += splitted[1]
    return ret

def calc_global_data():
    dfc = pd.read_csv('./src/assets/csv/time_series_covid19_confirmed_global.csv')
    dfd = pd.read_csv('./src/assets/csv/time_series_covid19_deaths_global.csv')
    dfr = pd.read_csv('./src/assets/csv/time_series_covid19_recovered_global.csv')
    print('[')
    total_confirm = -1
    total_death = -1
    total_cure = -1    
    for index, row in dfc.iteritems():
        if index != 'Province/State' and index != 'Country/Region' and index != 'Lat' and index != 'Long':
            last_total_confirm = total_confirm
            last_total_death = total_death
            last_total_cure = total_cure
            total_confirm = 0
            total_death = 0
            total_cure = 0
            for i in range(len(dfc)):
                total_confirm += dfc[index][i]
            for i in range(len(dfd)):
                total_death += dfd[index][i]
            for i in range(len(dfr)):
                total_cure += dfr[index][i]
            if last_total_confirm == -1:
                last_total_confirm = int(2 * total_confirm / 3)
            if last_total_cure == -1:
                last_total_cure = int(2 * total_cure / 3)
            if last_total_death == -1:
                last_total_death = int(2 * total_death / 3)
            print('  {')
            print("    \"date\": \"" + format_string(index) + "\",")
            print("    \"total_confirm\": " + str(total_confirm) + ",")
            print("    \"daily_confirm\": " + str(total_confirm - last_total_confirm) + ",")
            print("    \"total_death\": " + str(total_death) + ",")
            print("    \"daily_death\": " + str(total_death - last_total_death) + ",")
            print("    \"total_cure\": " + str(total_cure) + ",")
            print("    \"daily_cure\": " + str(total_cure - last_total_cure) + ",")
            print("    \"cure_rate\": " + str(format(total_cure / total_confirm, '.4f')) + ",")
            print("    \"death_rate\": " + str(format(total_death / total_confirm, '.4f')) + ",")
            print("    \"confirm_rate\": " + str(0) + "")
            print('  },')
    print(']')

def calc_country_data():
    dfc = pd.read_csv('./src/assets/csv/time_series_covid19_confirmed_global.csv')
    dfd = pd.read_csv('./src/assets/csv/time_series_covid19_deaths_global.csv')
    dfr = pd.read_csv('./src/assets/csv/time_series_covid19_recovered_global.csv')
    print('[')
    last_country = ""
    countries = []
    countries_col = dfc['Country/Region']
    for i in range(len(dfc)):
        if countries_col[i] != last_country:
            countries.append(countries_col[i])
        last_country = countries_col[i]
    for country in countries:
        print('  {')
        print('    \"country\": ' + "\"" + country.replace("'", "\\'") + "\",")
        print("    \"list\": [")
        total_confirm = -1
        total_death = -1
        total_cure = -1 
        for index, row in dfc.iteritems():
            if index != 'Province/State' and index != 'Country/Region' and index != 'Lat' and index != 'Long':
                last_total_confirm = total_confirm
                last_total_death = total_death
                last_total_cure = total_cure
                total_confirm = 0
                total_death = 0
                total_cure = 0
                for i in range(len(dfc)):
                    if dfc['Country/Region'][i] == country:
                        total_confirm += dfc[index][i]
                for i in range(len(dfd)):
                    if dfd['Country/Region'][i] == country:
                        total_death += dfd[index][i]
                for i in range(len(dfr)):
                    if dfr['Country/Region'][i] == country:
                        total_cure += dfr[index][i]
                if last_total_confirm == -1:
                    last_total_confirm = int(2 * total_confirm / 3)
                if last_total_cure == -1:
                    last_total_cure = int(2 * total_cure / 3)
                if last_total_death == -1:
                    last_total_death = int(2 * total_death / 3)                
                print('      {')
                print("        \"date\": \"" + format_string(index) + "\",")
                print("        \"total_confirm\": " + str(total_confirm) + ",")
                print("        \"daily_confirm\": " + str(total_confirm - last_total_confirm) + ",")
                print("        \"total_death\": " + str(total_death) + ",")
                print("        \"daily_death\": " + str(total_death - last_total_death) + ",")
                print("        \"total_cure\": " + str(total_cure) + ",")
                print("        \"daily_cure\": " + str(total_cure - last_total_cure) + ",")
                print("        \"cure_rate\": " + str(format(total_cure / max(total_confirm, 1), '.4f')) + ",")
                print("        \"death_rate\": " + str(format(total_death / max(total_confirm, 1), '.4f')) + ",")
                print("        \"confirm_rate\": " + str(0) + "")
                if index != last_date:
                    print('      },')
                else:
                    print('      }')
        print("    ]")
        print('  },')
    print(']')

if print_country_name:
    list_country()
    print("")
if print_global_data:
    calc_global_data()
    print("")
if print_country_data:
    calc_country_data()
