import babel, app

@app.template_filter('dt')
def format_datetime(value, format='medium'):
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format="dd/MM/y"
    return babel.dates.format_datetime(value, format)