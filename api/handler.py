from http.server import BaseHTTPRequestHandler
import json
import time
import sys
from pymongo import MongoClient
sys.path.insert(0, 'src/vendor')
import requests

class Vinyl:
    def __init__(self, title, price, url, image):
        self.title = title
        self.price = price
        self.url = url
        self.image = image

    def printDetails(self):
       print(f'title: {self.title}')
       print(f'price: {self.price}')
       print(f'url:   {self.url}')
       print(f'url:   {self.image}')

    def vinyltoDict(self):
        return {
            'title': self.title,
            'price': self.price,
            'url': self.url,
            'image': self.image
        }

def hello():
    
    # curl "https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&channel=WEB&count=24&default_purchasability_filter=true&include_sponsored=true&keyword=vinyl+records&offset=0&page=^%^2Fs^%^2Fvinyl+records&platform=mobile&pricing_store_id=83&sort_by=Featured&store_ids=83^%^2C2190^%^2C770&useragent=Mozilla^%^2F5.0+^%^28Linux^%^3B+Android+6.0^%^3B+Nexus+5+Build^%^2FMRA58N^%^29+AppleWebKit^%^2F537.36+^%^28KHTML^%^2C+like+Gecko^%^29+Chrome^%^2F110.0.0.0+Mobile+Safari^%^2F537.36&visitor_id=0186612F72AD020192513D4B25087EDC&zip=79364" ^
    #   -H "authority: redsky.target.com" ^
    #   -H "accept: application/json" ^
    #   -H "accept-language: en-US,en;q=0.9" ^
    #   -H "cookie: TealeafAkaSid=mh7cYCXaQAo5_tQqQAzb89Hydi38el3Q; visitorId=0186612F72AD020192513D4B25087EDC; sapphire=1; UserLocation=79364^|33.440^|-101.650^|TX^|US; accessToken=eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIwMWU1NjFhZi1hNThjLTRkYWItODdjMS04YTkwMDIxMGZjY2YiLCJpc3MiOiJNSTYiLCJleHAiOjE2NzY3NTQxNDksImlhdCI6MTY3NjY2Nzc0OSwianRpIjoiVEdULmNhNWMyNGUzOWQ2NjRkYTg5NzEyOWIwODM3ZjM3NzYwLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImM0Njg3NzIwMDY4ZmVmODBiNjZjZDk0NDIzZTEzZTA4NTk2N2JkYzUxOTI1NmQ2OGM4MTk3OGRhNzUzNDcwMTMiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.lgs9eGS3vEX_YMc-I_EsJbgjk1dPcHHViOA-hLzNaAXAuA41kKWBMxPVPp34WFljVksL5t8KCQUMR5sefrTRkIpAdXmGtfMfucU86cV2d-MZD8q7vCx17XgE5MqJOGpO4UjzyL3nx8TZJp-awVQzRYwxOUKX2lrmU8SUIb7ONjBfUNyPxBsd1K9wwd3c8jrC7OT7_U8XerRCNKiM6EuvIk1nzemnIW_QIdHt4V7KkC2IH_1K3ITMmWbTsBmVWku8NTvD57IPqfOHULhI8RD3SyiaumB9qUb0SKMkqUbpMBuIUaHSu8X7qveD1PtO-jZMWUWCmjqGjmx8k4csRpNGQg; idToken=eyJhbGciOiJub25lIn0.eyJzdWIiOiIwMWU1NjFhZi1hNThjLTRkYWItODdjMS04YTkwMDIxMGZjY2YiLCJpc3MiOiJNSTYiLCJleHAiOjE2NzY3NTQxNDksImlhdCI6MTY3NjY2Nzc0OSwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlfX0.; refreshToken=ax40mMv4Zfnb7IzNUCsynjH2V1sLMTmj1HxaOtqG9nKK3ExX_b5F4n8zELmMPm-VGTBV6d33Vat6en-KRBYOSg; fiatsCookie=DSI_83^|DSN_Lubbock^%^20University^%^20Ave^|DSZ_79423; ci_pixmgr=other; _gcl_au=1.1.538189206.1676667753; _ga=GA1.2.1619494967.1676668624; _gid=GA1.2.1291468420.1676668624; __gads=ID=745146e152674252:T=1676750262:S=ALNI_MazrU5IZnHEVSWlbvC_m-K10KC25g; __gpi=UID=0000094a135050e5:T=1676750262:RT=1676750262:S=ALNI_MZWX-O5SR8Z59c8VgHNHpd6TJ2geQ; _mitata=ZDg2Y2RlOTA0ZmJhYWNiY2U1NTdmNzhmNzM0OTIxNzYyMmMyYjVmODFjOTJiMjkyNGIyNGE2NTgxZjlhNDA5Zg==_/^@^#/1676750424_/^@^#/ctnXdTClgORooqSD_/^@^#/MzkxYmJlNDJkNzA5OTc3NGFiOGYwMWFhYTUxNjY2YTIxM2Y1NjE1OTk5ZjBiMzRhYTU3MzA5MWI0Mjg0OWRjNw==_/^@^#/000; ffsession=^{^%^22sessionHash^%^22:^%^229316a55e22a721676667747678^%^22^%^2C^%^22prevPageName^%^22:^%^22search:^%^20search^%^20results^%^22^%^2C^%^22prevPageType^%^22:^%^22search:^%^20search^%^20results^%^22^%^2C^%^22prevPageUrl^%^22:^%^22https://www.target.com/s?searchTerm=vinyl+records&tref=typeahead^%^257Cterm^%^257C0^%^257Cvinyl+records^%^257Cvinyl+records^%^257C^%^257C^%^257Cservice^%^257C10^%^257C^%^257C^%^257C&category=0^%^257CAll^%^257Cmatchallpartial^%^257Call+categories&searchTermRaw=&sortBy=Featured&moveTo=product-list-grid^%^22^%^2C^%^22prevSearchTerm^%^22:^%^22vinyl^%^20records^%^22^%^2C^%^22sessionHit^%^22:23^}; _uetsid=65a1dad0af0611ed8f463541a41dd873; _uetvid=65a1f630af0611edafaeeb821e37aa76" ^
    #   -H "origin: https://www.target.com" ^
    #   -H "referer: https://www.target.com/s?searchTerm=vinyl+records&tref=typeahead^%^7Cterm^%^7C0^%^7Cvinyl+records^%^7Cvinyl+records^%^7C^%^7C^%^7Cservice^%^7C10^%^7C^%^7C^%^7C&category=0^%^7CAll^%^7Cmatchallpartial^%^7Call+categories&searchTermRaw=&sortBy=Featured&moveTo=product-list-grid" ^
    #   -H "sec-ch-ua: ^\^"Chromium^\^";v=^\^"110^\^", ^\^"Not A(Brand^\^";v=^\^"24^\^", ^\^"Google Chrome^\^";v=^\^"110^\^"" ^
    #   -H "sec-ch-ua-mobile: ?1" ^
    #   -H "sec-ch-ua-platform: ^\^"Android^\^"" ^
    #   -H "sec-fetch-dest: empty" ^
    #   -H "sec-fetch-mode: cors" ^
    #   -H "sec-fetch-site: same-site" ^
    #   -H "user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36" ^
    #   --compressed
    
    #DO NOT INCLUDE COOKIES IN REQUESTS

  def getDB():
    CONNECTION_STRING = "mongodb+srv://Pacforever:Pacforever@cluster0.xfgz9lp.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    return client.get_database('webscrapingDb')

  getDB()
  
  vinylArr = []
  db = getDB()
  targetTable = db['target']

  headers = {
  'authority': 'redsky.target.com',
  'accept': 'application/json',
  'accept-language': 'en-US,en;q=0.9',
  # 'cookie': 'TealeafAkaSid=mh7cYCXaQAo5_tQqQAzb89Hydi38el3Q; visitorId=0186612F72AD020192513D4B25087EDC; sapphire=1; UserLocation=79364|33.440|-101.650|TX|US; fiatsCookie=DSI_83|DSN_Lubbock%20University%20Ave|DSZ_79423; ci_pixmgr=other; _gcl_au=1.1.538189206.1676667753; _ga=GA1.2.1619494967.1676668624; __gads=ID=745146e152674252:T=1676750262:S=ALNI_MazrU5IZnHEVSWlbvC_m-K10KC25g; __gpi=UID=0000094a135050e5:T=1676750262:RT=1676750262:S=ALNI_MZWX-O5SR8Z59c8VgHNHpd6TJ2geQ; egsSessionId=c009b679-5875-4e1d-a5e3-8ad304cc6a05; accessToken=eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJkNjkzYmIwOC01ODM1LTQ0ZWUtYmQ4Mi02YWNhOGI2OTQxYWUiLCJpc3MiOiJNSTYiLCJleHAiOjE2NzcxODY1MjQsImlhdCI6MTY3NzEwMDEyNCwianRpIjoiVEdULmQyZjg1YzhkNTg1MzRkY2U5Y2I2ZGJhOWE3NmMyODQ3LWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImM0Njg3NzIwMDY4ZmVmODBiNjZjZDk0NDIzZTEzZTA4NTk2N2JkYzUxOTI1NmQ2OGM4MTk3OGRhNzUzNDcwMTMiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.Y5YxIkrAahlfjo35HvMRKVxGtjxXU1hAVLjMpK-90Yw_v8REpgrIZwCJLDtlVupo9f1jODgaEI3TwyfF225T6XGP7oXmkKCDxabSjpHOlUJRVJvmxyC9wBxBn-UiB7vdFoqQvL7gH2LDyTJf7scxHz6pVKgoYJx5PsSnWNs8QUosdGeo0APPCDHLtQ9_P4RiWAf5nzWh5zn8j-42gYNcu6xhNXLoCf7B8DIl2sJgIZRZZeWC7iQRs8lmYdTr_RfIq61PcFsKNHUhOP2qHLk3MS9dR4c6v9RzFxsuIW7tZJCKDzKUQOok5PboVZJjwnu8nsaa50q_aWnL1Lm8MVyMXA; idToken=eyJhbGciOiJub25lIn0.eyJzdWIiOiJkNjkzYmIwOC01ODM1LTQ0ZWUtYmQ4Mi02YWNhOGI2OTQxYWUiLCJpc3MiOiJNSTYiLCJleHAiOjE2NzcxODY1MjQsImlhdCI6MTY3NzEwMDEyNCwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlfX0.; refreshToken=Ze0PHhUWj4n8pcIbyyt2DqvfY87O19Z1iRhXSebX0RwKzhV3JbIz-maV0gZiqsLT9eXSjRzzUJGZRONkvxC2nQ; _mitata=ODYwYjYwNzZkZTZiNTY0ZTQyYTg0OTY0YWE3NTc5NGI0MTY0NzJlYzRiNTJlNTYxYzg5OGYyNmIwNGQyYmMyZA==_/@#/1677100978_/@#/cGqFYYsjtKjuMfw1_/@#/ODA3OTY0MjlmNWNjYmM0OTUyZWZlZDc1ZjlkMDM1NjJmM2EzN2I0NDhlNGIwMjAxOTJiYjRiMmE3ZWQyMjcxMA==_/@#/000; ffsession={%22sessionHash%22:%221b68891ee8245d1677100119669%22%2C%22prevPageName%22:%22search:%20search%20results%22%2C%22prevPageType%22:%22search:%20search%20results%22%2C%22prevPageUrl%22:%22https://www.target.com/s?searchTerm=target+vinyl%22%2C%22prevSearchTerm%22:%22target%20vinyl%22%2C%22sessionHit%22:7}; _uetsid=1ac98240b2f511ed8b7cf3ade0088b26; _uetvid=1ac9b4a0b2f511ed8c31bfb24e459528',
  'origin': 'https://www.target.com',
  'referer': 'https://www.target.com/s?searchTerm=target+vinyl',
  'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
  'sec-ch-ua-mobile': '?1',
  'sec-ch-ua-platform': '"Android"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
  }
  
  def requestTarget(offset=0):
    response = requests.get(
    'https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2',
    params = {
      'key': '9f36aeafbe60771e321a7cc95a78140772ab3e96',
      'channel': 'WEB',
      'count': '24',
      'default_purchasability_filter': 'true',
      'include_sponsored': 'true',
      'keyword': 'vinyl',
      'offset': f'{offset}',
      'page': '/s/target vinyl',
      'platform': 'mobile',
      'pricing_store_id': '83',
      'store_ids': '83,2190,770',
      'useragent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
      'visitor_id': '0186612F72AD020192513D4B25087EDC',
      'zip': '79364',
  },
    headers=headers,
    )
    formatAsJson(response, offset)
  
  def formatAsJson(response, offset):
    json_formatted_str = json.loads(response.text)
  
    turnJSONintoReadable(json_formatted_str, offset)
  
  
  def turnJSONintoReadable(json_formatted_str, offset):
    products = json_formatted_str['data']['search']['products']
    initializeVinyl(products)
    offset+=24
    time.sleep(5)
    try:
      requestTarget(offset)
    except:
      targetTable.delete_many({})
      targetTable.insert_many(vinylArr)
      print('done')

  def initializeVinyl(products):
      for product in products:
        print(json.dumps(product, indent=4))
        price = product['price']['formatted_current_price']
        title = product['item']['product_description']['title']
        url = product['item']['enrichment']['buy_url']
        image = product['item']['enrichment']['images']['primary_image_url']
        vinyl = Vinyl(title, price, url, image)
        vinylDict = vinyl.vinyltoDict()
        print(vinylDict)
        vinylArr.append(vinylDict)  
        
      
  requestTarget()

hello()
