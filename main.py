import requests
import csv
import funtions.connections as connections
import conf.constants as constants

connections.ssh_connect()
connections.sql_connect()

data = csv.DictReader(open(constants.PATH_FILE, 'r'))
headers = {
    'Authorization': 'Bearer {}'.format(constants.AUTH),
    'Content-Type': 'application/json'
}

for row in data:
    print('value = ' + row['value'] + '\nlabel = ' + row['label'])

    body = constants.BODY.replace('{value}', row['value'])

    print('body = ' + body)

    url = "{}/{}".format(constants.MAGENTO_URL, constants.API_URL)
    print('url = ' + url)

    response = requests.post(url=url, headers=headers, data=body)

    if response.status_code == 200:
        option_id = response.text.replace('"', '')

        if "_" in response.text:
            option_id = option_id.split('_')[1]

        for store in connections.select_query('SELECT store_id, name FROM store'):

            if store['store_id'] != 0:
                print('adding option to store ' + store['name'])

                query_value = f"INSERT INTO eav_attribute_option_value SET option_id = {int(option_id)}, store_id = {store['store_id']}, value = '{row['label']}'"
                query_swatch = f"INSERT INTO eav_attribute_option_swatch SET option_id = {int(option_id)}, store_id = {store['store_id']}, value = '{row['label']}', type = 0 "

                print(f"{query_value}\n{query_swatch}")

                value_id = connections.insert_query(query_value)
                print(f'value_id : {value_id}')

                swatch_id = connections.insert_query(query_swatch)
                print(f'swatch_id : {swatch_id}')

    else:
        print(response.status_code)
        print(response.text)

connections.sql_disconnect()
connections.ssh_disconnect()
