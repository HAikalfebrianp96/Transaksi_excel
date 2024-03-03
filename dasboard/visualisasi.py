import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')

# Menyiapkan data day_df
day_df = pd.read_csv(r"dasboard/mixel.csv")
day_df.head()

# Menghapus kolom yang tidak diperlukan
drop_col = ['windspeed']

for i in day_df.columns:
  if i in drop_col:
    day_df.drop(labels=i, axis=1, inplace=True)

# Mengubah nama judul kolom
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

# Mengubah angka menjadi keterangan
day_df['month'] = day_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
day_df['weekday'] = day_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
day_df['weather_cond'] = day_df['weather_cond'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})


# Menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

# Menyiapkan daily_casual_rent_df
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan daily_registered_rent_df

def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df
    
# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# Menyiapkan workingday_rent_df
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

# Menyiapkan holiday_rent_df
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

# Menyiapkan weather_rent_df
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather_cond').agg({
        'count': 'sum'
    })
    return weather_rent_df


# Membuat komponen filter
min_date = pd.to_datetime(day_df['dateday']).dt.date.min()
max_date = pd.to_datetime(day_df['dateday']).dt.date.max()

image_url = 'https://upload.wikimedia.org/wikipedia/commons/9/97/Sepeda_Onthel.jpg'
with st.sidebar:
    st.image(image_url, caption='bike', use_column_width=True)
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df['dateday'] >= str(start_date)) & 
                (day_df['dateday'] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)


# Membuat Dashboard secara lengkap

# Membuat judul
st.header('Bike Rental Dashboard 🚲')

# Membuat jumlah penyewaan harian
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual User', value= daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered User', value= daily_rent_registered)
 
with col3:
    daily_rent_total = daily_rent_df['count'].sum()
    st.metric('Total User', value= daily_rent_total)

# Membuat jumlah penyewaan bulanan
st.subheader('Monthly Rentals')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_rent_df.index,
    monthly_rent_df['count'],
    marker='o', 
    linewidth=2,
    color='tab:blue'
)

for index, row in enumerate(monthly_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

analysis_text = '''
<h3>Analisis:</h3>
<p>Musim panas (Juni-Agustus) adalah periode dengan permintaan sewa sepeda tertinggi. Hal ini kemungkinan disebabkan oleh cuaca yang hangat dan cerah, yang mendorong orang untuk lebih banyak beraktivitas di luar ruangan.</p>
<p>Musim dingin (Desember-Februari) adalah periode dengan permintaan sewa sepeda terendah. Hal ini kemungkinan disebabkan oleh cuaca yang dingin dan bersalju, yang membuat orang enggan untuk bersepeda.</p>
<p>Ada sedikit peningkatan permintaan sewa sepeda di musim semi (Maret-Mei) dan musim gugur (September-November). Hal ini kemungkinan disebabkan oleh cuaca yang lebih moderat, yang membuat orang lebih nyaman untuk bersepeda.</p>

<h3>Kesimpulan:</h3>
<p>Tren musiman yang jelas dalam penyewaan sepeda menunjukkan bahwa permintaan untuk layanan ini sangat dipengaruhi oleh cuaca. Perusahaan penyewaan sepeda dapat menggunakan data ini untuk merencanakan strategi bisnis mereka dan memastikan bahwa mereka memiliki persediaan sepeda yang memadai untuk memenuhi permintaan.</p>
'''

st.markdown(analysis_text, unsafe_allow_html=True)


# Membuat jumlah penyewaan berdasarkan season
st.subheader('Seasonly Rentals')

fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x='season',
    y='registered',
    data=season_rent_df,
    label='Registered',
    color='tab:blue',
    ax=ax
)

sns.barplot(
    x='season',
    y='casual',
    data=season_rent_df,
    label='Casual',
    color='tab:orange',
    ax=ax
)

