import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pymongo import MongoClient
import seaborn as sns

def load_data():
    # Create a connection to the MongoDB instance
    client = MongoClient('mongodb://localhost:27017/')  # replace with your MongoDB connection string if not local

    # Access the specific database and collection
    db = client["your_database"]
    collection = db["your_collection"]

    # Convert the collection to a DataFrame
    dt = pd.DataFrame(list(collection.find()))
    dt.drop("_id", axis=1, inplace=True)

    # Set 'datetime' as the index
    dt.set_index('datetime', inplace=True)

    # Convert 'datetime' column to datetime format with the correct format
    dt.index = pd.to_datetime(dt.index, format='%Y-%m-%dT%H:%M:%S.%fZ')

    # Extract the hour from the 'datetime' column
    dt['hour'] = dt.index.hour

    # Set the frequency to hourly
    dt = dt.asfreq('h')

    # Sort the data by 'datetime'
    dt = dt.sort_index()

    return dt




def main():
    st.title('Energy Data Analysis')
    st.markdown("## Total Power Overview")
    dt = load_data()

    total_consumption = dt["powerConsumptionTotal"].sum()
    total_production = dt["powerProductionTotal"].sum()
    total_import = dt["powerImportTotal"].sum()
    total_export = dt["powerExportTotal"].sum()

    totals = pd.DataFrame({
        'Category': ['Consumption', 'Production', 'Import', 'Export'],
        'Value': [total_consumption, total_production, total_import, total_export]
    })

    # Plot the differences using a bar plot
    # Total Power Breakdown
    st.markdown("### Total Power Breakdown")
    fig1, ax1 = plt.subplots()
    sns.barplot(x='Category', y='Value', data=totals, palette=['blue', 'green', 'orange', 'red'], ax=ax1)
    ax1.set_title('Difference in Total Power')
    st.pyplot(fig1)

    # Get the descriptive statistics
    st.markdown("## Descriptive Statistics")
    statistics = dt.describe()
    statistics.rename(columns={"powerConsumptionTotal": "ConsumptionTotal","powerProductionTotal": "ProductionTotal",
                               "powerImportTotal": "ImportTotal", "powerExportTotal": "ExportTotal", "powerConsumptionBreakdown.nuclear": "nuclear", "powerConsumptionBreakdown.geothermal": "geothermal",
                               "powerConsumptionBreakdown.wind": "wind", "powerConsumptionBreakdown.gas": "gas",
                               "powerConsumptionBreakdown.oil": "oil", "powerConsumptionBreakdown.solar": "solar"},inplace=True)

    # Create a box plot for descriptive statistics
    fig2, ax2 = plt.subplots(figsize=(15, 10))
    sns.boxplot(data=statistics, palette="Set3", ax=ax2, width=0.6)
    ax2.set_title('Box Plot of Descriptive Statistics', fontsize=20)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right', fontsize=12)
    st.pyplot(fig2)

    # Sidebar for user inputs and navigation
    with st.sidebar:
        st.header('Settings')
        column = st.selectbox('Select Data Column', dt.columns)
        p = st.slider('AR(p) Order', 0, 5, 2)
        d = st.slider('Differencing Order', 0, 2, 1)
        q = st.slider('MA(q) Order', 0, 5, 2)

    # Main content area
    series = dt[column]
    model = ARIMA(series, order=(p, d, q))
    model_fit = model.fit()
    pred = model_fit.forecast(steps=24)
    # Create a time index for the next 24 hours
    forecast_index = pd.date_range(start=dt.index[-1], periods=25, freq='h')[1:]

    # Forecast Plot
    st.markdown("## Forecast with the side panel")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=dt, x=dt.index, y=column, label='Actual', ax=ax3)
    sns.lineplot(x=forecast_index, y=pred, label='Forecast', linestyle='--', ax=ax3)
    ax3.set_title(f'Forecast of {column} for the Next 24 Hours')
    st.pyplot(fig3)


if __name__ == "__main__":
    main()


