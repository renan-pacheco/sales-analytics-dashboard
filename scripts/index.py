import pandas as pd
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO

from app import *
from visualizations_functions import *
from helper_functions import *

# Configure the logger:
logger = setup_logger('../logging/index.log')

# Import the datasets:
df_raw = pd.read_csv("../datasets/sales_raw.csv")
df_final = pd.read_csv("../datasets/sales_analysis.csv")


# ========================= CREATE LISTS USED BY FILTERS =========================

# Create list of options to be chosen for the month's filter (list of dicts)...
# First, initialize the list:
month_options = [{'label': 'Ano inteiro', 'value': 0}]
# Iterate through the options of month using the above list's structure:
for i, j in zip(df_raw['Mês'].unique(), df_final['Mês'].unique()):
    month_options.append({'label': i, 'value': int(j)})
# Sort the assigned month numbers in ascending order (from 1 to 12):
month_options = sorted(month_options, key=lambda x: x['value'])

# Create list of options to be chosen for the teams:
# First, initialize the list:
team_options = [{'label': 'All teams', 'value': 0}]
# Iterate through the list of options to get the individual teams:
for i in df_final['Equipe'].unique():
    team_options.append({'label': i, 'value': i})


# ========================= INSTANTIATE STYLES FOR THE DASH =========================

# Define the length for all objects to be 100% of their size:
tab_card = {'height': '100%'}

# Define global configuration of all charts:
main_config = {
    "hovermode": "x unified",
    "legend": {"yanchor":"top",
                "y":0.9,
                "xanchor":"left",
                "x":0.1,
                "title": {"text": None},
                "font" :{"color":"white"},
                "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l":10, "r":10, "t":10, "b":10}
}

# Config graph to drop button tips on top of each chart:
config_graph = {"displayModeBar": False, "showTips": False}

# Instantiate the design templates:
template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY


# ========================= CONSTRUCT THE APP'S LAYOUT =========================

