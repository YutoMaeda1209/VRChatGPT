# VRChatGPT
https://user-images.githubusercontent.com/55312129/226665675-8beedf4f-3a55-4de9-907c-a0bf76578802.mp4

## 概要
VRChatGPTは、VRChat上でChatGPTを搭載したキャラクターと会話することを目的に作成されたプログラムである。

## 必要ソフト
- Python3.10.9
- COEIROINK
- VRChat

## 利用方法
1. VRChatのアバターパラメータにint型の`Expressions`、`Status`を追加する。各値に設定するアニメーションは下記の表の通りにする。

| 値 | Expressions | Status |
| ---- | ----| ----|
| 0 | 通常 | 終了 |
| 1 | 喜ぶ | 聞き取り中 |
| 2 | 怒る | 処理中 |
| 3 | 泣く | 話し中 |
| 4 | 驚く | エラー |
2. [Releaseページ](https://github.com/Yuchi-Games/VRChatGPT/releases)からZipファイルをダウンロードして解凍する。
3. COEIROINKとVRChatを起動する。
4. Run.pyの46行目`os.environ["OPENAI_API_KEY"]`の部分をOpenAIのAPIKeyに書き換える
※環境変数を使うことをお勧めします。
5. Run.pyを実行する。
6. PythonとVRChatのマイクとスピーカーをVBCableなどで接続する。
