import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import logging

def setup_logger(log_file):
    """Set up a logger to log events to both console and a file."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Log to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Log to file
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

# Configure the logger:
logger = setup_logger('../logging/visualizations.log')


# ======================= TOP CONSULTANT BY EACH TEAM AND SALES (PIE CHART) ==========================

def pie_consultant_by_team(df, cols_to_group, value):
    """

    :param df:
    :param cols_to_group:
    :param value:
    :return:
    """
    try:
        # Define the dataframe:
        top_consult_team_sales = df.groupby(cols_to_group)[value].sum().\
            sort_values(ascending=False).groupby(cols_to_group[1]).head(1).reset_index()

        # Construct the visualization:
        fig1 = go.Figure()
        fig1.add_trace(
            go.Pie(
                labels = top_consult_team_sales[cols_to_group[0]] + " (" + top_consult_team_sales[cols_to_group[1]] + ")",
                values = top_consult_team_sales[value],
                hole = 0.5
            )
        )

        return fig1

    except Exception as e:
        logger.error(f"Error while constructing chart number 1: {str(e)}")
        raise


# ======================= TOP CONSULTANT BY EACH TEAM AND SALES (BAR CHART) =============================

def bar_consultant_by_team(df, cols_to_group, value):
    """

    :param df:
    :param cols_to_group:
    :param value:
    :return:
    """
    try:
        # Define the dataframe:
        top_consult_team_sales = df.groupby(cols_to_group)[value].sum(). \
            sort_values(ascending=False).groupby(cols_to_group[1]).head(1).reset_index()

        # Construct the visualization:
        fig2 = go.Figure()
        fig2.add_trace(
            go.Bar(
                x=top_consult_team_sales[cols_to_group[0]],
                y=top_consult_team_sales[value],
                textposition='auto',
                text=top_consult_team_sales[value],
                marker=dict(
                    color='lightsteelblue',
                    colorscale='Viridis'  # Optional: Choose a colorscale, or remove this for default colors
                )
            )
        )

        return fig2

    except Exception as e:
        logger.error(f"Error while constructing chart number 2: {str(e)}")
        raise


# ================================= TOTAL CALLS BY DAY OF MONTH =======================================

def scatter_calls_by_day(df, cols_to_group, value):
    """

    :param df:
    :param cols_to_group:
    :param value:
    :return:
    """
    try:
        # Create auxiliary dataframe:
        calls_by_day = df.groupby(cols_to_group)[value].sum().reset_index()

        # Build the chart:
        fig3 = go.Figure(
            go.Scatter(
                x = calls_by_day[cols_to_group],
                y = calls_by_day[value],
                mode = 'lines',
                fill = 'tonexty'
            )
        )
        # Add anotations to the chart:
        fig3.add_annotation(
            text = "Total de chamadas por dia do mês",
            xref = 'paper', yref = 'paper',
            font = dict(size=17, color='gray'),
            align = 'center',
            bgcolor = "rgba(0, 0, 0, 0.8)",
            x = 0.05, y = 0.85, showarrow = False
        )
        fig3.add_annotation(
            text = f"Média: {round(calls_by_day[value].mean(), 2)}",
            xref = 'paper', yref = 'paper',
            font = dict(size=20, color='gray'),
            align = 'center', bgcolor = "rgba(0, 0, 0, 0.8)",
            x = 0.05, y=0.55, showarrow=False
        )

        return fig3  #Returns scatter figure.

    except Exception as e:
        logger.error(f"Error while constructing scatter plot (graph 3): {str(e)}")
        raise


# ===================== TOTAL CALLS BY MONTH ===========================

def scatter_calls_by_month(df, cols_to_group, value):
    """

    :param df:
    :param cols_to_group:
    :param value:
    :return:
    """
    try:
        # Create dataframe to be used by visualization:
        calls_by_month = df.groupby(cols_to_group)[value].sum().reset_index()

        # Construct chart:
        fig4 = go.Figure(
            go.Scatter(
                x=calls_by_month[cols_to_group],
                y=calls_by_month[value],
                mode='lines',
                fill='tonexty'
            )
        )

        # Add annotations to the chart:
        fig4.add_annotation(
            text="Total de chamadas por mês",
            xref='paper', yref='paper',
            font=dict(size=15, color='grey'),
            align='center', bgcolor="rgba(0, 0, 0, 0.8)",
            x=0.05, y=0.85, showarrow=False
        )
        fig4.add_annotation(
            text=f"Média: {round(calls_by_month[value].mean(), 2)}",
            xref='paper', yref='paper',
            font=dict(size=20, color='gray'),
            align='center', bgcolor="rgba(0, 0, 0, 0.8)",
            x=0.05, y=0.55, showarrow=False
        )

        return fig4

    except Exception as e:
        logger.error(f"Error while constructing chart number 4: {str(e)}")
        raise


# ==================== INDICATOR: BEST SALESPERSON/CONSULTANT =========================

def kpi_best_consultant(df, cols_to_group, value):
    """

    :param df:
    :param cols_to_group:
    :param value:
    :return:
    """
    try:
        # Define the dataframe:
        best_consultant = df.groupby(cols_to_group)[value].sum(). \
            reset_index().sort_values(by=value, ascending=False).reset_index(drop=True)

        # Build the visualization:
        fig5 = go.Figure()
        fig5.add_trace(
            go.Indicator(
                mode='number+delta',
                title={"text": f"<span>{best_consultant[cols_to_group[0]].iloc[0]} - "
                               f"Top Consultant ({best_consultant[cols_to_group[1]].iloc[0]})</span><br>"
                               f"<span style='font-size: 70%'>Vendas - Em relação a média</span><br>"
                       },
                value=best_consultant[value].iloc[0],
                number={'prefix': "R$ "},
                delta={'relative': True, 'valueformat': '.2%', 'reference': best_consultant[value].mean()}
            )
        )

        return fig5

    except Exception as e:
        logger.error(f"Error while constructing the 1st indicator: {str(e)}")
        raise


# ========================= INDICATOR: BEST TEAM ===============================

def kpi_best_team(df, cols_to_group, value):
    """

    :param df:
    :param cols_to_group:
    :param value:
    :return:
    """
    try:
        # Define the dataframe:
        best_team = df.groupby(cols_to_group)[value].sum().reset_index(). \
            sort_values(by=value, ascending=False)

        # Construct the indicator' visualization:
        fig6 = go.Figure()
        fig6.add_trace(
            go.Indicator(
                mode='number+delta',
                title={"text": f"<span>{best_team[cols_to_group].iloc[0]} - Top Team"
                               f"</span><br><span style='font-size: 70%'>Vendas - Em relação a média</span><br>"
                       },
                value=best_team[value].iloc[0],
                number={'prefix': "R$ "},
                delta={'relative': True, 'valueformat': '.2%', 'reference': best_team[value].mean()}
            )
        )

        return fig6

    except Exception as e:
        logger.error(f"Error while constructing indicator number 2: {str(e)}")
        raise


# ================ EARNINGS BY MONTH SEGREGATED BY TEAMS ======================

def scatter_sales_month_teams(df, cols_to_group, value):
    """

    :param df:
    :param cols_to_group:
    :param value:
    :return:
    """
    try:
        # Create necessary dataframes:
        paym_over_months_by_team = df.groupby(cols_to_group)[value].sum().reset_index()
        payment_by_team = df.groupby(cols_to_group[0])[value].sum().reset_index()

        # Build the visualization:
        fig7 = px.line(
            data_frame=paym_over_months_by_team,
            x=cols_to_group[0], y=value, color=cols_to_group[1]
        )

        # Update the chart:
        fig7.add_trace(
            go.Scatter(
                x=payment_by_team[cols_to_group[0]],
                y=payment_by_team[value],
                mode='lines+markers', fill='tonexty',
                fillcolor="rgba(255, 0, 0, 0.2)",
                name="Total de Vendas"
            )
        )

        return fig7

    except Exception as e:
        logger.error(f"Error while constructing chart number 5: {str(e)}")
        raise


# ===================== TOTAL OF SALES BY TEAM ==================================

def bar_sales_by_team(df, cols_to_group, value):
    """

    :param df:
    :param cols_to_group:
    :param value:
    :return:
    """
    try:
        # Create auxiliary dataframe:
        sales_by_team = df.groupby(cols_to_group)[value].sum(). \
            reset_index().sort_values(by=value, ascending=False)

        # Build the chart:
        fig8 = go.Figure(
            go.Bar(
                x=sales_by_team[value],
                y=sales_by_team[cols_to_group],
                orientation='h',
                textposition='auto',
                text=sales_by_team[value],
                insidetextfont=dict(family="Times", size=12)
            )
        )

        return fig8

    except Exception as e:
        logger.error(f"Error while constructing chart number 6: {str(e)}")
        raise


# ================ TOTAL PAYMENTS BY MARKETING CHANNEL ======================

def paym_by_channel(df, cols_to_group, value):
    """

    :param df:
    :param cols_to_group:
    :param value:
    :return:
    """
    try:
        # Create dataframe:
        paym_by_channel = df.groupby(cols_to_group)[value].sum().reset_index()

        # Construct the visualization:
        fig9 = go.Figure()  # Instantiate the figure
        fig9.add_trace(
            go.Pie(
                labels=paym_by_channel[cols_to_group],
                values=paym_by_channel[value],
                hole=0.5
            )
        )
        return fig9

    except Exception as e:
        logger.error(f"Error while constructing chart number 7: {str(e)}")
        raise


# ============= TOTAL PAYMENTS BY MARKETING CHANNEL OVER MONTHS ===================

def paym_by_channel_over_months(df, cols_to_group, value):
    """

    :param df:
    :param cols_to_group:
    :param value:
    :return:
    """
    try:
        # Create dataframe:
        paym_over_months_by_mkt = df.groupby(cols_to_group)[value].sum().reset_index()

        # Construct the visualization:
        fig10 = px.line(
            data_frame=paym_over_months_by_mkt,
            x=cols_to_group[1], y=value,
            color=cols_to_group[0]
        )

        return fig10

    except Exception as e:
        logger.error(f"Error while constructing chart number 8: {str(e)}")
        raise


# ========================= INDICATOR: TOTAL OF EARNINGS ===============================

def total_sales(df, value):
    """

    :param df:
    :param cols_to_group:
    :param value:
    :return:
    """
    try:
        # Build the indicator's visualization:
        fig11 = go.Figure()
        fig11.add_trace(
            go.Indicator(
                mode='number',
                title={
                    "text": f"<span style='font-size: 150%'>Valor Total</span><br><span style='font-size= 70%>Em Reais</span>"},
                value=df[value].sum(),
                number={'prefix': "R$ "}
            )
        )

        return fig11

    except Exception as e:
        logger.error(f"Error while constructing indicator number 3: {str(e)}")
        raise


# ============== PAYMENTS AND NO-PAYMENTS WITH RESPECT TO CALLS MADE ===================

# # Define the dataframe:
# paym_status = df.groupby('Status de Pagamento')['Chamadas Realizadas'].sum().reset_index()
#
# # Build the visualization:
# fig6 = go.Figure()
# fig6.add_trace(
#     go.Pie(
#         labels = ['Não Pago', 'Pago'], values = paym_status['Chamadas Realizadas'], hole = 0.6
#     )
# )

# ======================== INDICATOR: TOTAL OF CALLS MADE ===========================

# # Build the indicator's visualization:
# fig10 = go.Figure()
# fig10.add_trace(
#     go.Indicator(
#         mode = 'number',
#         title = {"text": f"<span style='font-size: 150%'>Total Chamadas Realizadas</span>"},
#         value = len(df[df['Status de Pagamento'] == 1])
#     )
# )

# ====================================================================================

# The 'color' property is a color and may be specified as:
#       - A hex string (e.g. '#ff0000')
#       - An rgb/rgba string (e.g. 'rgb(255,0,0)')
#       - An hsl/hsla string (e.g. 'hsl(0,100%,50%)')
#       - An hsv/hsva string (e.g. 'hsv(0,100%,100%)')
#       - A named CSS color:
#             aliceblue, antiquewhite, aqua, aquamarine, azure,
#             beige, bisque, black, blanchedalmond, blue,
#             blueviolet, brown, burlywood, cadetblue,
#             chartreuse, chocolate, coral, cornflowerblue,
#             cornsilk, crimson, cyan, darkblue, darkcyan,
#             darkgoldenrod, darkgray, darkgrey, darkgreen,
#             darkkhaki, darkmagenta, darkolivegreen, darkorange,
#             darkorchid, darkred, darksalmon, darkseagreen,
#             darkslateblue, darkslategray, darkslategrey,
#             darkturquoise, darkviolet, deeppink, deepskyblue,
#             dimgray, dimgrey, dodgerblue, firebrick,
#             floralwhite, forestgreen, fuchsia, gainsboro,
#             ghostwhite, gold, goldenrod, gray, grey, green,
#             greenyellow, honeydew, hotpink, indianred, indigo,
#             ivory, khaki, lavender, lavenderblush, lawngreen,
#             lemonchiffon, lightblue, lightcoral, lightcyan,
#             lightgoldenrodyellow, lightgray, lightgrey,
#             lightgreen, lightpink, lightsalmon, lightseagreen,
#             lightskyblue, lightslategray, lightslategrey,
#             lightsteelblue, lightyellow, lime, limegreen,
#             linen, magenta, maroon, mediumaquamarine,
#             mediumblue, mediumorchid, mediumpurple,
#             mediumseagreen, mediumslateblue, mediumspringgreen,
#             mediumturquoise, mediumvioletred, midnightblue,
#             mintcream, mistyrose, moccasin, navajowhite, navy,
#             oldlace, olive, olivedrab, orange, orangered,
#             orchid, palegoldenrod, palegreen, paleturquoise,
#             palevioletred, papayawhip, peachpuff, peru, pink,
#             plum, powderblue, purple, red, rosybrown,
#             royalblue, rebeccapurple, saddlebrown, salmon,
#             sandybrown, seagreen, seashell, sienna, silver,
#             skyblue, slateblue, slategray, slategrey, snow,
#             springgreen, steelblue, tan, teal, thistle, tomato,
#             turquoise, violet, wheat, white, whitesmoke,
#             yellow, yellowgreen