# Define the app's layout:
app.layout = dbc.Container(
    children = [
        # Construct 1st row of the dashboard's layout:
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        # Add the first row to the card:
                        dbc.Row([
                            dbc.Col([
                                html.Legend("Sales Analytics")
                            ], sm=8),
                            dbc.Col([
                                html.I(className='fa fa-balance-scale', style={'font-size': '300%'})
                            ], sm=4, align="center")
                        ]),
                        dbc.Row([
                            dbc.Col([
                                ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
                                html.Legend("Provided by ADATA")
                            ])
                        ], style={'margin-top': '10px'}),
                        # Add another row to the card:
                        dbc.Row([
                            dbc.Button("Linkedin", href="https://www.linkedin.com/in/renan-pacheco-301324aa/",
                                       target="_blank")  #Opens a new tab
                        ], style={'margin-top': '10px'})
                    ])
                ], style=tab_card)
            ], sm=4, lg=2),
            # Add the first space where a bar chart will be located...
            # Create a new column where the chart will be added:
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row(
                            dbc.Col(
                                dbc.Col(html.Legend("Top Consultores por Equipe"))
                            )
                        ),
                        dbc.Row([
                            dbc.Col([
                                # Add the first graph, name(id) to be called later by callbacks and
                                # add classname in order to be editable by themeswicher:
                                dcc.Graph(id='graph1', className='dbc', config=config_graph)
                            ], sm=12, md=7),
                            dbc.Col([
                                dcc.Graph(id='graph2', className='dbc', config=config_graph)
                            ], sm=12, md=5)
                        ])
                    ])
                ], style=tab_card)
            ], sm=12, lg=7),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row(
                            dbc.Col([
                                html.H5("Escolha o mês"),
                                dbc.RadioItems(
                                    id = 'radio-month',
                                    options = month_options,
                                    value = 0,  #By default, all months are selected
                                    inline = True,
                                    labelCheckedClassName = "text-success", #If checked, color it green
                                    inputCheckedClassName = "border border-success bg-success"
                                ),
                                html.Div(
                                    id='month-select',
                                    style={'style-align': 'center', 'margin-top': '30px'},
                                    className='dbc'
                                )
                            ])
                        )
                    ])
                ], style=tab_card)
            ], sm=12, lg=3)
        ], className='g-2 my-auto', style={'margin-top': '7px'}),

        # Construct 2nd row of the dashboard's layout:
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='graph3', className='dbc', config=config_graph)
                            ])
                        ], style=tab_card)
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='graph4', className='dbc', config=config_graph)
                            ])
                        ], style=tab_card)
                    ])
                ], className='g-2 my-auto', style={'margin-top': '7px'})
            ], sm=12, lg=5),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                # Slot for indicator number 1
                                dcc.Graph(id='graph5', className='dbc', config=config_graph)
                            ])
                        ], style=tab_card)
                    ], sm=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                # Slot for indicator number 2
                                dcc.Graph(id='graph6', className='dbc', config=config_graph)
                            ])
                        ], style=tab_card)
                    ], sm=6)
                ], className='g-2'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dcc.Graph(id='graph7', className='dbc', config=config_graph)
                        ], style=tab_card)
                    ])
                ], className='g-2 my-auto', style={'margin-top': '7px'})
            ], sm=12, lg=4),
             # Add the 3rd and last column of the layout for the middle row:
            dbc.Col([
                dbc.Card([
                    dcc.Graph(id='graph8', className='dbc', config=config_graph)
                ], style=tab_card)  #Define style for tabcard of graph 8
            ], sm=12, lg=3)
        ],  className='g-2 my-auto', style={'margin-top': '7px'}),

        # Construct 3rd row of the dashboard's layout:
        dbc.Row([
            # Add the first column:
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Distribuição de Propaganda"),
                        dcc.Graph(id='graph9', className='dbc', config=config_graph)
                    ])
                ], style=tab_card)
            ], sm=12, lg=2),
            # Add the second column:
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Valores de Propaganda Convertidos por Mês"),
                        dcc.Graph(id='graph10', className='dbc', config=config_graph)
                    ])
                ], style=tab_card)  #Get 100% of rows' length
            ], sm=12, lg=5),
            # Add the third column:
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id='graph11', className='dbc', config=config_graph)
                    ])
                ], style=tab_card)
            ], sm=12, lg=3),
            # Add fourth and final column:
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Escolha a equipe:"),
                        dbc.RadioItems(
                            id = 'radio-team',
                            options = team_options,
                            value = 0,
                            inline = True,
                            labelCheckedClassName = 'text-warning',
                            inputCheckedClassName = 'border border-warning bg-warning'
                        ),
                        html.Div(
                            id = 'team-select',
                            style = {'text-align': 'center', 'margin-top': '30px'},
                            className = 'dbc'
                        )
                    ])
                ], style=tab_card)
            ], sm=12, lg=2)
        ], className='g-2 my-auto', style={'margin-top': '7px'})
    ],
    fluid = True,
    style = {'height': '100vh'}
)

# ========================= CONSTRUCT THE CALLBACKS =========================

# Construct first callback for charts 1 and 2 (ref. 1st line)
@app.callback(
    Output(component_id = 'graph1', component_property = 'figure'),
    Output(component_id = 'graph2', component_property = 'figure'),
    Output(component_id = 'month-select', component_property = 'children'),
    Input (component_id = 'radio-month', component_property = 'value'),  #Receives the month selected from radio
    Input (component_id = ThemeSwitchAIO.ids.switch('theme'), component_property = 'value')
)
# Define the function to plot the 1st and 2nd charts
def graph1_and_2 (month, toggle):
    """
    Creates charts 1 and 2 of the dashboard.
    :param month: Month selected by user to filter the charts.
    :param toggle: Changes theme of dashboard (from dark to light and vice versa).
    :return: Figures of charts 1 and 2.
    """
    try:
        # Define change rule for template
        template = template_theme1 if toggle else template_theme2

        # Call function to return the mask for the selected month
        month_mask = month_filter(df=df_final, reference_col='Mês', month=month)

        # Create auxiliary df to return only the selected months
        df_graph = df_final.loc[month_mask]

        # Call function to create the pie chart:
        fig2 = pie_consultant_by_team(df = df_graph,
                                      cols_to_group = ['Consultor', 'Equipe'],
                                      value = 'Valor Pago')
        # Call function to create the bar chart:
        fig1 = bar_consultant_by_team(df = df_graph,
                                      cols_to_group = ['Consultor', 'Equipe'],
                                      value = 'Valor Pago')

        # Update figure's layouts:
        fig1.update_layout(main_config, height=200, template=template)
        fig2.update_layout(main_config, height=200, template=template, showlegend=False)

        # Display on the screen the month selected by the radio:
        select = html.H1(convert_to_text(month))

        return fig1, fig2, select

    except Exception as e:
        logger.error(f"Error while plotting first block of graphs: {str(e)}")
        raise

