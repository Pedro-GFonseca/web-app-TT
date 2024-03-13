#!/usr/bin/python3
import time
import streamlit as sl
from scipy import stats as st
import pandas as pd

if 'experiment_no' not in sl.session_state:
    sl.session_state['experiment_no'] = 0

if 'df_experiment_results' not in sl.session_state:
    sl.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean'])

sl.header('Jogando uma moeda.')


chart = sl.line_chart([0.0, 1.0])

def toss_coin(n):
    trial_outcomes = st.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1
        
        if r == 1:
            outcome_1_count += 1

        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)

    return mean

number_of_trials = sl.slider('Número de tentativas: ', 1, 1000, 10)
start_button = sl.button('Executar')

if start_button:
    sl.write(f'Executanto o experimento de {number_of_trials} tentativas.')
    sl.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)
    sl.session_state['df_experiment_results'] = pd.concat([
        sl.session_state['df_experiment_results'],
        pd.DataFrame(data=[[sl.session_state['experiment_no'],
                            number_of_trials, mean]],
                     columns=['no', 'iterations', 'mean'])
        ],
                                                          axis=0)
    sl.session_state['df_experiment_results'] = sl.session_state['df_experiment_results'].reset_index(drop=True)

    sl.write(sl.session_state['df_experiment_results'])