for index, row in season_rent_df.iterrows():
    ax.text(index, row['registered'], str(row['registered']), ha='center', va='bottom', fontsize=12)
    ax.text(index, row['casual'], str(row['casual']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)

analysis_text = '''
<h2 style="color:#0077b6;">Analisis</h2>

<h3 style="color:#ef476f;">Kesimpulan:</h3>
<ul>
  <li>Musim panas memiliki jumlah persewaan sepeda tertinggi (1.670.076).</li>
  <li>Musim semi memiliki jumlah persewaan sepeda kedua tertinggi (1.430.134).</li>
  <li>Musim gugur memiliki jumlah persewaan sepeda ketiga tertinggi (821.452).</li>
  <li>Musim dingin memiliki jumlah persewaan sepeda terendah (452.182).</li>
</ul>

<h3 style="color:#ef476f;">Analisis:</h3>
<ul>
  <li>Perbedaan signifikan terlihat antara jumlah persewaan pada musim panas dan musim dingin. Hal ini menunjukkan bahwa musim memiliki pengaruh besar pada tingkat penggunaan sepeda bersama.</li>
  <li>Jumlah persewaan pada musim semi dan musim gugur lebih tinggi daripada musim dingin. Hal ini menunjukkan bahwa orang lebih memilih untuk menggunakan sepeda bersama dalam cuaca hangat daripada cuaca dingin.</li>
</ul>
'''

st.markdown(analysis_text, unsafe_allow_html=True)



fig, ax = plt.subplots(figsize=(16, 8))

colors=["tab:blue", "tab:orange", "tab:green"]

sns.barplot(
    x=weather_rent_df.index,
    y=weather_rent_df['count'],
    palette=colors,
    ax=ax
)

for index, row in enumerate(weather_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

analysis_text = '''
<h2 style="color:#0077b6;">Analisis</h2>

<h3 style="color:#ef476f;">Kesimpulan:</h3>
<ul>
  <li>Cuaca cerah/berawan sebagian memiliki jumlah persewaan sepeda tertinggi (4.596.125).</li>
  <li>Hujan/salju ringan memiliki jumlah persewaan sepeda kedua tertinggi (1.792.810).</li>
  <li>Kabut/berawan memiliki jumlah persewaan sepeda ketiga tertinggi (196.200).</li>
  <li>Cuaca buruk memiliki jumlah persewaan sepeda terendah (223).</li>
</ul>

<h3 style="color:#ef476f;">Analisis:</h3>
<ul>
  <li>Perbedaan signifikan terlihat antara jumlah persewaan pada cuaca cerah/berawan sebagian dan cuaca buruk. Hal ini menunjukkan bahwa cuaca memiliki pengaruh besar pada tingkat penggunaan sepeda bersama.</li>
  <li>Jumlah persewaan pada hujan/salju ringan lebih tinggi daripada kabut/berawan. Hal ini menunjukkan bahwa orang lebih memilih untuk menggunakan sepeda bersama dalam cuaca dingin daripada cuaca basah.</li>
</ul>
'''

st.markdown(analysis_text, unsafe_allow_html=True)




##Membuat jumlah penyewaan berdasarkan weekday, working dan holiday
st.subheader('Weekday, Workingday, and Holiday Rentals')

fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15,10))

colors1=["tab:blue", "tab:orange"]
colors2=["tab:blue", "tab:orange"]
colors3=["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink"]

## Berdasarkan workingday
sns.barplot(
    x='workingday',
    y='count',
    data=workingday_rent_df,
    palette=colors1,
    ax=axes[0])

for index, row in enumerate(workingday_rent_df['count']):
    axes[0].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[0].set_title('Number of Rents based on Working Day')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

# Berdasarkan holiday
sns.barplot(
  x='holiday',
  y='count',
  data=holiday_rent_df,
  palette=colors2,
  ax=axes[1])

for index, row in enumerate(holiday_rent_df['count']):
    axes[1].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[1].set_title('Number of Rents based on Holiday')
axes[1].set_ylabel(None)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=10)

# Berdasarkan weekday
sns.barplot(
  x='weekday',
  y='count',
  data=weekday_rent_df,
  palette=colors3,
  ax=axes[2])

for index, row in enumerate(weekday_rent_df['count']):
    axes[2].text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

axes[2].set_title('Number of Rents based on Weekday')
axes[2].set_ylabel(None)
axes[2].tick_params(axis='x', labelsize=15)
axes[2].tick_params(axis='y', labelsize=10)


sns.pointplot(
    x=day_df['hr'],
    y=day_df['registered'],
    hue=day_df['season'],
    ax=axes[1]
)

axes[1].set_title('Bike Rental Trend according to Instant on Season')
axes[1].set_xlabel("Hour of the Day")
axes[1].set_ylabel("Registered Bike Rentals")

# Plot ketiga (kosongkan saja)
axes[2].axis('off')

plt.tight_layout()
st.pyplot(fig)
analysis_text = '''
<h2 style="color:#0077b6;">Analisis:</h2>

<h3 style="color:#ef476f;">Tren Musiman:</h3>
<p>Dalam industri penyewaan sepeda di Indonesia, ada tren musiman yang jelas. Permintaan tertinggi terjadi selama musim kemarau (Mei-Oktober), sementara permintaan terendah terjadi selama musim hujan (November-April).</p>

<h3 style="color:#ef476f;">Faktor Penentu:</h3>
<p>Cuaca adalah faktor kunci yang memengaruhi tren musiman ini. Di musim kemarau, cuaca cerah dan minim hujan membuat orang lebih nyaman untuk bersepeda. Sebaliknya, di musim hujan, cuaca basah dan angin membuat orang enggan untuk bersepeda.</p>

<h3 style="color:#ef476f;">Hari-Hari Dengan Permintaan Tinggi:</h3>
<p>Selain tren musiman, ada juga hari-hari tertentu yang menunjukkan permintaan sewa sepeda yang lebih tinggi, seperti akhir pekan dan hari libur nasional. Ini menunjukkan bahwa banyak orang memilih untuk menggunakan sepeda untuk beraktivitas di luar ruangan pada hari-hari tersebut.</p>

<h2 style="color:#0077b6;">Kesimpulan:</h2>
<p>Tren musiman dan hari-hari dengan permintaan tinggi dalam industri penyewaan sepeda menunjukkan adanya peluang besar bagi perusahaan penyewaan sepeda untuk meningkatkan pendapatan mereka. Perusahaan dapat menggunakan data ini untuk merencanakan strategi bisnis mereka dan memastikan bahwa mereka memiliki persediaan sepeda yang memadai untuk memenuhi permintaan.</p>
'''

st.markdown(analysis_text, unsafe_allow_html=True)

st.caption('Copyright (c) M haikal 2023')
