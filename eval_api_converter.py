#coding=utf-8
from glob import glob
from loguru import logger
import argparse
import os
import json
from utils import save, clean_breakline
from factory import createIndictment, createVerdict, createTransferdoc

# args
parser = argparse.ArgumentParser()
parser.add_argument('to_format',choices=['verdict','indictment','transferdoc'])
parser.add_argument('-i','--in_dir', default='./test_data')
parser.add_argument('-o','--out_dir',default='./out_data')
args = parser.parse_args()
logger.debug(args)

assert os.path.isdir(args.in_dir)
os.makedirs(args.out_dir,exist_ok=True)

if __name__ == '__main__':
    files = glob(os.path.join(args.in_dir,"*.json"))
    format_type = args.to_format
    for file in files:
        file_name = os.path.basename(file)
        logger.info(f"f_name: {file_name} f_path: {file}")
        data = open(file,'r',encoding='utf-8').read()
        data = json.loads(data)
        data = clean_breakline(data,ignore_keys=['unlabelDoc'])
        
        if format_type == 'verdict':
            processed_data = createVerdict(data)
        elif format_type == 'indictment':
            processed_data = createIndictment(data)
        elif format_type == 'transferdoc':
            processed_data = createTransferdoc(data)
        else:
            raise Exception('`format_type` error')
        
        processed_data = processed_data.dict()
        save(processed_data,os.path.join(args.out_dir,file_name))

