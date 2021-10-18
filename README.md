# Acceptance Toolkit 2021
## 標註程式
[標註工具使指南](https://hackmd.io/0nrrMc5NQRKxlZZVkwmD7w)

[2021 ITRI LAW-TAGGER Local Version](https://github.com/NLU-Law-Tech/2021_VerdictTagger/tree/local-mode#下載) 

## 合併與後處理
```sh
usage: eval_api_converter.py [-h] [-i IN_DIR] [-o OUT_DIR] {verdict,indictment}

positional arguments:
  {verdict,indictment}

optional arguments:
  -h, --help            show this help message and exit
  -i IN_DIR, --in_dir IN_DIR
  -o OUT_DIR, --out_dir OUT_DIR
```
### 標註資料轉**判決書**輸入
```sh
python eval_api_converter.py -i='test_data' verdict
```
### 標註資料轉**起訴書**輸入
```sh
python eval_api_converter.py -i='test_data' indictment
```
## 辨識率分數計算
```
usage: eval_api_scorer.py [-h] [-i IN_DIR] [-s SERVER]

optional arguments:
  -h, --help            show this help message and exit
  -i IN_DIR, --in_dir IN_DIR
  -s SERVER, --server SERVER
```
### 呼叫API與算分
```sh
python eval_api_scorer.py -s http://140.120.13.250:16005
```
### 指標平均分數
```json
{'license_plate_number': {'prec': 0.3333333333333333, 'recall': 0.3333333333333333, 'f1': 0.3333333333333333}, 'account': {'prec': 0.0, 'recall': 0.0, 'f1': 0.0}, 'phone_number': {'prec': 0.0, 'recall': 0.0, 'f1': 0.0}})
```