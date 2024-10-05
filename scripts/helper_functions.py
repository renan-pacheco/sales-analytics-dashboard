import logging

def setup_logger(log_file):
    try:
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

    except Exception as e:
        logging.error(f"Error while creating the logger: {str(e)}")
        raise

# Configure the logger:
logger = setup_logger('../logging/helper_functions.log')


def month_filter(df, reference_col, month):
    """
    Defines a mask for the month selected within the dashboard and
    used by the index.py script
    :return: the mask as a string.
    """
    try:
        if month == 0:
            # If the selected month is equal to 0, the mask returns all possible months
            mask = df[reference_col].isin(df[reference_col].unique())
        else:
            mask = df[reference_col].isin([month])

        return mask

    except Exception as e:
        logger.error(f"Error filtering the month: {str(e)}")
        raise


def convert_to_text(month):
    """
    Receives month selected by user and returns a list of months.
    :return: Index of list of months.
    """
    try:
        months_list = ['Ano inteiro', 'Janeiro', 'Fevereiro', 'Março', 'Abril',
                       'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro',
                       'Novembro', 'Dezembro']

        return months_list[month]

    except Exception as e:
        logger.error(f"Error converting month to text: {str(e)}")
        raise


def team_filter(df, reference_col, team):
    """
    Defines a mask for the team selected within the dashboard and
    used by the index.py script.
    :return: the mask as a string.
    """
    try:
        if team == 0:
            mask = df[reference_col].isin(df[reference_col].unique())
        else:
            mask = df[reference_col].isin([team])

        return mask

    except Exception as e:
        logger.error(f"Error while filtering the team values: {str(e)}")
        raise