
from ampalibe import webserver

@webserver.get('/custom')
def test():
    return 'Un endpoint cutomiser'