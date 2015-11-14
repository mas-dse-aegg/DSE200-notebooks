"""Rain Simulation

Simulates rain drops on a surface by animating the scale and opacity
of 50 scatter points.

Author: Nicolas P. Rougier
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.basemap import Basemap
import pandas as pd

feed="http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/"
feeds={1: feed + "significant_month.csv",
      2: feed+ "4.5_month.csv",
      3: feed+ "2.5_month.csv",
      4: feed + "1.0_month.csv"}

def download_data(i):
    return pd.read_csv(feeds[i])

stations=download_data(2)
lons=stations['longitude'].values
lats=stations['latitude'].values

#General plot  initializations
fig = plt.figure(figsize=(14,10))
ax = plt.subplot(1,1,1)
earth = Basemap(projection='mill')
earth.drawcoastlines(color='0.50', linewidth=0.25)
earth.fillcontinents(color='0.95')


x, y = earth(lons,lats)
earth.plot(x,y,'g.')

# Create new Figure and an Axes which fills it.

# ax = fig.add_axes([0, 0, 1, 1], frameon=False)
# ax.set_xlim(0, 1), ax.set_xticks([])
# ax.set_ylim(0, 1), ax.set_yticks([])

# Create rain data
n_drops = len(x)
rain_drops = np.zeros(n_drops, dtype=[('position', float, 2),
                                      ('size',     float, 1),
                                      ('growth',   float, 1),
                                      ('color',    float, 4)])

# Initialize the raindrops in random positions and with
# random growth rates.
#chose 50 from our dataset 
pairs = np.column_stack((x,y))
# pairs = pairs[:n_drops]


rain_drops['position'] = pairs #np.random.uniform(0, 1, (n_drops, 2)) *1000000
rain_drops['growth'] = np.random.uniform(50, 200, n_drops) 

# Construct the scatter which we will update during animation
# as the raindrops develop.
scat = ax.scatter(rain_drops['position'][:, 0], rain_drops['position'][:, 1],
                  s=rain_drops['size'], lw=0.5, edgecolors=rain_drops['color'],
                  facecolors='none', zorder=100)


def update(frame_number):
    # Get an index which we can use to re-spawn the oldest raindrop.
    current_index = frame_number % n_drops

    # Make all colors more transparent as time progresses.
    rain_drops['color'][:, 3] -= 1.0/len(rain_drops)
    rain_drops['color'][:, 3] = np.clip(rain_drops['color'][:, 3], 0, 1)

    # Make all circles bigger.
    rain_drops['size'] += rain_drops['growth']

    # Pick a new position for oldest rain drop, resetting its size,
    # color and growth factor.
    # rain_drops['position'][current_index] = np.random.uniform(0, 1, 2)
    rain_drops['size'][current_index] = 5
    rain_drops['color'][current_index] = (0, 0, 0, 1)
    rain_drops['growth'][current_index] = np.random.uniform(50, 200)

    # Update the scatter collection, with the new colors, sizes and positions.
    scat.set_edgecolors(rain_drops['color'])
    scat.set_sizes(rain_drops['size'])
    scat.set_offsets(rain_drops['position'])


# Construct the animation, using the update function as the animation
# director.
animation = FuncAnimation(fig, update, interval=10)
plt.show()

