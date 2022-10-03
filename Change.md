# Change logs

(Japanese)  
クリーンアップ用のスクリプトを作成しました。
このスクリプトは解析に必要のないルートボーンを削除し、`Hips`にルートを割り当てます。更に、いくつかのボーンの名前変更とミラーリングを実装しています。  
クリーンアップされたbvhファイルは`dataset/cleaned`に配置されます。

(English)  
I created CLEAN UP script.
The following script change the `ROOT` bone to the `Hips` and align the `ROOT` of the rest pose with the origin. The script also renames some bones and implements mirroring.  
Cleaned bvh files are stored in `dataset/cleaned`.

```bash
python utils/cleanup.py
```
