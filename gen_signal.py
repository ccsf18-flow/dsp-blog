from data import signal
from matplotlib import pyplot as plt

# Start by showing the signal itself
fig = plt.gcf()
plt.plot(signal)
plt.savefig('img/signal.png', bbox_inches='tight', dpi=fig.dpi)
