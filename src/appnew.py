# STANDARD IMPORTS
import pandas as pd
import numpy as np
from numpy import array
import scipy
from datetime import datetime
import math
import sklearn.metrics
from sklearn.metrics import mean_squared_error

# MATPLOTLIB
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# PLOTLY
import plotly.express as px
import plotly.graph_objects as go

# ARIMA
from pmdarima.arima import auto_arima

# ETS
from statsmodels.tsa.api import ExponentialSmoothing
from multiprocessing import cpu_count
from joblib import Parallel
from joblib import delayed

# PROPHET
from prophet import Prophet

###################################################################################

# PY FILES ARIMA
from get_sum import get_sum
import auto_arima_single
from auto_arima_single import run_arima_get_rmse
from run_arima_tune_get_pred import run_arima

# PY FILES ETS
from ETS_Function import run_ETS_get_rmse
from ETS_Function import predictions

# PY FILES PROPHET
from auto_single_prophet import run_prophet_get_rmse
from run_prophet_tune_get_pred import run_prophet

###################################################################################

# STREAMLIT
import streamlit as st

###################################################################################

# HEADER

st.title('SIX Time Series Prediction')
#st.header('X')
#st.subheader('X')
#st.text('X')
#st.code('for i in range(8): foo()')
#st.write('testtest')

###################################################################################

# START MONTH

start_month = '08-2020'

###################################################################################

# FILE UPLOADER

# file uploader part 1
uploaded_file = st.file_uploader('Upload dataset to run analysis', type=['csv', 'xlsx'])

# progress_bar color
st.markdown(
    """
    <style>
        .stProgress > div > div > div > div {
            background-image: linear-gradient(to right, #ff4b4b , #4bb543);
        }
    </style>""",
    unsafe_allow_html=True,
)

# progress_bar setup
progress_bar = st.progress(0)

# file uploader part 2
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file) #, error_bad_lines=True, warn_bad_lines=False)
    except:
        try:
            df = pd.read_excel(uploaded_file)
        except:
            df = pd.DataFrame()

    # progress_bar animation
    for perc_completed in range(100):
        progress_bar.progress(perc_completed+1)

    # file uploader success
    st.success('Dataset uploaded successfully.')

###################################################################################

# DATASET INFO

if uploaded_file is not None:
    df2 = df.copy()
    df2 = df2.set_index(df2.columns[0])
    df2_dates = pd.Series(pd.period_range(start_month, freq="M", periods=len(df2.columns)))
    df2.columns = df2_dates
    st.text(str(len(df2.axes[0])) + ' merchants x ' + str(len(df2.axes[1])) + ' months.\n'
            + 'Period from ' + str(df2.columns[0]) + ' to ' + str(df2.columns[-1]) + '.')

###################################################################################

# GET_SUM DISPLAY

if uploaded_file is not None:
    data = get_sum(df, 'sum', start_month)
    # prints differently on streamlit
    st.table(data)
    st.dataframe(data)
    print(data)
    print()

###################################################################################

# GET_RMSE

if uploaded_file is not None:
    models = ['ARIMA', 'ETS', 'PROPHET']
    rmse_models = dict.fromkeys(models)

    # RUN ARIMA get RMSE
    rmse_models['ARIMA'] = (run_arima_get_rmse(merchant=data, merchant_name='total', train_test_split=21, seasonality=12, D_val=1))

    # RUN ETS get RMSE
    cfg, rmse_models['ETS'] = run_ETS_get_rmse(data)

    # RUN PROPHET get RMSE
    rmse_models['PROPHET'] = (run_prophet_get_rmse(merchant=data, train_test_split=21))

    # python console print check
    print('List of RMSE per model')
    print(rmse_models)
    print()

    # best model depending on the smallest error
    best = min(rmse_models, key=rmse_models.get)

    # python console print check
    print('The best model is {}'.format(best))

###################################################################################

# BEST MODEL 12M PREDICTION

#if uploaded_file is not None:
    #if best == 'ARIMA':
        #predictions_df_ar, fitted_df_ar = run_arima(data, 'total', seasonality=12, D_val=1, pred_months=12)
        #predictions_df_ar.to_csv(output + str(data.Month.max()) + '_arima_pred.csv')
        #fitted_df_ar.to_csv(output + str(data.Month.max()) + '_arima_fit.csv')
    #elif best == 'ETS':
        #df_predictions_ets, df_fitted_ets = predictions(data, cfg)
        #df_predictions_ets.to_csv(output + str(data.Month.max()) + '_ETS_pred.csv')
        #df_fitted_ets.to_csv(output + str(data.Month.max()) + '_ETS_fit.csv')
    #elif best == 'PROPHET':
        #df_predictions_pr, df_fitted_pr = run_prophet(data, pred_months=12)
        #df_fitted_pr.to_csv(output + str(data.Month.max()) + '_Prophet_fit.csv')
        #df_predictions_pr.to_csv(output + str(data.Month.max()) + '_Prophet_pred.csv')

###################################################################################

# ALL MODELS 12M PREDICTIONS

if uploaded_file is not None:

    # ARIMA output
    predictions_df_ar, fitted_df_ar = run_arima(data, 'total', seasonality=12, D_val=1, pred_months=12)
    #predictions_df_ar.to_csv(output + str(data.Month.max()) + '_arima_pred.csv')
    #fitted_df_ar.to_csv(output + str(data.Month.max()) + '_arima_fit.csv')

    # ETS output
    df_predictions_ets, df_fitted_ets = predictions(data, cfg)
    #df_predictions_ets.to_csv(output + str(data.Month.max()) + '_ETS_pred.csv')
    #df_fitted_ets.to_csv(output + str(data.Month.max()) + '_ETS_fit.csv')

    # PROPHET output
    df_predictions_pr, df_fitted_pr = run_prophet(data, pred_months=12)
    #df_fitted_pr.to_csv(output + str(data.Month.max()) + '_Prophet_fit.csv')
    #df_predictions_pr.to_csv(output + str(data.Month.max()) + '_Prophet_pred.csv')

###################################################################################

# RUN COMPLETED

    st.balloons()