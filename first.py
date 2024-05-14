import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.express as px


URL = 'https://api.hh.ru/vacancies'
jobs = ['Геодезист', 'Хореограф', 'Кинорежиссер', 'Учитель', 'Хирург']

data = {}
for job in jobs:
    parametrs = {
        'text': job,
        'area': 1,
        'page': 0,
        'per_page': 100
    }
    now = requests.get(URL, parametrs).json()
    pages = now['pages']
    data[job] = []
    for page in range(pages):
        parametrs['page'] = page
        now = requests.get(URL, parametrs).json()
        data[job].append(now)

counter = 0
for info in data.keys():
    counter += data[info][0]['found']
    print(info, data[info][0]['found'])
print(counter)


EPS = 1e-9

class Company:
    def __init__(self, name: str, lat: [None, float], lng: [None, float]):
        self.name = name
        self.lat = lat if lat is not None else 2000.0
        self.lng = lng if lng is not None else 2000.0

    def __eq__(self, other):
        return self.name == other.name and (self.lat - other.lat) < EPS and (self.lng - other.lng) < EPS

    def get_diff(self, first: tuple[float, float], second: tuple[float, float]) -> float:
        return ((first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2) ** 0.5

    def check_in_MKAD(self):
        center = (55.755864, 37.617698)
        side = (55.758852, 37.842823)
        return self.get_diff(center, side) >= self.get_diff(center, (self.lat, self.lng))


companies = {}
for key in data.keys():
    companies[key] = []
    for page_info in data[key]:
        for vac in page_info['items']:
            lat, lng = None, None
            if vac['address'] is not None:
                lat, lng = vac['address']['lat'], vac['address']['lng']
            now = Company(vac['employer']['name'], lat, lng)
            if now not in companies[key]:
                companies[key].append(now)
cnt = 0
for i in companies.values():
    cnt += len(i)
print(cnt)

counter_with_coords = 0
for key in data.keys():
    companies[key] = []
    for page_info in data[key]:
        for vac in page_info['items']:
            if vac['address'] is not None:
                counter_with_coords += 1
print(counter_with_coords)

in_center = {}
for key in data.keys():
    in_center[key] = []
    for page_info in data[key]:
        for vac in page_info['items']:
            if vac['address'] is not None:
                lat, lng = vac['address']['lat'], vac['address']['lng']
                now = Company(vac['employer']['name'], lat, lng)
                if now.check_in_MKAD():
                    in_center[key].append(now)
cnt = 0
for i in in_center.values():
    cnt += len(i)
print(cnt)


colors = ['orange', 'green', 'blue', 'black', 'red']
for id, info in enumerate(sorted(in_center.values(), key=lambda x: len(x), reverse=True)):
    lats = []
    lngs = []
    for item in info:
        lats.append(item.lat)
        lngs.append(item.lng)
    plt.scatter(lats, lngs, c=colors[id], s=25, alpha=0.20)
plt.show()


need = []
for key in in_center.keys():
    for item in in_center[key]:
        need.append([item.lat, item.lng, key, 1])
csv_data = pd.DataFrame(need, columns=['lat', 'lng', 'color', 'size'])
fig = px.scatter_mapbox(csv_data, lat="lat", lon="lng", zoom=10, size='size', size_max=6, color='color')
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
