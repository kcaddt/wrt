#!/usr/bin/python

from flask import Flask
from {{ methods_file }} imports {{ methods_list }}

app = Flask(__name__)

{% for method in methods %}
@app.route("/{{method.name}}/")
{{method.content}}

{% endfor %}

if __name__ == '__main__':
    app.run(host='{{ host }}', port={{ port }})
