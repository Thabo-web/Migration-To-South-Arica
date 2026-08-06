import pandas as pd
from pathlib import Path
from typing import Optional 
import matplotlib.pyplot as plt
import seaborn as sns
from src.data_loader import load_data
#PYTHONPATH=. python3 src/data_processing.py

df = load_data()

sns.regplot(x='country_name', y='2010', data=df)

plt.show()
