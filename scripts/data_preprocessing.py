import warnings
import pandas as pd
from datetime import timedelta

# Prevent warning messages to be printed on the screen:
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# To display all columns within the terminal space
pd.options.display.width = 0
pd.options.display.max_columns = None
pd.options.display.max_rows = None

# Import the dataset:
df = pd.read_csv("../datasets/sales_raw.csv")
#df = pd.read_csv("asimov_academy/Interactive_Dashboards_Track/Dash/Sales Analysis Project/datasets/sales_analysis.csv")

# Rename the values from column 'month' as numbers:
df.loc[df['Mês'] == 'Jan', 'Mês'] = 1
df.loc[df['Mês'] == 'Fev', 'Mês'] = 2
df.loc[df['Mês'] == 'Mar', 'Mês'] = 3
df.loc[df['Mês'] == 'Abr', 'Mês'] = 4
df.loc[df['Mês'] == 'Mai', 'Mês'] = 5
df.loc[df['Mês'] == 'Jun', 'Mês'] = 6
df.loc[df['Mês'] == 'Jul', 'Mês'] = 7
df.loc[df['Mês'] == 'Ago', 'Mês'] = 8
df.loc[df['Mês'] == 'Set', 'Mês'] = 9
df.loc[df['Mês'] == 'Out', 'Mês'] = 10
df.loc[df['Mês'] == 'Nov', 'Mês'] = 11
df.loc[df['Mês'] == 'Dez', 'Mês'] = 12

# Change data types:
df['Mês'] = df['Mês'].astype(int)
# df['Valor Pago'] = df['Valor Pago'].apply(lambda x: int(x.replace('R$', '').strip()))
df['Valor Pago'] = df['Valor Pago'].str.lstrip("R$ ").astype(int)
df['Duração da chamada'] = df['Duração da chamada'].apply(
    lambda x: str(timedelta(minutes=int(x.split(':')[0]), seconds=int(x.split(':')[1])))
).apply(lambda x: x.split(", ")[-1])  # Remove "days" part if present

df.loc[df['Status de Pagamento'] == 'Pago', 'Status de Pagamento'] = 1
df.loc[df['Status de Pagamento'] == 'Não pago', 'Status de Pagamento'] = 0

# Export cleaned dataset:
df.to_csv("../datasets/sales_analysis.csv", index=False)

