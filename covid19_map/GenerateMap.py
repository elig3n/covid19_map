import os
import sys
import shutil
import json
import pandas
import folium
import requests

URL = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/'

def GetLatestCovidCsv():
    try:
        request = requests.get(f'{URL}dpc-covid19-ita-regioni-latest.csv')
        directory = os.getcwd()
        filename = directory + '\\csv\\latest.csv'
        f = open(filename,'wb')
        f.write(request.content)
        return filename
    except Exception as e:
        print(e)

def GetCovidCsv(date):
    if(date == 'latest'):
        return GetLatestCovidCsv()
    try:
        filename = os.getcwd() + f'\\csv\\{date}.csv'
        if(not os.path.isfile(filename)):
            request = requests.get(f'{URL}dpc-covid19-ita-regioni-{date}.csv')
            if(request.text == "404: Not Found"):
                return None
            f = open(filename,'wb')
            f.write(request.content)
        return filename
    except Exception as e:
        print(e)

def GenerateHTML(date):
    csv = GetCovidCsv(date)
    if(csv == None):
        #cd = os.getcwd()
        #map_path = f"{cd}\\map.html"
        #if(os.path.isfile(map_path)):
            #os.remove(map_path)
        #shutil.copy2(f"{cd}\\404.html", map_path)
        return "404"
    else:
        regcovid = pandas.read_csv(csv)
        filename = f'maps/map{date}.html'
    if(os.path.isfile(os.getcwd() + f'\\maps\\map{date}.html')):
        return filename
    else:
        with open('regioni.geojson') as f:
            regioni_geojson = json.load(f)
        for item in regioni_geojson["features"]:
            item["regcovid"] = item["properties"]["NOME_REG"]
        map = folium.Map(location = [43, 12], zoom_start = 6)
        folium.Choropleth(
        geo_data = regioni_geojson,
        data = regcovid,
        columns = ['denominazione_regione', 'totale_positivi'],
        key_on = 'feature.regcovid',
        bins = 6,
        fillColor = 'OrRd',
        nan_fill_color = 'white',
        fill_opacity = 0.6,
        nan_fill_opacity = None,
        line_color = 'black',
        line_weight = 1,
        line_opacity = 1,
        name = None,
        legend_name = 'Positivi da COVID-19 regioni italiane',
        overlay = True,
        control = True,
        show = True,
        topojson = None,
        smoothfactor = None,
        highlight = None
    ).add_to(map)
    map.save(filename)
    return filename
    
def main():
    if(len(sys.argv) > 1):
        print(GenerateHTML(sys.argv[1]))
    else:
        GenerateHTML("latest")

if (__name__  == '__main__'):
    main()