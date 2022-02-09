# convert_coco_to_voc
COCO形式のJSONファイルをPascal VOC形式のXMLファイルへ変換するスクリプト

# Requirement 
* tqdm 4.62.2 or later
* xmltodict 0.12.0 or later

# Usage
使用方法は以下です。
```bash
python convert_coco_to_voc.py json_filename xml_output_directory
```
* --set_name<br>
xmlファイル一覧テキストを出力名<br>
デフォルト：train
* --bbox_offset<br>
Pascal VOC形式のバウンディングボックスへ変換する際のオフセット<br>
デフォルト：1
* --folder<br>
\<folder\>タグに書き込む内容<br>
デフォルト：VOCCOCO
* --path<br>
\<path\>タグに書き込む内容<br>
デフォルト：指定なし
* --owner<br>
\<owner\>タグに書き込む内容<br>
デフォルト：Unknown
* --source_database<br>
\<database\>タグに書き込む内容<br>
デフォルト：Unknown
* --source_annotation<br>
\<annotation\>タグに書き込む内容<br>
デフォルト：Unknown
* --source_image<br>
\<image\>タグに書き込む内容<br>
デフォルト：Unknown
* --image_depth<br>
\<depth\>タグに書き込む内容<br>
デフォルト：3
* --segmented<br>
\<segmented\>タグに書き込む内容<br>
デフォルト：0

# Author
高橋かずひと(https://twitter.com/KzhtTkhs)
 
# License 
convert_coco_to_voc is under [Apache-2.0 License](LICENSE).
