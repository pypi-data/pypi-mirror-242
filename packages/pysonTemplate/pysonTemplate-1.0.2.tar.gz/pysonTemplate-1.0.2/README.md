use the library in other Python scripts. 
Create a new Python script in a different directory and 
import and use the send function from the library

```
from python.xTemplate import Template as template

self.template = template()

self.template.send_email(table_html)

[Email]
smtp_server='mrelay.noc.sony.co.jp'
smtp_port=25
sender='SCK-VOS_MAP_SYSTEM@sony.com'


python setup.py sdist bdist_wheel

twine upload dist/*


def db_commit_many(self, params):
    try:
        db_connection = self.database_connector.connectPostgreSQL(**params)
        db_connection.commit_many(params['query'], params['values'])

    except Exception as error:
        self.handle_error(error)

# Example of using the function
params = {
    'db': 'your_db',
    'host': 'your_host',
    'user': 'your_user',
    'pw': 'your_password',
    'port': 'your_port',
    'schemas': 'your_schemas'
}

self.db_commit_many(params)



email_message = {
    "message_body": "Your email message body here",
    "recipient": "recipient@example.com",
    "recipient_cc": "cc@example.com",
    "subject": "Your email subject here",
    "header":"your header",
    "header2":"your header2",
    "footer":"your footer",
    "footer2":"your footer2"
}
```