# ===============================================
    
# Construct second callback for chart 3 (ref. 2nd line)
@app.callback(
    Output(component_id = 'graph3', component_property = 'figure'),
    Input (component_id = 'radio-team', component_property = 'value'),
    Input (component_id = 'radio-month', component_property = 'value'),  #Receives the month selected from radio
    Input (component_id = ThemeSwitchAIO.ids.switch('theme'), component_property = 'value')
)
# Define the function to plot the 3rd chart
def graph3(team, month, toggle):
    """
    Creates chart 3 the dashboard.
    :param team: Team selected by user to filter the charts.
    :param month: Month selected by user to filter the charts.
    :param toggle: Changes theme of dashboard (from dark to light and vice versa).
    :return: Figure of chart 3.
    """
    try:
        # Define change rule for template
        template = template_theme1 if toggle else template_theme2

        # Call function to return the mask for the selected month
        month_mask = month_filter(df=df_final, reference_col='Mês', month=month)

        # Create auxiliary df to return only the selected months
        df_graph = df_final.loc[month_mask]

        # Call function to return the mask for the selected team
        team_mask = team_filter(df=df_final, reference_col='Equipe', team=team)

        # Create auxiliary df to return only the selected teams
        df_graph = df_graph.loc[team_mask]

        # Call function to create the scatter chart
        fig3 = scatter_calls_by_day(df = df_graph,
                                    cols_to_group = 'Dia',
                                    value = 'Chamadas Realizadas')

        # Update figure's layouts
        fig3.update_layout(main_config, height=180, template=template)

        return fig3

    except Exception as e:
        logger.error(f"Error while constructing chart number 3: {str(e)}")
        raise


# ===============================================

# Construct third callback for chart 4 (ref. 2nd line)
@app.callback(
    Output(component_id = 'graph4', component_property = 'figure'),
    Input (component_id = 'radio-team', component_property = 'value'),
    Input (component_id = ThemeSwitchAIO.ids.switch('theme'), component_property = 'value')
)
# Define the function to plot the 4th chart
def graph4(team, toggle):
    """
    Creates chart 4 the dashboard.
    :param team: Team selected by user to filter the charts.
    :param toggle: Changes theme of dashboard (from dark to light and vice versa).
    :return: Figure of chart 4.
    """
    try:
        # Define change rule for template
        template = template_theme1 if toggle else template_theme2

        # Call function to return the mask for the selected team
        team_mask = team_filter(df=df_final, reference_col='Equipe', team=team)

        # Create auxiliary df to return only the selected teams
        df_graph = df_final.loc[team_mask]

        # Call function to create the scatter chart
        fig4 = scatter_calls_by_month(df = df_graph,
                                      cols_to_group = 'Mês',
                                      value = 'Chamadas Realizadas')

        # Update figure's layouts
        fig4.update_layout(main_config, height=180, template=template)

        return fig4

    except Exception as e:
        logger.error(f"Error while constructing chart number 4: {str(e)}")
        raise


# ===============================================

