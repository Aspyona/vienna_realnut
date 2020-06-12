import pandas as pd

df = pd.read_csv('/home/pf/autobefreit/REALNUT2018OGD.csv')

list(df)

df.loc[df.NUTZUNG_LEVEL2 == 'weitere verkehrliche Nutzungen', 'NUTZUNG_LEVEL2'] = df.loc[df.NUTZUNG_LEVEL2 == 'weitere verkehrliche Nutzungen', 'NUTZUNG_LEVEL3']
df.loc[df.NUTZUNG_LEVEL2 == 'Straßenraum', 'NUTZUNG_LEVEL2'] = 'Straßenraum & Parkplätze'
df.loc[df.NUTZUNG_LEVEL2 == 'Parkplätze u. Parkhäuser', 'NUTZUNG_LEVEL2'] = 'Straßenraum & Parkplätze'


df.NUTZUNG_LEVEL1.value_counts()
df.NUTZUNG_LEVEL2.value_counts()
df.NUTZUNG_LEVEL3.value_counts()

df[df.NUTZUNG_LEVEL2 == 'Straßenraum'].FLAECHE.sum()
df.BEZ.value_counts()
df[df.NUTZUNG_LEVEL2 == 'weitere verkehrliche Nutzungen'].NUTZUNG_LEVEL3.value_counts()

district_array = []
for i in range(21):
    streets = df[(df.NUTZUNG_LEVEL2 == 'Straßenraum & Parkplätze') & (df.BEZ == i + 1)].FLAECHE.sum()
    district = df[df.BEZ == i + 1].FLAECHE.sum()
    frac = (streets) / district
    district_array.append(frac)
    print(i + 1, frac)

#%%

labels = df.NUTZUNG_LEVEL2.unique()
sizes = []
labels_used = []
district = 1
is_district = df.BEZ == district
# is_district = df.BEZ > 0
district_area = df[is_district].FLAECHE.sum()

others_idx = False
for i, label in enumerate(labels):
    usage = df[(df.NUTZUNG_LEVEL2 == label) & is_district].FLAECHE.sum()
    if usage / district_area < 0.01:
        if others_idx is False:
            print(label, 'first')
            labels_used.append('Sonstiges')
            sizes.append(df[(df.NUTZUNG_LEVEL2 == label) & is_district].FLAECHE.sum())
            others_idx = i
        else:
            print(label)
            sizes[others_idx] += df[(df.NUTZUNG_LEVEL2 == label) & is_district].FLAECHE.sum()
    else:
        labels_used.append(label)
        sizes.append(df[(df.NUTZUNG_LEVEL2 == label) & is_district].FLAECHE.sum())

#%%
import plotly.graph_objects as go
import plotly.io as pio
explode = list(0 for label in labels_used)
street_idx = labels_used.index('Straßenraum & Parkplätze')
explode[street_idx] = 0.1

# pull is given as a fraction of the pie radius
fig = go.Figure(data=[go.Pie(labels=labels_used, values=sizes, pull=explode)])

fig.update_layout(legend=dict(x=0, y=-1, traceorder="normal", xanchor='left', yanchor='bottom'))
fig.update_layout(autosize=False, width=600, height=600,)
pio.write_html(fig, file='index.html', auto_open=True)
fig.show()

#%%

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.size'] = 16.0

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
explode = list(0 for label in labels_used)
street_idx = labels_used.index('Straßenraum & Parkplätze')
explode[street_idx] = 0.1

fig1, ax1 = plt.subplots(figsize=(10, 10))
ax1.pie(sizes, explode=explode, labels=labels_used, autopct='%1.1f%%',
        shadow=False, startangle=90, )
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.tight_layout()
plt.savefig('/home/pf/autobefreit/pie_vienna_1.png', bbox_inches='tight', dpi=500)
plt.show()


#%%
import numpy as np
fig1, ax1 = plt.subplots(figsize=(10, 5))
plt.bar(np.arange(1, 22), district_array)
plt.xticks(np.arange(1, 22, 1.0))
plt.grid()
plt.gca().set_axisbelow(True)
plt.tight_layout()
plt.xlabel('Bezirk')
plt.ylabel('Anteil Straßen & Parkplätze')
plt.savefig('/home/pf/autobefreit/districts.png', bbox_inches='tight', dpi=500)
plt.show()
