import datetime as dt


def year(requset):
    year = dt.datetime.now().year
    context = {'year': year}
    return(context)
