# foreign_tax
SBI証券の「外国株式等配当金」の確定申告に使えるスクリプトです. 
Python3系で動きます。  
NISAには対応していません(2021/4月から現在の分まで使えます). 

# インストール
pip install pdfminer.six

# 使い方
「外国株式等配当金」でSBI証券の電子ポストを検索して、すべての外国配当金のPDFを一つのフォルダに集めます。  
スクリプト内のDIRのパスを変更します。  

# 実行方法
python pdf_data.py

#出力結果
出力された以下の結果を
```
---------確定申告に記載する値-------------
配当金等金額->50.33$
外国源泉徴収額->4.98$
配当金等金額YEN->5534円
外国源泉徴収額YEN->543円

```

ご利用は自己責任でお願いします
