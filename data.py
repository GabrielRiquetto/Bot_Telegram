from datetime import datetime

def transformDate(day, month, year):
    meses = {"01": "january", "02": "february", "03": "march", "04": "april", "05": "may", "06": "june", "07": "july", "08": "august", "09": "september", "10": "october", "11": "november", "12": "december"}
    date_str2 = f'{day}/{month}/{year}'
    try:
        date_dt2 = datetime.strptime(date_str2, '%d/%m/%Y')
        if date_dt2.weekday() == 0:
            return meses[month]
        else:
            return False
    except ValueError:
        return False
