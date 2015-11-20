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



class dataPlot(object):
    """dataPlot takes a pandas dataframe as input and outputs different plots correspondng to the input dataframe"""
    
    def __init__(self, df):
        """Initialize variables"""
        self.df = df
        self.fig = plt.figure()
        
    def histogram(self,colType):
        ax1 = self.fig.add_subplot(2, 1, 1)         # 2x1 grid, first plot
        ax1.hist(self.df[colType], bins=15)
        
    def scatter(self):
        ax2 = self.fig.add_subplot(2, 1, 2)         # 2x1 grid, first plot
        ax2.scatter(self.df["longitude"], self.df["latitude"], s=self.df["mag"]*20)
        
    def animate(self):
        lons = self.df['longitude'].values
        lats = self.df['latitude'].values

        # General plot  initializations
        self.fig = plt.figure(figsize=(14,10))
        ax = self.fig.add_subplot(1,1,1)
        earth = Basemap(projection='mill')
        earth.drawcoastlines(color='0.50', linewidth=0.25)
        earth.fillcontinents(color='0.95')
        x, y = earth(lons,lats)
        earth.plot(x,y,'g.')
        
        #rain

        # Create rain data
        n_drops = len(x)
        print n_drops
        rain_drops = np.zeros(n_drops, dtype=[('position', float, 2),
                                              ('size',     float, 1),
                                              ('growth',   float, 1),
                                              ('mag',      float, 1),
                                              ('color',    float, 4)])

        rain_drops['mag'] = self.df['mag']
        rain_drops['position'] = np.column_stack((x,y)) # n_drop x 2 matrix  #np.random.uniform(0, 1, (n_drops, 2)) *1000000
        rain_drops['color'] = (0,0,1,1)
        rain_drops['growth'] = np.exp(self.df['mag']) * 0.1 #n_drop randoms between 50 & 200 

        # Construct the scatter which we will update during animation
        # as the raindrops develop.
        scat = ax.scatter(rain_drops['position'][:, 0], rain_drops['position'][:, 1],
                          s=rain_drops['size'], lw=0.5, edgecolors=rain_drops['color'],
                          facecolors='none', zorder=100)


        def update(frame_number):
            # Get an index which we can use to re-spawn the oldest raindrop.
            current_index = frame_number % n_drops
            print current_index

            # Make all colors more transparent as time progresses.
            rain_drops['color'][:, 3] -= 1.0/len(rain_drops)
            rain_drops['color'][:, 3] = np.clip(rain_drops['color'][:, 3], 0, 1)

            rain_drops['size'] += rain_drops['growth']

            if(rain_drops['mag'][current_index]>6):
                rain_drops['color'][current_index] =  (1,0,0,1)

            # Update the scatter collection, with the new colors, sizes and positions.
            scat.set_edgecolors(rain_drops['color'])
            scat.set_sizes(rain_drops['size'])
            scat.set_offsets(rain_drops['position'])


        # Construct the animation, using the update function as the animation
        # director.
        animation = FuncAnimation(self.fig, update, interval=10)
        plt.show()


data_10 = download_data(2)
dataPlot(data_10).animate()