# Construct fourth callback for indicators 1 and 2 (ref. 2nd line)
@app.callback(
    Output(component_id = 'graph5', component_property = 'figure'),
    Output(component_id = 'graph6', component_property = 'figure'),
    Input (component_id = 'radio-month', component_property = 'value'),
    Input (component_id = ThemeSwitchAIO.ids.switch('theme'), component_property = 'value')
)
# Define the function to plot the indicators 1 and 2
def indicator1_and_2(month, toggle):
    """
    Creates indicators 1 and 2 of the dashboard.
    :param month: Month selected by user to filter the charts.
    :param toggle: Changes theme of dashboard (from dark to light and vice versa).
    :return: Figures of indicators 1 and 2.
    """
    try:
        # Define change rule for template
        template = template_theme1 if toggle else template_theme2

        # Call function to return the mask for the selected month
        month_mask = month_filter(df=df_final, reference_col='Mês', month=month)

        # Create auxiliary df to return only the selected months
        df_graph = df_final.loc[month_mask]

        # Call function to create indicator 1:
        fig5 = kpi_best_consultant(df = df_graph,
                                   cols_to_group = ['Consultor', 'Equipe'],
                                   value = 'Valor Pago')

        # Call function to create indicator 2
        fig6 = kpi_best_team(df = df_graph,
                             cols_to_group = 'Equipe',
                             value = 'Valor Pago')

        # Update figure's layouts
        fig5.update_layout(main_config, height=180, template=template)
        fig6.update_layout(main_config, height=180, template=template)
        fig5.update_layout({'margin': {'l': 0, 'r': 0, 't': 50, 'b': 0}})
        fig6.update_layout({'margin': {'l': 0, 'r': 0, 't': 50, 'b': 0}})

        return fig5, fig6

    except Exception as e:
        logger.error(f"Error while constructing indicators 1 and 2: {str(e)}")
        raise


# ===============================================

# Construct fifth callback for chart 5 (ref. 2nd line)
@app.callback(
    Output(component_id = 'graph7', component_property = 'figure'),
    Input (component_id = ThemeSwitchAIO.ids.switch('theme'), component_property = 'value')
)
# Define the function to plot the chart number 5
def graph5(toggle):
    """
    Creates chart number 5 of the dashboard.
    :param toggle: Changes theme of dashboard (from dark to light and vice versa).
    :return: Figures of chart number 5.
    """
    try:
        # Define change rule for template
        template = template_theme1 if toggle else template_theme2

        # Create auxiliary df to return only the selected months
        # df_graph = df_final.copy()

        # Call function to create chart number 5
        fig7 = scatter_sales_month_teams(df = df_final,
                                         cols_to_group = ['Mês', 'Equipe'],
                                         value = 'Valor Pago')

        # Update figure's layouts
        fig7.update_layout(main_config,
                           yaxis = {'title': None}, xaxis = {'title': None},
                           height = 210, template = template)
        fig7.update_layout({'legend': {'yanchor': 'top',
                                       'y': 0.99,
                                       'font': {'color': 'white', 'size': 10}}})

        return fig7

    except Exception as e:
        logger.error(f"Error while constructing chart number 5: {str(e)}")
        raise


# ===============================================

# Construct sixth callback for chart 6 (ref. 2nd line)
@app.callback(
    Output(component_id = 'graph8', component_property = 'figure'),
    Input (component_id = 'radio-month', component_property = 'value'),
    Input (component_id = ThemeSwitchAIO.ids.switch('theme'), component_property = 'value')
)
# Define the function to plot the chart number 6
def graph6(month, toggle):
    """
    Creates chart 6 the dashboard.
    :param team: Team selected by user to filter the charts. ???????
    :param month: Month selected by user to filter the charts.
    :param toggle: Changes theme of dashboard (from dark to light and vice versa).
    :return: Figure of chart 6.
    """
    try:
        # Define change rule for template
        template = template_theme1 if toggle else template_theme2

        # Call function to return the mask for the selected month
        month_mask = month_filter(df=df_final, reference_col='Mês', month=month)

        # Create auxiliary df to return only the selected months
        df_graph = df_final.loc[month_mask]

        # Call function to create chart number 6:
        fig8 = bar_sales_by_team(df = df_graph,
                                 cols_to_group = 'Equipe',
                                 value = 'Valor Pago')

        # Update figure's layouts
        fig8.update_layout(main_config, height = 360, template = template)

        return fig8

    except Exception as e:
        logger.error(f"Error while constructing chart number 6: {str(e)}")
        raise


# ===============================================

