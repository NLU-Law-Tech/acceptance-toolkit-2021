from typing import List
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

class CsvWirter():
    def __init__(self,save_path):
        logger.opt(colors=True).info(f"<red>save csv to: {save_path}</red>")
        self.csv_writer = open(save_path,'a',encoding='utf-8')
    
    def _to_csv_row(self,line:list):
        line = [str(l).replace(",","") for l in line]
        line = ','.join(line)
        logger.opt(colors=True).info(f"<blue>{line.split(',')}</blue>")
        return line
        
    def setHeader(self,header:list):
        self.csv_header = header
        self.write(header)

    def write(self,line:list):
        line = self._to_csv_row(line)
        self.csv_writer.write(f"{line}\n")

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

        self.eval_idv_writer = CsvWirter(os.path.join(self.save_response_dir,'eval_idv.csv'))
        self.eval_idv_writer.setHeader(['file','name']+self.keys)
    
    def _call(self,data,endpoint):
        r = requests.post(endpoint,data=json.dumps(data),headers={'Content-Type':'application/json'})
        return r.json()
    
    def eval_idv(self,score,log_name):
        self.idv_score = defaultdict(lambda:{})
        for key in self.keys:
            for p_score in score[key]['_details']:
                name = p_score['name']
                for metric in ['prec','recall','f1']:
                    if key not in self.idv_score[name]:
                        self.idv_score[name][key] = {}
                    if metric not in self.idv_score[name][key]:
                        self.idv_score[name][key][metric] = {}
                    self.idv_score[name][key][metric] = p_score[metric]

        for k,v in self.idv_score.items():
            name = k
            object_f1_scores = []
            for object in self.keys:
                object_f1_score = str(v[object]['f1'])
                object_f1_scores.append(object_f1_score)
            self.eval_idv_writer.write([log_name,name]+object_f1_scores)            
                    
    def eval(self,data,log_name=None):
        if log_name is None:
            log_name = str(self.len+1)+'.json'
        score = self._call(data,self._eval_api_endpoint)
        save(score,os.path.join(self.save_response_dir,log_name))

        self.eval_idv(score,log_name)
        # logger.info(json.dumps(score,ensure_ascii=False))

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
        