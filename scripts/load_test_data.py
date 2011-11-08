try:
    import json
except ImportError:
    import simplejson as json
import urllib2

API_HOST = 'http://localhost:8000'
API_KEY = 'test'

DATA_FEEDS = [
    {
        'type': 'instructors',
        'file': 'instructors.json',
        'url': '/instructor/import/',
    },
    {
        'type': 'students',
        'file': 'students.json',
        'url': '/student/import/',
    },
    {
        'type': 'sections',
        'file': 'sections.json',
        'url': '/section/import/',
    },
    {
        'type': 'enrollments',
        'file': 'enrollments.json',
        'url': '/enrollment/import/',
    },
]

for feed in DATA_FEEDS:
    # Open JSON file, read contents, close JSON file
    f = file('test_data/%s' % feed['file'])
    data = f.read()
    f.close()

    # 1. Convert JSON to Python list
    # 2. Add some extra attributes
    # 3. Convert Python list to JSON
    data = json.loads(data)
    data = json.dumps([{
        'api_key': API_KEY,
        feed['type']: data
    }])

    # Open HTTP request to API
    req = urllib2.Request('%s/api%s' % (API_HOST, feed['url']))

    # Attach Content-type header and POST data
    req.add_header('Content-type', 'application/json')
    req.add_data(data)

    # Make request and read response
    res = urllib2.urlopen(req)
    out = res.read()

    # Close HTTP connection
    res.close()

    # Print response from API
    print out