# Construct seventh callback for chart 7 (ref. 3rd line)
@app.callback(
    Output(component_id = 'graph9', component_property = 'figure'),
    Input (component_id = 'radio-month', component_property = 'value'),
    Input (component_id = 'radio-team', component_property = 'value'),
    Input (component_id = ThemeSwitchAIO.ids.switch('theme'), component_property = 'value')
)
# Define the function to plot the chart number 7:
def graph7(month, team, toggle):
    """
    Creates chart 7 the dashboard.
    :param team: Team selected by user to filter the charts.
    :param month: Month selected by user to filter the charts.
    :param toggle: Changes theme of dashboard (from dark to light and vice versa).
    :return: Figure of chart 7.
    """
    try:
        # Define change rule for template
        template = template_theme1 if toggle else template_theme2

        # Call function to return the mask for the selected month
        month_mask = month_filter(df=df_final, reference_col='Mês', month=month)
        # Create auxiliary df to return only the selected months
        df_graph = df_final.loc[month_mask]

        # Call function to return the mask for the selected team
        team_mask = team_filter(df=df_final, reference_col='Equipe', team=team)
        # Create auxiliary df to return only the selected teams
        df_graph = df_graph.loc[team_mask]

        # Call function to create the scatter chart
        fig9 = paym_by_channel(df = df_graph,
                               cols_to_group = 'Meio de Propaganda',
                               value = 'Valor Pago')

        # Update figure's layouts
        fig9.update_layout(main_config, height = 200, template = template, showlegend = False)

        return fig9

    except Exception as e:
        logger.error(f"Error while constructing chart number 7: {str(e)}")
        raise


# ===============================================

# Construct eighth callback for chart 8 (ref. 3rd line)
@app.callback(
    Output(component_id = 'graph10', component_property = 'figure'),
    Input (component_id = 'radio-team', component_property = 'value'),
    Input (component_id = ThemeSwitchAIO.ids.switch('theme'), component_property = 'value')
)
# Define the function to plot the chart number 8:
def graph8(team, toggle):
    """

    :param team:
    :param toggle:
    :return:
    """
    try:
        # Define change rule for template
        template = template_theme1 if toggle else template_theme2

        # Call function to return the mask for the selected team
        team_mask = team_filter(df=df_final, reference_col='Equipe', team=team)

        # Create auxiliary df to return only the selected teams
        df_graph = df_final.loc[team_mask]

        # Call function to create the scatter chart
        fig10 = paym_by_channel_over_months(df = df_graph,
                                            cols_to_group = ['Meio de Propaganda', 'Mês'],
                                            value = 'Valor Pago')

        # Update figure's layouts
        fig10.update_layout(main_config, height = 360, template = template, showlegend = False)

        fig10.update_layout({'legend': {'yanchor': 'top',
                                       'y': 0.99,
                                       'font': {'color': 'white', 'size': 10}}})

        return fig10

    except Exception as e:
        logger.error(f"Error while constructing chart number 8: {str(e)}")
        raise

# ===============================================

# Construct nineth callback for indicator number 3 (ref. 3rd line)
@app.callback(
    Output(component_id = 'graph11', component_property = 'figure'),
    Output(component_id = 'team-select', component_property = 'children'),
    Input (component_id = 'radio-month', component_property = 'value'),
    Input (component_id = 'radio-team', component_property = 'value'),
    Input (component_id = ThemeSwitchAIO.ids.switch('theme'), component_property = 'value')
)
# Define the function to plot the indicator number 3:
def indicator3(month, team, toggle):
    """

    :param month:
    :param team:
    :param toggle:
    :return:
    """
    try:
        # Define change rule for template
        template = template_theme1 if toggle else template_theme2

        # Call function to return the mask for the selected month
        month_mask = month_filter(df=df_final, reference_col='Mês', month=month)
        # Create auxiliary df to return only the selected months
        df_graph = df_final.loc[month_mask]

        # Call function to return the mask for the selected team
        team_mask = team_filter(df=df_final, reference_col='Equipe', team=team)
        # Create auxiliary df to return only the selected teams
        df_graph = df_graph.loc[team_mask]

        # Call function to create the scatter chart
        fig11 = total_sales(df = df_graph, value = 'Valor Pago')

        # Update figure's layouts
        fig11.update_layout(main_config, height = 300, template = template)

        # Display on the screen the team selected by the radio:
        select_team = html.H1("Todas as equipes") if team == 0 else html.H1(team)

        return fig11, select_team

    except Exception as e:
        logger.error(f"Error while constructing indicator number 3: {str(e)}")
        raise


# ===========================================================================


# Run the app:
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
