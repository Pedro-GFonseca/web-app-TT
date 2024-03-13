#!/usr/bin/python3
import pandas as pd
import plotly.express as px
import streamlit as st


with st.sidebar: #Criando uma sidebar para selecionar o modo de visualização
    st.title('Dados de venda de carros')
    st.header('Selecione um modo de visualização')

    variable_selected = st.selectbox('Modo de visualização', ['Dados Brutos', 'Gráficos'])

    if (variable_selected == 'Dados Brutos'):
        st.write('Você também pode selecionar um agrupamento para os dados brutos para visualizar as médias de cada variável')


car_data = pd.read_csv('vehicles.csv') # Lendo os dados

if (variable_selected == 'Dados Brutos'): # Se a variável selecionada for Dados Brutos, vai mostrar opções de agrupamento
    select_options = ['Nenhum', 'model', 'condition', 'type', 'paint_color']

    grouping = st.selectbox('Tipo de agrupamento', select_options)
    
    if (grouping == 'Nenhum'):
        st.dataframe(car_data, use_container_width=True)
    
    else:
        grouped_dataframe = car_data.groupby(grouping).mean()
        st.dataframe(grouped_dataframe, use_container_width=True)

if (variable_selected == 'Gráficos'): # Se o modo selecionado for o de gráficos, vai mostrar as opções

    hist_button = st.checkbox('Criar histograma') # Criando os botões
    disp_button = st.checkbox('Criar gráfico de dispersão') 
    bar_button = st.checkbox('Criar gráfico de barras')

    if hist_button: # Se o botão for clicado
        st.write('Criando histogramas para o conjunto de dados de anúncio de venda de carros')
        fig_year = px.histogram(car_data, x='model_year', labels={'model_year' : 'Ano de Fabricação'}, title='Quantidade de Carros por Ano de Fabricação')

        fig = px.histogram(car_data, x='odometer', labels={'odometer' : 'Odômetro'}, title='Frequência por Odômetro')

        
        # Exibir um gráfico Plotly interativo
        st.plotly_chart(fig, use_container_width=True)
        st.plotly_chart(fig_year, use_container_width=True)

    if disp_button:
        st.write('Criando gráfico de dispersão para o conjunto de dados de anúncio de venda de carros')
        
        model_year = car_data.groupby('model_year')['price'].mean().reset_index()
        fig_scatter = px.scatter(model_year, x='model_year', y='price', labels={'price' : 'Preço', 'model_year' : 'Ano de Fabricação'}, title='Preço por Ano de Fabricação')


        st.plotly_chart(fig_scatter, use_container_width=True)

    if bar_button:
        st.write('Criando gráficos de barras para o conjunto de dados de anúncio de venda de carros')

        condition_data = car_data.groupby('condition')['model_year'].count().reset_index()
        fig_condition = px.bar(condition_data, x='condition', y='model_year', title='Condição dos carros', labels={'model_year' : 'Quantidade de carros', 'condition' : 'Condição'})

        groupby_fuel = car_data.groupby('fuel')['price'].mean().reset_index()
        fig_fuel = px.bar(groupby_fuel, x='fuel', y='price', labels={'price' : 'Preço', 'fuel' : 'Tipo de Combustível'}, title='Preço por Tipo de Combustível')

        type_data = car_data.groupby('type')['model'].count().reset_index()
        fig_type = px.bar(type_data, x='type', y='model', labels={'type' : 'Tipo de Veículo', 'model' : 'Quantidade'}, title='Quantidade de Veículos por Tipo')

        st.plotly_chart(fig_condition, use_container_width=True)
        st.plotly_chart(fig_fuel, use_container_width=True)
        st.plotly_chart(fig_type, use_container_width=True)

