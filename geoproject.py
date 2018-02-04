"""
GeoProject 2.0 coded by Kuba Siekierzyński (c) 2017

The script builds a dictionary of Polish cities and their inhabitants, by parsing the fixed webpage on wikipedia
http://pl.wikipedia.org/wiki/Miasta_w_Polsce_(statystyki)

Next, each dictionary keyword is processed through Google geolocation API to set the geographic coordinates.
http://maps.googleapis.com/maps/api/geocode/xml?

It pulls them down (longitude and latitude) by parsing the XML and adding the values to the dictionary (by town key).

Finally, a graphic window opens and draws a 3D map of all the cities, based on coordinates approximations. The cities\
are shown as cuboids with their heights dependent on the city's population. The map is totally navigable, rotatable and\
zoomable.

"""
import urllib.request
from bs4 import *
from urllib.parse import urlencode as ENCODE
from xml.etree import ElementTree as XML
import pickle
import pyglet
from random import randint as r

cities = {}  # sets up the dictionary
count = 0
mouse_xy = [0, 0, '']

def populate():
    """
    pulls the data from 'cities.pickle' or tries to obtain it from wikipedia
    """

    global cities
    try:
        print('Trying to obtain data from \'cities.pickle\'...')
        with open('cities.pickle', 'rb') as f:
            cities = pickle.load(f)
        print('Success.', len(cities), 'entries found.')
    except FileNotFoundError:
        print('File \'cities.pickle\' not found.')
        url = 'http://pl.wikipedia.org/wiki/Miasta_w_Polsce_(statystyki)'
        count = 0
        print('Trying to parse data from wikipedia:\n', str(url))
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        table_rows = soup.table.find_all('tr')  # finds all <tr> (table rows) on the website (the only table)
        print('Success.', len(table_rows), 'entries found.')  # sums up all table rows including the table header
        print('Processing...')
        for row in table_rows:  # let's go
            city_data = []  # this will collect the needed data per row
            city_key = row.a['title']  # the city's name is part of the 'title' attribute
            city_dat = row.find_all('td')  # let's search in the row's cells
            for city_num in city_dat:
                if not city_num.get('data-sort-value') is None:  # each <tr> contains 6 cells, take only those with data
                    city_data += city_num  # we end up with a 3-item list each time
            if city_key != 'Powiat':  # oh yes, we don't need the header as it does not contains any data
                cities[city_key] = [int(str(city_data[1]).replace('\xa0', '')), 0, 0]  # converts the pop, adds lat/lon
                count += 1
                # print(city_key, cities[city_key])
            print("Done.", count, "cities successfully imported.")


def localize(city):
    """
    takes a city name, pushes it to Google API and assigns longitude and latitude to cities dictionary item
    """

    global cities
    api_url = 'http://maps.googleapis.com/maps/api/geocode/xml?'
    # the location of Google's geolocation API
    url = api_url + ENCODE({'sensor': 'false', 'address': city + ', Poland'})
    # putting the parts together in UTF-8 format
    f = False
    while not f:
        print('Retrieving the data on:', city)
        data = urllib.request.urlopen(url).read()
        # getting that data
        print('Retrieved', len(data), 'characters. Parsing...')
        tree = XML.fromstring(data)
        # digging into the XML tree
        res = tree.findall('result')
        # let's see the results now
        if len(res) > 0:
            f = True
        else:
            print('Something went wrong, trying again.')
    lat = res[0].find('geometry').find('location').find('lat').text
    # dig into the XML tree to find 'latitude'
    lng = res[0].find('geometry').find('location').find('lng').text
    # and longitude
    lat = float(lat)
    lng = float(lng)
    cities[city][1] = lat
    cities[city][2] = lng


def localize_all():
    """
    Goes through the cities one by one, looks for its coordinates and saves the pulled data to the pickle file
    """

    global cities
    for city_name, city_data in cities.items():
        localize(city_name)
    with open('cities.pickle', 'wb') as f:
        pickle.dump(cities, f, pickle.HIGHEST_PROTOCOL)


populate()
# localize_all() # <== use only if trying to populate for the first time

# w, h = 1000, 800
scale = 80
window = pyglet.window.Window(fullscreen=True, caption='GeoProject 2.0 PL')
title = pyglet.text.Label('GeoProject 2.0 PL',
                          font_name='monospace',
                          font_size=18,
                          x=window.width//2, y=window.height - 30,
                          anchor_x='center', anchor_y='center')

@window.event
def on_draw():
    global cities, scale, mouse_xy
    mouse_pos = pyglet.text.Label(str(mouse_xy[2]),
                                  font_name='monospace',
                                  font_size=8,
                                  x=mouse_xy[0], y=mouse_xy[1] + 10,
                                  anchor_x='center', anchor_y='center')
    window.clear()
    for city in cities:
        popu = int(cities[city][0])
        long = int(cities[city][2] * scale * 0.8 - 550)
        lati = int(cities[city][1] * scale * 1.2 - 4600)
        size = int(popu**0.15)
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v3i', (long - size, lati, 0, long, lati - size, 0,
                                                             long + size, lati, 0, long, lati + size, 0)),
                                                    ('c3B', (255, 255, 255,
                                                             r(0, 255), r(0, 255), r (0,255),
                                                             255, 255, 255,
                                                             0, 0, 0)))

        # pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2i', (long - size, lati, long, lati - size,
        #                                                      long + size, lati, long, lati + size)),
        #                                             ('c3B', (255, 255, 255, 255, 128, 128, 255, 0, 0, 0, 0, 0)))
    title.draw()
    mouse_pos.draw()
    fps.draw()

@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouse_xy, cities
    city = ''
    for key, values in cities.items():
        city_x = int(cities[key][2] * scale * 0.8 - 550)
        city_y = int(cities[key][1] * scale * 1.2 - 4600)
        if (city_x - 3 <= x <= city_x + 3) and (city_y - 3 <= y <= city_y + 3):
            city = key
            break
    mouse_xy = [x, y, city]


fps = pyglet.clock.ClockDisplay()

pyglet.app.run()

"""
for city in cities:
    count += 1
    print(count, '|', city, '|', 'Pop:', cities[city][0], 'Lng:', cities[city][1], 'Lat:', cities[city][2])
"""