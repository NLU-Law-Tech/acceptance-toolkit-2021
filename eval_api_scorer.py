import requests
from glob import glob
import argparse
import os
import json
from loguru import logger
import urllib.parse
from collections import defaultdict
import copy
import time
from utils import save

parser = argparse.ArgumentParser()
parser.add_argument('-i','--in_dir',default='./out_data')
parser.add_argument('server')
args = parser.parse_args()
logger.debug(args)

class EvalApiScorer():
    def __init__(self,server,keys=['license_plate_number','account','phone_number']):
        self.keys = keys
        self._eval_api_endpoint = urllib.parse.urljoin(server,'/api/v2/evaluate/parse')
        logger.info(f"api_endpoint: {self._eval_api_endpoint}")
        self.score = defaultdict(lambda:{})
        self.len = 0

        # save response
        self.save_response_dir = f'./.api_res_log/{int(time.time())}'
        os.makedirs(self.save_response_dir,exist_ok=True)
    
    def _call(self,data,endpoint):
        r = requests.post(endpoint,data=json.dumps(data),headers={'Content-Type':'application/json'})
        return r.json()
    
    def eval(self,data,log_name=None):
        if log_name is None:
            log_name = str(self.len+1)+'.json'
        score = self._call(data,self._eval_api_endpoint)
        logger.info(json.dumps(score,ensure_ascii=False))
        save(score,os.path.join(self.save_response_dir,log_name))

        for key in self.keys:
            for metric in ['prec','recall','f1']:
                if metric not in self.score[key]:
                    self.score[key][metric] = 0.0
                self.score[key][metric] += score[key][metric]
        # step len
        self.len += 1
                
    def compute(self):
        final_score = copy.deepcopy(self.score)
        for k,v in final_score.items():
            for metric in ['prec','recall','f1']:
                final_score[k][metric] = final_score[k][metric]/self.len
        return final_score
        
        
if __name__ == '__main__':
    scorer = EvalApiScorer(server=args.server)
    files = glob(os.path.join(args.in_dir,"*.json"))
    for file in files:
        data = open(file,'r',encoding='utf-8').read()
        data = json.loads(data)
        scorer.eval(data,os.path.basename(file))
    logger.info(f"*** AVG score ***\n{json.dumps(scorer.compute())}")
        