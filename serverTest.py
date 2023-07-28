from flask import Flask, jsonify
from flask_cors import CORS
import requests
import datetime
import time
import pytz



application = Flask(__name__)
app = application
CORS(app)

def get_slots(x, y, wallet, auth):
        headers = {
            'authority': 'api.plantvsundead.com',
            'accept': 'application/json',
            'accept-language': 'pt-BR,pt;q=0.7',
            'authorization': f'{auth}',
            'content-type': 'application/json;charset=UTF-8',
            'internal-api-key': 'key_for_testing_pvu_2023',
            'origin': 'https://marketplace.plantvsundead.com',
            'referer': 'https://marketplace.plantvsundead.com/',
            'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'x-u-a-check': 'Android-Unity-Farm',
        }

        params = {
            'x': str(x),
            'y': str(y),
        }

        response = requests.get('https://api.plantvsundead.com/lands/get-by-coordinate', params=params, headers=headers)
        json_data = response.json()
        slots = []

        for slot in json_data["data"][0]["slots"]:
            if "_id" in slot and slot.get("type") == 1 and slot.get("ownerId").lower() == f"{wallet}":
                location = slot.get("location")
                slots.append(location)

        return slots
               

def verificar_colheita(user, x, y):

    resultados = []

    if user == 'mira':
        auth = 'bearerHeader eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNBZGRyZXNzIjoiMHg0ODQ3Y2QxNWRkM2EzNGU2NzUyMzQ1OTJjNjY1NGNjNDM4NDExNzM3IiwiaWF0IjoxNjg0ODYxNjYzfQ.Ew0HQXTmMI0H4QAUMH4HG_MQqpKVvwAxKYi04MUqr30'
        wallet = '0x4847cd15dd3a34e675234592c6654cc438411737'
    elif user=='sakamoto':
        auth = 'bearerHeader eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNBZGRyZXNzIjoiMHhhMWY5NGUyMWM3N2I2NmYzYjcwMDI3MDM3YTEzZmZmNmFlMzNlZDA3IiwiaWF0IjoxNjg1NDA0NDA3fQ.AX_hgeSqiDBtNTgV2Pm6AZHJAjCiVWD5ochydUCcJnM'
        wallet = '0xa1f94e21c77b66f3b70027037a13fff6ae33ed07'
    elif user == 'shmervz':
        auth = 'bearerHeader eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNBZGRyZXNzIjoiMHgyZWYxOTAzN2ExOTE5NzU4OGEyZTcwMWViNzlmYTc5MmZmMGVhZGYwIiwiaWF0IjoxNjg1MTEwNTMyfQ.LsC4T-b1I_1-yBcjj7yN9IoeXmT7gKOrvq4XbbAY9rc'
        wallet = '0x2ef19037a19197588a2e701eb79fa792ff0eadf0'
    elif user == 'chsdust':
        auth = 'bearerHeader eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNBZGRyZXNzIjoiMHhjZWRjNGEzMWQwNWNmM2ExM2Y1ODA3ZGY1ZGRjODlhNjEyOTNkYzU5IiwiaWF0IjoxNjg2MTgyNDgxfQ.Y4ukHdEGAnljKSR7NfrSg7odRf57Gx7OI4220xi3-jE'
        wallet = '0xcedc4a31d05cf3a13f5807df5ddc89a61293dc59'
    else:
        auth = ''
        wallet = ''

    slots = get_slots(x, y, wallet, auth)
    
    headers = {
        'authority': 'api.plantvsundead.com',
        'accept': 'application/json',
        'accept-language': 'pt-BR,pt;q=0.5',
        'authorization': f'{auth}',
        'content-type': 'application/json;charset=UTF-8',
        'internal-api-key': 'key_for_testing_pvu_2023',
        'content-type': 'application/json;charset=UTF-8',
        'if-none-match': 'W/"11080-zDOqN+bsqw8Zw6Ml2dBYx1Oqifc"',
        'origin': 'https://marketplace.plantvsundead.com',
        'referer': 'https://marketplace.plantvsundead.com/',
        'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'x-u-a-check': 'Android-Unity-Farm',
    }

    params = {
        'x': f'{x}',
        'y': f'{y}',
    }

    response = requests.get('https://api.plantvsundead.com/lands/get-by-coordinate', params=params, headers=headers)
    data = response.json()

    for req in data["data"][0]["slots"]:
        if "_id" in req:
            id_planta = req["_id"]
            location = req["location"]


            if location in slots:

                if 'plantInfos' in req:
                    unique_id = req['plantInfos'].get('uniqueId')

                    headers = {
                        'authority': 'api.plantvsundead.com',
                        'accept': 'application/json, text/plain, */*',
                        'accept-language': 'pt-BR,pt;q=0.9',
                        'authorization': f'{auth}',
                        'origin': 'https://marketplace.plantvsundead.com',
                        'referer': 'https://marketplace.plantvsundead.com/',
                        'sec-ch-ua': '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-site',
                        'sec-gpc': '1',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                    }

                    params = {
                        'uniqueId': f'{unique_id}',
                    }

                    response3 = requests.get('https://api.plantvsundead.com/plants/detail', params=params, headers=headers)
                    data3 = response3.json()

                    
                    
                    try:
                        plant_url = data3['data']['plantConfig'].get('imageUrl')
                        
                    except:
                        pass

                current_time = int(time.time())
                harvest_time = req['harvestTime']

                # Converta o timestamp para um objeto datetime, especificando o fuso horário UTC
                harvest_datetime = datetime.datetime.fromtimestamp(harvest_time / 1000, pytz.utc)

                # Obtenha a data e hora atual com o fuso horário UTC
                current_datetime = datetime.datetime.fromtimestamp(current_time, pytz.utc)

                headers = {
                    'authority': 'api.plantvsundead.com',
                    'accept': 'application/json',
                    'accept-language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                    'authorization': f'{auth}',
                    'content-type': 'application/json;charset=UTF-8',
                    'internal-api-key': 'key_for_testing_pvu_2023',
                    'origin': 'https://marketplace.plantvsundead.com/',
                    'referer': 'https://marketplace.plantvsundead.com/',
                    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-site',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
                    'x-u-a-check': 'Android-Unity-Farm',
                }

                json_data = {
                    'slotIds': [
                        f'{id_planta}',
                    ],
                }

                response1 = requests.post('https://api.plantvsundead.com/farms/harvest-plant', headers=headers, json=json_data)
                if response1.status_code == 200:
                    resultados.append({
                        'status': True,
                        'descricao': 'Colheita com Sucesso!!',
                        'local': f'{location}',
                        'land': f'({x},{y})',
                        'url_plant': f'{plant_url}',
                    })
                else:
                    remaining_time = (harvest_datetime - current_datetime)

                    # Converta a diferença de tempo para um objeto de tempo
                    remaining_time = datetime.timedelta(seconds=remaining_time.total_seconds())

                    # Formate manualmente a diferença de tempo sem os milissegundos
                    hours, remainder = divmod(remaining_time.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    remaining_time_str = f"{hours}:{minutes}:{seconds}"
                    
                    resultados.append({
                        'status': False,
                        'descricao': 'Colheita sem Sucesso!!',
                        'local': f'{location}',
                        'land': f'({x},{y})',
                        'time': f'{remaining_time_str}',
                        'url_plant': f'{plant_url}',
                    })

    return resultados
     

@application.route(f'/api/colheita/<string:user>/<int:x>,<int:y>')
def colheita(user, x, y):
    resultados = verificar_colheita(user, x, y)
    return jsonify(resultados)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
