import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

df = pd.read_csv("data.dat")
heights = df["Height"]
n = heights.size

mean = heights.mean()
var = heights.var()
print(f"Unbiased sample mean: {mean}")
print(f"Sample variance     : {var}")

std = heights.std()
print("\n    Confidence intervals for mean:")
for p in (0.9, 0.96, 0.98):
    conf_interval = stats.norm.interval(p, loc=mean, scale=std)
    print(f"{p: <5}: {conf_interval}")

df.hist(bins=16, grid=True, density=True, color="salmon")
plt.xlabel("Рост, см")
plt.ylabel("Вероятность")
plt.savefig("hist.png")
plt.show()
