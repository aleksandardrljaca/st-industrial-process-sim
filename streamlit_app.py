# STREAMLIT APP FOR DATA VISUALIZATION
# TO RUN TYPE streamlit run telemetry_analytics.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def show_telemetry_analytics():
    # Učitaj podatke
    df = pd.read_csv('data/telemetry.csv')
    #df = pd.read_json('http://localhost:3001/telemetrydata')
    
    # Pretvori kolone 'Date' i 'Start Time' u datetime format
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df['Start Time'] = pd.to_datetime(df['Start Time']).dt.time
    df['End Time'] = pd.to_datetime(df['End Time']).dt.time

    # Postavi naslov i sidebar
    st.title('Telemetry Data Dashboard')

    st.sidebar.title("Filters")
    # Koristi 'datetime.date' za selektovanje opsega datuma
    date_range = st.sidebar.slider(
        "Select Date Range",
        min_value=df['Date'].min(),
        max_value=df['Date'].max(),
        value=(df['Date'].min(), df['Date'].max())
    )

    # Filtriraj podatke prema selektovanom opsegu datuma
    df_filtered = df[(df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])]

    # Prikaži osnovne informacije
    total_records = len(df_filtered)
    average_production_time = df_filtered['Production Time'].mean()
    average_temperature = df_filtered['Temperature'].mean()
    average_humidity = df_filtered['Humidity'].mean()

    st.metric(label="Total Records", value=total_records)
    st.metric(label="Average Production Time", value=f"{average_production_time:.2f} seconds")
    st.metric(label="Average Temperature", value=f"{average_temperature:.1f} °C")
    st.metric(label="Average Humidity", value=f"{average_humidity:.1f} %")

    # Grafikon proizvodnog vremena
    st.subheader('Production Time over Time')
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_filtered, x=df_filtered.index, y='Production Time', marker='o')
    plt.xticks(ticks=df_filtered.index[::int(len(df_filtered)/10)], labels=df_filtered['Start Time'][::int(len(df_filtered)/10)].astype(str), rotation=45)
    plt.xlabel('Time')
    plt.ylabel('Production Time (seconds)')
    st.pyplot(plt.gcf())

    # Grafikon temperature
    st.subheader('Temperature over Time')
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_filtered, x=df_filtered.index, y='Temperature', marker='o', color='orange')
    plt.xticks(ticks=df_filtered.index[::int(len(df_filtered)/10)], labels=df_filtered['Start Time'][::int(len(df_filtered)/10)].astype(str), rotation=45)
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    st.pyplot(plt.gcf())

    # Grafikon vlažnosti
    st.subheader('Humidity over Time')
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_filtered, x=df_filtered.index, y='Humidity', marker='o', color='blue')
    plt.xticks(ticks=df_filtered.index[::int(len(df_filtered)/10)], labels=df_filtered['Start Time'][::int(len(df_filtered)/10)].astype(str), rotation=45)
    plt.xlabel('Time')
    plt.ylabel('Humidity (%)')
    st.pyplot(plt.gcf())

    # Distribucija proizvodnog vremena
    st.subheader('Distribution of Production Time')
    plt.figure(figsize=(10, 6))
    sns.histplot(df_filtered['Production Time'], bins=20, kde=True)
    plt.xlabel('Production Time (seconds)')
    plt.ylabel('Frequency')
    st.pyplot(plt.gcf())

    # Distribucija temperature
    st.subheader('Distribution of Temperature')
    plt.figure(figsize=(10, 6))
    sns.histplot(df_filtered['Temperature'], bins=20, kde=True, color='orange')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Frequency')
    st.pyplot(plt.gcf())

    # Distribucija vlažnosti
    st.subheader('Distribution of Humidity')
    plt.figure(figsize=(10, 6))
    sns.histplot(df_filtered['Humidity'], bins=20, kde=True, color='blue')
    plt.xlabel('Humidity (%)')
    plt.ylabel('Frequency')
    st.pyplot(plt.gcf())


    # Korelaciona heatmap
    st.subheader('Correlation Heatmap')
    plt.figure(figsize=(10, 6))
    corr = df_filtered[['Production Time', 'Temperature', 'Humidity']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Heatmap')
    st.pyplot(plt.gcf())

    # Pairplot
    st.subheader('Pairplot')
    plt.figure(figsize=(10, 6))
    sns.pairplot(df_filtered[['Production Time', 'Temperature', 'Humidity']])
    st.pyplot(plt.gcf())
def show_defects_analytics():
    # Učitaj podatke
    df = pd.read_csv('data/defects.csv')
    #df = pd.read_json('http://localhost:3001/defectsdata')
    df['Date']=pd.to_datetime(df['Date']).dt.date
    # Prikaži naslov
    st.title('Defects Summary Dashboard')

    # Dodaj sidebar za filtriranje
    st.sidebar.title("Filters")
    selected_date = st.sidebar.selectbox('Select Date', df['Date'].unique())
    filtered_df = df[df['Date'] == selected_date]

    # Prikaži osnovne informacije koristeći st.metric
    total_defects = filtered_df['Total Defects'].sum()
    average_defects = filtered_df['Total Defects'].mean()
    max_defects = filtered_df['Total Defects'].max()
    min_defects = filtered_df['Total Defects'].min()

    st.metric(label="Total Defects", value=total_defects)
    st.metric(label="Average Defects per Interval", value=f"{average_defects:.2f}")
    st.metric(label="Max Defects in an Interval", value=max_defects)
    st.metric(label="Min Defects in an Interval", value=min_defects)

    # Grafikon totalnih defekata po vremenskim intervalima
    st.subheader('Total Defects per 15-Minute Interval')
    plt.figure(figsize=(12, 6))
    sns.barplot(data=filtered_df, x='Time Range', y='Total Defects', palette='viridis')
    plt.xticks(rotation=45)
    plt.xlabel('Time Range')
    plt.ylabel('Total Defects')
    plt.title(f'Total Defects for {selected_date}')
    st.pyplot(plt.gcf())

    # Histogram totalnih defekata
    st.subheader('Histogram of Total Defects')
    plt.figure(figsize=(10, 4))
    sns.histplot(filtered_df['Total Defects'], bins=10, kde=True, color='blue')
    plt.xlabel('Total Defects')
    plt.ylabel('Frequency')
    plt.title('Histogram of Total Defects')
    st.pyplot(plt.gcf())

    # Line plot za broj defekata po vremenskim intervalima
    st.subheader('Line Plot of Defects per 15-Minute Interval')
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=filtered_df, x='Time Range', y='Total Defects', marker='o', color='red')
    plt.xticks(rotation=45)
    plt.xlabel('Time Range')
    plt.ylabel('Total Defects')
    plt.title(f'Line Plot of Defects for {selected_date}')
    st.pyplot(plt.gcf())

    st.subheader('Heatmap of Defects per Time Range')
    # Pripremi podatke za heatmap
    heatmap_data = pd.pivot_table(filtered_df, values='Total Defects', index='Time Range', aggfunc='sum')
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', fmt='g')
    plt.xlabel('Time Range')
    plt.ylabel('Total Defects')
    plt.title(f'Heatmap of Defects for {selected_date}')
    st.pyplot(plt.gcf())

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Telemetry data", "Defects data"])
    
    if selection == "Telemetry data":
        show_telemetry_analytics()
    elif selection == "Defects data":
        show_defects_analytics()
    
if __name__ == "__main__":
    main()
