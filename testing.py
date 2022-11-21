import pandas as pd
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ppscore as pps 


df = pd.read_csv('/Users/johnsonhsiao/Desktop/a018101010-4170.csv',encoding='utf-8')
print(df)

mat = (pps.matrix(df[:27]))
print(mat)

plt.figure(figsize=(15, 13)) 
sns.heatmap(mat, annot=True, vmin=0, vmax=1, cmap='Blues') 
plt.title("Predictive Power Score")
