import requests
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import urllib.request
import json
from multiprocessing import Pool
import replace
from naver_keyword_search import function
import hashlib
import logging
logger = logging.getLogger(__name__)


def calculatestar(args):
    def calculate(func, args):
        result = func(*args)
        # print(len(result))
        return result
    return calculate(*args)

class Naver_api():

    def __init__(self, keyword: list, api_key: dict):
        self.id = api_key['client_id']
        self.secret = api_key['client_secret']
        self.content = keyword        
        self.acumulation = list(zip(self.id, self.secret))
        self.processes = 3
        self.tm = datetime.today() + relativedelta(months=-3)
        self.om = datetime.today() + relativedelta(months=-1)
        self.oy = datetime.today() + relativedelta(months=-12)
        self.now_time = datetime.today().strftime("%H%M%S")
        self.end = datetime.today().strftime("%Y-%m-%d")        
        self.url = "https://openapi.naver.com/v1/datalab/search";

    def ragged_chunks(self, seq, chunks):
        size = len(seq)
        start = 0
        for i in range(1, chunks + 1):
            stop = i * size // chunks            
            yield seq[start:stop]
            start = stop

    def manipulate(self):
        """
            1. first divide a number of chunks of keywords and stock_name 
                by 5 chunks
            2. make a list with api method and api_key dictionary
            3.                                 
        """        
        try:
            gr = [self.om.strftime("%Y-%m-%d"), self.tm.strftime("%Y-%m-%d"), self.oy.strftime("%Y-%m-%d")]
            task = [(self.get_signal,(gr[i], self.acumulation[i*2:i*2+2], i)) for i in range(3)]
            with Pool(self.processes) as pool:
                a = pool.map(calculatestar, task)                
                return a                        
        except Exception as err:
            logger.error(f'Error happend in manipulate {err}')   

    # def manipulate(self):
    #     a = self.get_signal(self.om.strftime("%Y-%m-%d"), self.acumulation[0:2], 1)
    #     return a

    def get_signal(self, start, key, ord):                
            collect = []
            i = 0            
            k = 0            
            for row in self.content:
                try:
                    body = "{\"startDate\":\"%s\",\"endDate\":\"%s\",\"timeUnit\":\"date\",\"keywordGroups\":[{\"groupName\":\"%s\",\"keywords\":[\"%s\"]}]}" % (
                    start,self.end,row['keyword'], row['keyword'])
                    body = body;
                    request = urllib.request.Request(self.url) 
                    request.add_header("X-Naver-Client-Id", key[k][0])
                    request.add_header("X-Naver-Client-Secret", key[k][1])
                    request.add_header("Content-Type", "application/json")
                    response = urllib.request.urlopen(request, data=body.encode("utf-8"))
                    response_body = response.read()
                    response_body = bytes.decode(response_body)
                    result = json.loads(response_body)
                    collect.append(result)                
                    # i += 1
                    # if i == 2:
                    #     break
                except urllib.error.URLError as err:
                    logger.info(f"key interruption: {err}")
                    k +=1
                    if k == 2:
                        break
                except Exception as err:
                    logger.info(f"error happened: {err}")
                    return None
            return collect

                     
            #         

            #     except urllib.error.URLError as err:
            #         logger.info(f"key interruption: {err}")
            #         i += 1
            #         if i == 2:
            #             return None
            #     except Exception as err:
            #         logger.info(f"error happened: {err}")
            #         return None