import requests
import time

class QueryAPI:
    def __init__(self, gis, api):
        self.gis = gis
        self.token = gis._con.token
        self.api = api

    def __api_get_request(api_url, token, query):
        api_url += f"/query?f=json&token={token}&where={query}&outFields=*"
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                return response.json()
            else:
                raise ValueError(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            return f"Exception occurred: {e}"
        
    def make_query_mmsi(self, mmsi, tmsp_min, tmsp_max):
        query = f"MMSI = '{mmsi}' AND msgTime > TIMESTAMP '{tmsp_min}' AND msgTime < TIMESTAMP '{tmsp_max}'"
        return self.__api_get_request(self, query)['features']

    def make_query_with_retries_mmsi(self, mmsi, tmsp_min, tmsp_max, max_retries=5, time_wait=1):
        result = None
        retries = 0
        
        while result is None and retries < max_retries:
            try:
                try_result = self.make_query_mmsi(mmsi, tmsp_min, tmsp_max)
                result = try_result
            except Exception as e:
                print(e)
                time.sleep(time_wait)
                retries += 1
                
        return result

    def make_query(self, tmsp_min, tmsp_max, query_position):
        query = f"msgTime > TIMESTAMP '{tmsp_min}' AND msgTime < TIMESTAMP '{tmsp_max}' AND {query_position}"
        return self.__api_get_request(query)['features']

    def make_query_with_retries(self, tmsp_min, tmsp_max, query_position, max_retries=5, time_wait=1):
        result = None
        retries = 0
        
        while result is None and retries < max_retries:
            try:
                try_result = self.make_query(tmsp_min, tmsp_max, query_position)
                result = try_result
            except Exception as e:
                print(e)
                time.sleep(time_wait)
                retries += 1
                
        return result
    
    def custom_query(self, query):
        return self.__api_get_request(query)['features']