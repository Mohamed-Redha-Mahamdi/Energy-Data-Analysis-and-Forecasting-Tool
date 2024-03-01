import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from pymongo import MongoClient
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error
import plotly.express as px

def load_data():
    # Create a connection to the MongoDB instance
    client = MongoClient('mongodb://localhost:27017/')  # replace with your MongoDB connection string if not local

    # Access the specific database and collection
    db = client["mydatabase"]
    collection = db["energy"]

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
    dt.rename(columns={"powerConsumptionTotal": "ConsumptionTotal","powerProductionTotal": "ProductionTotal",
                               "powerImportTotal": "ImportTotal", "powerExportTotal": "ExportTotal", "powerConsumptionBreakdown.nuclear": "nuclear", "powerConsumptionBreakdown.geothermal":   "geothermal",
                               "powerConsumptionBreakdown.wind": "wind", "powerConsumptionBreakdown.gas": "gas",
                               "powerConsumptionBreakdown.oil": "oil", "powerConsumptionBreakdown.solar": "solar"},inplace=True)
    return dt


def main():
    st.title('Energy Data Analysis')
    st.markdown("## Total Power Overview")
    dt = load_data()

    # Interactive Plotly Plot for Total Power Breakdown
    totals = pd.DataFrame({
        'Category': ['Consumption', 'Production', 'Import', 'Export'],
        'Value': [dt["ConsumptionTotal"].sum(), dt["ProductionTotal"].sum(),
                  dt["ImportTotal"].sum(), dt["ExportTotal"].sum()]
    })
    fig_totals = px.bar(totals, x='Category', y='Value', color='Category')
    st.plotly_chart(fig_totals, use_container_width=True)

    # Get the descriptive statistics
    st.markdown("## Descriptive Statistics")
    statistics = dt.describe()

    # Create a box plot for descriptive statistics
    fig2, ax2 = plt.subplots(figsize=(15, 10))
    sns.boxplot(data=statistics, palette="Set3", ax=ax2, width=0.6)
    ax2.set_title('Box Plot of Descriptive Statistics', fontsize=20)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right', fontsize=12)
    st.pyplot(fig2)

    # Correlation Heatmap
    st.markdown("## Correlation Heatmap")
    corr = dt.corr()
    fig_heatmap = px.imshow(corr, text_auto=True)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Time Series Decomposition Plot
    st.markdown("## Time Series Decomposition")
    series = dt['ConsumptionTotal']  # Replace with the appropriate column
    result = seasonal_decompose(series, model='additive', period=24)  # Assuming hourly data with daily seasonality
    fig_decompose = px.line(result.trend)  # Plotly figure for trend
    st.plotly_chart(fig_decompose, use_container_width=True)


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

    # Forecast Plot with Plotly
    forecast_index = pd.date_range(start=dt.index[-1], periods=25, freq='h')[1:]
    fig_forecast = px.line(dt, x=dt.index, y=column, labels={'value': 'Power Consumption'})
    fig_forecast.add_scatter(x=forecast_index, y=pred, mode='lines', name='Forecast')
    st.plotly_chart(fig_forecast, use_container_width=True)

    # Forecasting Metrics Display
    actual_values = dt['ConsumptionTotal'][-24:]  # Replace with actual values
    predicted_values = pred  # Replace with your predictions
    mae = mean_absolute_error(actual_values, predicted_values)
    rmse = mean_squared_error(actual_values, predicted_values, squared=False)
    st.metric(label="Mean Absolute Error", value=mae)
    st.metric(label="Root Mean Square Error", value=rmse)


if __name__ == "__main__":
    main()
