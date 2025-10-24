# YOLO物体検出アプリ

Raspberry PiでYOLOv8を使ったリアルタイム物体検出を体験できる初心者向けアプリケーションです。

## 📖 概要

このアプリケーションは、Raspberry Piカメラモジュールv3またはUSBカメラからの映像をリアルタイムで取得し、YOLOv8モデルを用いて物体検出を行い、検出結果をバウンディングボックス付きで画面に表示します。

**書籍掲載**: 本プロジェクトは書籍「機械学習モデルYOLOって何？準備と設定」(chapter10-1)に掲載されているサンプルプログラムです。

## ✨ 特徴

- 🎯 **シンプルな設計**: 初心者でも理解しやすい単一ファイル構成
- ⚡ **リアルタイム検出**: カメラ映像から瞬時に物体を検出
- 🎛️ **簡単な設定**: コマンドライン引数で柔軟に設定可能
- 📊 **FPS表示**: リアルタイムでパフォーマンスを確認
- 🛡️ **エラーハンドリング**: 初心者にも分かりやすいエラーメッセージ

## 🔧 必要なハードウェア

- **Raspberry Pi 4 Model B (4GB以上推奨)** または **Raspberry Pi 5**
- **Raspberry Pi カメラモジュール v3** または **USB カメラ**
- **microSDカード**: 32GB以上（Class 10以上推奨）
- **HDMIモニター** または **LCD モジュール**
- **電源アダプタ**: 公式5V/3A電源推奨

## 💻 ソフトウェア要件

- **OS**: Raspberry Pi OS (64bit版推奨、Debian 12 'Bookworm'ベース)
- **Python**: 3.9以上

## 📦 インストール手順

### 1. システムのアップデート

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. 必要なシステムライブラリのインストール

```bash
sudo apt install python3-pip python3-venv git cmake build-essential -y
```

### 3. プロジェクトのクローン

```bash
git clone https://github.com/Murasan201/10-001-yolov8-object-detection.git
cd 10-001-yolov8-object-detection
```

### 4. Python仮想環境の作成とアクティベート

```bash
python3 -m venv yolo_env
source yolo_env/bin/activate
```

仮想環境がアクティベートされると、プロンプトの先頭に `(yolo_env)` と表示されます。

### 5. 必要なPythonライブラリのインストール

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**注意**: PyTorchとYOLOv8のインストールには10〜20分程度かかる場合があります。

### 6. インストール確認

```bash
python -c "from ultralytics import YOLO; print('YOLOv8のインストールが成功しました')"
```

## 🚀 使い方

### 基本的な使用方法

カメラデバイス0番を使用してデフォルト設定で実行:

```bash
python detect.py
```

### コマンドライン引数

| 引数 | 説明 | デフォルト値 | 例 |
|------|------|--------------|-----|
| `--model` | YOLOモデルファイルのパス | `yolov8n.pt` | `--model yolov8s.pt` |
| `--source` | カメラ番号またはビデオファイルパス | `0` | `--source 1` または `--source video.mp4` |
| `--conf` | 検出の信頼度閾値 (0.0〜1.0) | `0.25` | `--conf 0.5` |
| `--duration` | 実行時間（秒） | なし（手動終了） | `--duration 60` |

### 使用例

#### 例1: デフォルト設定で実行

```bash
python detect.py
```

#### 例2: 信頼度閾値を高めに設定

```bash
python detect.py --conf 0.5
```

確信度50%以上の検出結果のみを表示します。

#### 例3: ビデオファイルから物体検出

```bash
python detect.py --source sample_video.mp4
```

#### 例4: 60秒間だけ実行

```bash
python detect.py --duration 60
```

60秒後に自動的に終了します。

#### 例5: USBカメラ（デバイス番号1）を使用

```bash
python detect.py --source 1
```

### 終了方法

- キーボードの **`q`** キーを押す
- **`Ctrl+C`** を押す
- `--duration` オプションで指定した時間が経過するまで待つ

## 📁 プロジェクト構造

