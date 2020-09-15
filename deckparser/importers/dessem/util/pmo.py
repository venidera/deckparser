from dateutil.relativedelta import relativedelta
from datetime import timedelta, date

def isFirstOperativeDay(d): # sábado
    return d.weekday() == 5

def firstOperativeDay(d):
    wd = d.weekday()
    if wd >= 5: # sábado e domingo
        delta_d = 5-wd
    else:
        delta_d = -(wd+2)
    return d + timedelta(days=delta_d)

def first_pmo_date(pmo_month):
    first_day = pmo_month.replace(day=1)
    return firstOperativeDay(first_day)

def pmo_date_range(pmo_month):
    next_month = pmo_month + relativedelta(months=1)
    return [first_pmo_date(pmo_month),
            first_pmo_date(next_month) + timedelta(days=-1)]

def pmo_date_list(pmo_month):
    sd,ed = pmo_date_range(pmo_month)
    return [sd + timedelta(days=i) for i in range(0, (ed-sd).days + 1)]

def get_pmo_month(deck_date):
    pmo_month = deck_date.replace(day=1)
    pmo_range = pmo_date_range(pmo_month)
    if pmo_range[0] <= deck_date <= pmo_range[1]:
        return pmo_month
    return pmo_month + relativedelta(months=1)

def real_month(rv, d, m, y):
    m_date = date(y,m,1)
    if rv == 0 and d > 20:
        m_date -= relativedelta(months=1)
    elif rv > 3 and d < 10:
        m_date += relativedelta(months=1)
    return m_date

def real_date(rv, d, m, y):
    m_date = real_month(rv, d, m, y)
    try:
        return m_date.replace(day=d)
    except:
        return None
        #raise ValueError('Invalid deck date: {:d}-{:d}-{:d} rv {:d}'.format(y,m,d,rv))

# from datetime import date
# import json
# date_list = [date(2020,1,1) + timedelta(days=i) for i in range(365)]
# for d in date_list:
#     print((d, get_pmo_month(d)))

