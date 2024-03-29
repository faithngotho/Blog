import urllib.request,json
from .models import Quote

def get_quote():
    '''
    Function that gets the json response to our url request
    '''

    with urllib.request.urlopen("http://quotes.stormconsultancy.co.uk/random.json") as url:
        get_quote_data = url.read()
        get_quote_response = json.loads(get_quote_data)

        quote_results = None

        if get_quote_response:
            author = get_quote_response.get('author')
            quote = get_quote_response.get('quote')
            quote_results = Quote(author,quote)
    return quote_results