import locale
locale.setlocale(locale.LC_ALL, 'C')

def format_currency(amount):
    return '${:,.2f}'.format(amount)
    
def format_currency_millions(amount):
    return '${:,.2f}'.format(amount / 1000000)