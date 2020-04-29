import matplotlib.pyplot as plt
import numpy as np
from data_code.analyze_timeline import *

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
def make_religion_plot(state, religion_lis):
    labels = [name[0] for name in religion_lis]
    sizes = [count[1] for count in religion_lis]
    # explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Of All Religious Words Tweeted, the Percent of Words by Religion')

    link = 'app/static/images/' + state + '_religion_plot.png'

    fig.savefig(link)
