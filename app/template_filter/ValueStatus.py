from app import app
from app.routes.scan import threadScanner

@app.template_filter('value_status_file')
def value_status_file(status_number):
    return {
        0:'Waiting',
        1:'In progress ( '+str(threadScanner.get_percent())+' % )',
        2:'Finished',
        -1:'Failure'
    }[status_number]