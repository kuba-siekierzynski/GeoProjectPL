# GeoProjectPL
Data mining and visualizations concerning data on Polish cities

## Description
GeoProjectPL is my fully self-made project combining several fields of my knowledge: some Python, web scraping and parsing, data mining, machine learning algorithms, data visualization and interactive programming.

In its initial shape the code was supposed to get the names of Polish cities (actually all locations with city rights/town privileges) from a wikipedia page: https://pl.wikipedia.org/wiki/Miasta_w_Polsce_(statystyki)
Later on, I added that it also parsed for some basic information -- population.
(by the way, I wrote the code back in 2017, when there were 923 towns in Poland and was a little surprised having re-run it a year later - this time 930 locations were found already :)

After the data is collected from wikipedia (which takes several seconds), the code tries to achieve the cities' exact (or approximate) locations, using the Google API. Each city name parsed from wikipedia is plugged in to the geocoding API and both longitude and latitude are retrieved for each city. That, in turn, takes 3-5 minutes, depending on the net connection.

![Output](https://user-images.githubusercontent.com/23619663/35780612-64174b26-09de-11e8-9276-74230ffdc75a.png)

Finally, when all geolocation data is collected, the code run the visualization part. Using OpenGL-supporting pyglet module, it creates a 2D surface and draws flickering diamonds in respective city locations. The size of each diamond is city population-dependent. The user can also hover the mouse cursor over each city and its name will be displayed.

<img src="https://user-images.githubusercontent.com/23619663/35780613-6433b892-09de-11e8-8950-58ec9396b53d.png" width=350 alt="Flickering cities"/> <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/POLSKA_Miasta.png/800px-POLSKA_Miasta.png" width=350 alt="Polish cities" />


## Future dev (and notes to self)
Future developments will include, according to my free time resources available:
-- conversion to 3D
   - each city will be represented by a cube, instead of a diamond
   - some 3D-related visualization options (rotation, zoom, etc.) will be available - much like in my other project - [LAB 3D](https://github.com/kuba-siekierzynski/labyrinth3d)
   - navigating will include mouse and keyboard controls
   - color-coding - for now the flickering is just for fun, colors will have meanings depending on the visualization choice
   
-- Polish plane
   - using the Google API I want to find not only longitude and latitute of cities, but also absolute and relative height over the sea level
   - that will be applicable not only to the cities - I want to create a datapoint mesh and retrieve the mean heights for 1x1km squares covering Poland's territory, to build a 2D surface in a 3D space
   - cities will be put on top of it, to not only visualise the plane, but also a relative heigth - a fully 3D experience!

-- Machine learning implemented
   - Top local news (most frequent topics related to a particular city) - web scraping plus ML algorithms (TF/IDF), to select top five word groups
   - making predictions - population in 2020, 2030, 2040 and beyond, based on past data
   - anything else I find interesting :)


## Requirements
- urllib - for making web connections
- beautifulsoup - for scraping/parsing the wikipedia page
- xml - for parsing XML response from Google API
- pickle - for file dumping/retrieving
- pyglet - for 2D/3D data visualization in OpenGL
