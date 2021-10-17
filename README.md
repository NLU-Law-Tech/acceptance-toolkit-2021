# Acceptance Toolkit 2021
## 標註程式
[標註工具使指南](https://hackmd.io/0nrrMc5NQRKxlZZVkwmD7w)

[2021 ITRI LAW-TAGGER Local Version](https://github.com/NLU-Law-Tech/2021_VerdictTagger/tree/local-mode#下載) 

## 合併與後處理
```sh
usage: eva_api_converter.py [-h] [-in_dir IN_DIR] [-out_dir OUT_DIR]
                            {verdict,indictment}

positional arguments:
  {verdict,indictment}

optional arguments:
  -h, --help            show this help message and exit
  -in_dir IN_DIR
  -out_dir OUT_DIR
```
### 標註資料轉**判決書**輸入
```sh
python eva_api_converter.py -in_dir='test_data' verdict
```
### 標註資料轉**起訴書**輸入
```sh
python eva_api_converter.py -in_dir='test_data' indictment
```
## 辨識率分數計算
...