```
10-001-yolov8-object-detection/
├── CLAUDE.md                          # 開発ルール
├── LICENSE                            # ライセンス情報
├── README.md                          # このファイル
├── requirements.txt                   # Python依存パッケージ
├── detect.py                          # メインスクリプト
├── 10-001_YOLO物体検出アプリ_要件定義書.md
└── models/                            # YOLOモデル格納ディレクトリ（作成推奨）
    └── yolov8n.pt                     # 初回実行時に自動ダウンロード
```

## 🎓 YOLOv8モデルについて

YOLOv8には、精度と速度のトレードオフに応じた複数のモデルサイズが用意されています:

| モデル | サイズ | 速度 | 精度 | Raspberry Piでの推奨 |
|--------|--------|------|------|----------------------|
| `yolov8n.pt` | Nano | 最速 | 低 | ✅ 推奨 |
| `yolov8s.pt` | Small | 速い | 中 | ⚠️ 可能だが遅い |
| `yolov8m.pt` | Medium | 普通 | 高 | ❌ 非推奨 |
| `yolov8l.pt` | Large | 遅い | 高 | ❌ 非推奨 |
| `yolov8x.pt` | XLarge | 最遅 | 最高 | ❌ 非推奨 |

**Raspberry Pi 4/5では `yolov8n.pt`（Nano）の使用を強く推奨します。**

初回実行時に指定したモデルが自動的にダウンロードされます。

## 🔍 検出可能な物体

YOLOv8の事前訓練モデルは、COCOデータセットの80クラスの物体を検出できます:

- **人間**: person
- **乗り物**: bicycle, car, motorcycle, airplane, bus, train, truck, boat
- **動物**: bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe
- **家具**: chair, couch, bed, dining table
- **電子機器**: tv, laptop, mouse, keyboard, cell phone
- その他多数...

## ⚙️ パフォーマンスチューニング

### GPUメモリの割り当て

```bash
sudo raspi-config
```

「7 Advanced Options」→「A3 Memory Split」で128MBまたは256MBに設定後、再起動。

### 解像度の調整

カメラの解像度を下げることでFPSを向上できます。`detect.py`に以下を追加:

```python
# initialize_camera関数内に追加
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

## 🐛 トラブルシューティング

### カメラが認識されない

**問題**: `エラー: カメラまたはビデオファイルを開けませんでした`

**解決方法**:
1. カメラが正しく接続されているか確認
2. Raspberry Piカメラの場合、カメラインターフェースを有効化:
   ```bash
   sudo raspi-config
   # Interface Options → Camera → Enable
   sudo reboot
   ```
3. 別のデバイス番号を試す: `--source 1` または `--source 2`

### メモリ不足エラー

**問題**: `Out of memory` エラー

**解決方法**:
1. 他のアプリケーションを終了
2. より小さいモデル(`yolov8n.pt`)を使用
3. スワップ領域を増やす

### FPSが低い

**問題**: 処理速度が遅い（1 FPS以下）

**解決方法**:
1. `yolov8n.pt`（Nano）モデルを使用
2. カメラ解像度を下げる
3. 信頼度閾値を上げる（`--conf 0.5`など）

### モデルのダウンロードが失敗する

**問題**: インターネット接続の問題でモデルがダウンロードできない

**解決方法**:
1. インターネット接続を確認
2. 手動でダウンロード:
   ```bash
   wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
   ```

## 📚 参考資料

- [YOLOv8公式ドキュメント](https://docs.ultralytics.com/)
- [OpenCV-Python チュートリアル](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Raspberry Pi カメラ設定ガイド](https://www.raspberrypi.com/documentation/accessories/camera.html)

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 🤝 貢献

バグ報告、機能リクエスト、プルリクエストを歓迎します。

## 📧 サポート

質問や問題がある場合は、GitHubのIssuesページで報告してください。

---

**初心者の皆さんへ**: このプロジェクトは学習目的で作成されています。コードを読んで、動かして、改造して、楽しみながらAI技術を学んでください！
