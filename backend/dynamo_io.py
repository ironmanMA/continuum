__author__ = 'mohammad'

import boto.dynamodb
import simplejson as json

AWS_ACCESS_KEY = 'AKIAJ6XUO5KUSL2ZQKSA'
AWS_SECRET_KEY = '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'

conn = boto.dynamodb.connect_to_region(
        'us-west-2',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY)

table = conn.get_table('boomboard')


def json_dump(json_data):
    return json_data

def get_item (metric, date):
    json_content = '{"error":"true"}'
    print metric, date
    try:
        item = table.get_item(hash_key=metric, range_key=date)
        json_content = str(item['value'])
    except Exception:
      pass

    json_data = json.loads(json_content)
    return json_dump(json_data)


def put_item( metric, date, value):

    print metric, date, value

    item_data = {
        'value': value
    }
    item = table.new_item(
        hash_key=metric,
        range_key=date,
        attrs=item_data
    )
    item.put()