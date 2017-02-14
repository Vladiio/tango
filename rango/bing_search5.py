import requests


def main():
    search_terms = input('What do you looking for?: ')
    results = bing_search(search_terms)
    for result in results:
        print(result['title'])
        print(result['link'])
        print(result['summary'])
        print('-'* 100)



def read_bing_key():
    bing_api_key = None
    try:
        with open('bing.key', 'r') as file:
            bing_api_key = file.readline()
    except:
        raise IOError('bing.key file not found')

    return bing_api_key


def bing_search(query):
    url = 'https://api.cognitive.microsoft.com/bing/v5.0/search'
    # query string parameters
    payload = {'q': query}
    # custom headers
    bing_api_key = read_bing_key()
    headers = {'Ocp-Apim-Subscription-Key': '{0}'.format(bing_api_key)}
    # make GET request
    r = requests.get(url, params=payload, headers=headers)
    # get JSON response
    r = r.json()
    results = []

    for result in r.get('webPages', {}).get('value', {}):
        results.append({
            'title': result['name'],
            'link': result['url'],
            'summary': result['snippet'],
        })

    return results


if __name__ == '__main__':
    main()
