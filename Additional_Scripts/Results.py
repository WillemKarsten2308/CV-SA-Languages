import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

totSen = np.array([29036, 55466, 18793, 11311])
useSen = np.array([228, 1366, 983, 644])
totScaled = totSen/10

allTokens = [254275, 482284, 194034, 243235]
allTypes = [15204, 103990, 58393, 19261]
useTokens = np.array([3754, 13035, 10669, 12676])
useTypes = np.array([1470, 7966, 6560, 2997])

useTokensScaled = useTokens*20
useTypesScaled = useTypes*10

languages = ['NSO', 'ZU', 'XH', 'TN']

plt.title("Total and Usable Sentences")
plt.xlabel("Languages")
plt.ylabel("Amount")
plt.plot(languages, totScaled, c='b', marker='x', label='Total')
plt.plot(languages, useSen, c='r', marker='s', label='Usable')
plt.legend(loc='upper left')
plt.show()

plt.title("Types and Tokens")
plt.xlabel("Languages")
plt.ylabel("Amount")
plt.subplot(121)
plt.suptitle('No Manipulation')
plt.plot(languages, allTokens, c='b', marker='x', label='ALLTokens')
plt.plot(languages, allTypes, c='c', marker='x', label='ALLTypes')
plt.plot(languages, useTokens, c='g', marker='s', label='UsableTokens')
plt.plot(languages, useTypes, c='y', marker='s', label='UsableTypes')
plt.legend(loc='upper right')

plt.subplot(122)
plt.suptitle('With Manipulation')
plt.plot(languages, allTokens, c='b', marker='x', label='ALLTokens')
plt.plot(languages, allTypes, c='c', marker='x', label='ALLTypes')
plt.plot(languages, useTokensScaled, c='g', marker='s', label='UsableTokens')
plt.plot(languages, useTypesScaled, c='y', marker='s', label='UsableTypes')
plt.legend(loc='upper right')
plt.show()

