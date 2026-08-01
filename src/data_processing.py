%matplotlib inline
import pandas as pd
from pathlib import Path
from typing import Optional 
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_loader import load_data

df = load_data()

sns.regplot(x='independent_variable', y='dependent_variable', data=df)
plt.show()
