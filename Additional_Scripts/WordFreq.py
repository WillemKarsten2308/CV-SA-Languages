import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('XH_Freq.csv')
print(data)

df = pd.DataFrame(data)

toP = data.iloc[:, 1]
print(toP)

plt.plot(data.iloc[:, 1])
plt.title("Decrease in XU Words")
plt.ylabel("Number of Words")
plt.show()

data1 = pd.read_csv('AF_Freq.csv')
plt.plot(data1.iloc[:, 1])
plt.title("Decrease in AF Words")
plt.ylabel("Number of Words")
plt.show()

