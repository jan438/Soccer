import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
x = np.linspace(0, 2*np.pi, 100)
y = np.cos(x)
fig, ax = plt.subplots()
ax.plot(x, y, color="green")
fig.savefig("PDF/figure.pdf")
plt.show()
key = input("Wait")
