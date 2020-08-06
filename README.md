# ダウンロード
[こちら](https://drive.google.com/file/d/18eKgunHv56oxsGmuoi_uf5NXYSkFSbnE/view?usp=sharing)のリンクからダウンロードします。容量が83MBあってgithubにアップロードできませんでした。

# このプログラムについて
.psdファイルのレイヤーの名前の先頭に「!」や「*」を一括でつけるプログラムです。

# 使い方
ダウンロードした.exeを実行すると以下のようなウィンドウが表示されます。ちなみに立ち上がるまで少々時間を要します。   
編集したい.psdファイルを開いて適用したい項目を選んで変換すると右側の空間に変換後のレイヤー構造が表示されます。   
必要な変換が終わったら上書き保存、あるいは別名で保存します。   

![cap](https://user-images.githubusercontent.com/48207892/89515942-bff90380-d812-11ea-9c43-262f5741b8af.PNG)

## 変換メニューについて
大体文章に書いてあるそのままの変換を行います。   
例えば1つ目のメニューは指定した条件に合うレイヤーやグループをフィルタリングして名前の先頭に「!」や[*」を加えます。このとき、名前の先頭が「!」か「*」のレイヤーやグループは変換されません。   
フィルタリング条件は5つを指定することができます。
- 層：レイヤーの階層を指していて、最上位階層を「1層」として定義しています。例えば、どのグループにも属さいないレイヤーは1層、どのグループにも属さないグループに属するレイヤーは2層です。そして0層は特定位の階層ではなく「全ての層」を指定します
- レイヤーやグループの名前に含まれる言葉
- 一致条件：「含む」か「一致する」を選ぶことができます。どちらも融通が効かないので、ローマ字の大文字と小文字、全角半角、ひらがなとカタカナも全て違う言葉として扱い、「一言一句違わず含まれる・一致する」名前だけをフィルタリングします。例えば、「ああついでに氷をいれてくれ」というレイヤーがあったとして「アツイ」を含んでいるとはみなしません。
- 検索対象の種類：検索対象がレイヤーかそれともグループかを指定します。ここで「物」を選んだ場合両方とも変換します。「グループの直下の物」の場合、指定する条件に合致するグループを探し、その直下にあるレイヤーとグループを全て変換します
- 頭につける記号：「!」か「*」

2つめ、3つ目の変換メニューはどちらも1つ目のメニューでできる変換ですが、おそらく使用頻度が高いだろうと思い単一のメニューで作成しました。   
4つ目のメニューは全てのレイヤー、グループの名前の先頭の「!」、「*」を取り除きます。

## ショートカットキー
プログラムに記載している通りのショートカットキーが使えます。

# フィードバックについて
ツイッター( https://twitter.com/662611034 )の方でも受け付けます。

# プログラムの中身について
## 構成
以下の3つのファイルで構成されています。
- handler.py：psdを読み込んだりレイヤー名を変えたりするクラスを定義しています。Python標準ライブラリのreと、pipからインストールしたpsd_toolsを用いています。
- gui.py：GUIの見た目の部分と、選択した項目の情報を出力するクラスを定義しています。Python標準ライブラリのtkinterを用いました。
- __main__.py：上記のhandler.pyとgui.pyをまとめて新しいメソッドを定義したりボタンに関数をバインドしたりしています。ウェブページを開くためにPython標準ライブラリのwebbrowserを用いています。
Windows以外の環境の方はこれらのファイルと必要なパッケージをダウンロードしてご利用いただくこともできます。Windows以外の環境でこのプログラムが必要な場合があるかは甚だ疑問ですが。

## ビルド
pyinstallerを用いて64bit Windows 10でビルドしました。
