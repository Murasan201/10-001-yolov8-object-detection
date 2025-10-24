# セットアップガイド

このドキュメントでは、YOLO物体検出アプリの詳細なセットアップ手順を説明します。

## Raspberry Piの初期設定

### 1. Raspberry Pi OSのインストール

1. **Raspberry Pi Imager**をダウンロード
   - https://www.raspberrypi.com/software/

2. **OSを選択**
   - "Raspberry Pi OS (64-bit)" を選択
   - Debian 12 'Bookworm'ベースを推奨

3. **microSDカードに書き込み**
   - 32GB以上のmicroSDカード（Class 10以上）を使用
   - 書き込みには5〜10分程度かかります

4. **初回起動設定**
   - 言語、タイムゾーン、WiFi設定を行う
   - ユーザー名とパスワードを設定

### 2. システムの更新

```bash
# パッケージリストを更新
sudo apt update

# インストール済みパッケージをアップグレード
sudo apt upgrade -y

# 再起動（推奨）
sudo reboot
```

### 3. カメラの有効化

Raspberry Piカメラモジュールを使用する場合:

```bash
# 設定ツールを起動
sudo raspi-config

# 以下の順で選択:
# 3 Interface Options
# → I1 Camera
# → Yes で有効化
# → Finish

# 再起動
sudo reboot
```

### 4. カメラの動作確認

```bash
# 静止画撮影テスト
libcamera-still -o test.jpg

# プレビュー表示テスト（5秒間）
libcamera-hello -t 5000
```

## Python環境のセットアップ

### 1. 必要なシステムツールのインストール

```bash
sudo apt install -y \
    python3-pip \
    python3-venv \
    git \
    cmake \
    build-essential \
    libopencv-dev \
    python3-opencv
```

### 2. プロジェクトのダウンロード

GitHubからプロジェクトをクローン:

```bash
cd ~
git clone https://github.com/Murasan201/10-001-yolov8-object-detection.git
cd 10-001-yolov8-object-detection
```

### 3. Python仮想環境の作成

```bash
# 仮想環境を作成
python3 -m venv yolo_env

# 仮想環境をアクティベート
source yolo_env/bin/activate

# アクティベートされると、プロンプトに (yolo_env) が表示されます
# 例: (yolo_env) pi@raspberrypi:~/10-001-yolov8-object-detection $
```

### 4. Pythonパッケージのインストール

```bash
# pipを最新版にアップグレード
pip install --upgrade pip

# 必要なパッケージをインストール（10〜20分かかる場合があります）
pip install -r requirements.txt
```

**インストール中の注意事項**:
- PyTorchのビルドには時間がかかります（10〜15分程度）
- メモリ使用量が増えるため、他のアプリケーションは終了しておくことを推奨
- エラーが発生した場合は、再度実行してみてください

### 5. インストールの確認

```bash
# PyTorchの確認
python -c "import torch; print(f'PyTorch version: {torch.__version__}')"

# OpenCVの確認
python -c "import cv2; print(f'OpenCV version: {cv2.__version__}')"

# YOLOv8の確認
python -c "from ultralytics import YOLO; print('YOLOv8 import successful')"
```

すべてのコマンドがエラーなく実行されれば、インストールは成功です。

## YOLOモデルの準備

### 初回実行時の自動ダウンロード

最初に`detect.py`を実行すると、YOLOv8nanoモデル（約6MB）が自動的にダウンロードされます。

```bash
python detect.py
```

### 手動ダウンロード（オプション）

インターネット接続が不安定な場合、事前にモデルをダウンロードできます:

```bash
# modelsディレクトリに移動
cd models

# YOLOv8 nanoモデルをダウンロード
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt

# プロジェクトルートに戻る
cd ..
```

## パフォーマンス最適化

### 1. GPUメモリの割り当て

```bash
sudo raspi-config

# 以下の順で選択:
# 7 Advanced Options
# → A3 Memory Split
# → 128 または 256 を入力

# 再起動
sudo reboot
```

### 2. スワップサイズの増加（4GBモデルの場合）

メモリ4GBのRaspberry Piの場合、スワップサイズを増やすことで安定性が向上します:

```bash
# スワップファイル設定を編集
sudo nano /etc/dphys-swapfile

# 以下の行を変更:
# CONF_SWAPSIZE=100
# ↓
# CONF_SWAPSIZE=2048

# 保存して閉じる（Ctrl+X, Y, Enter）

# スワップサービスを再起動
sudo dphys-swapfile swapoff
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### 3. 不要なサービスの停止

```bash
# Bluetoothを無効化（使用しない場合）
sudo systemctl disable bluetooth
sudo systemctl stop bluetooth

# 再起動
sudo reboot
```

## トラブルシューティング

### カメラが認識されない

**症状**: `カメラを開けませんでした` エラー

**解決策**:

1. カメラケーブルの接続確認
   - ケーブルがしっかり差し込まれているか
   - 向きが正しいか（青い面がEthernet側）

2. カメラインターフェースの有効化確認
   ```bash
   sudo raspi-config
   # Interface Options → Camera → Enabled
   ```

3. カメラデバイスの確認
   ```bash
   ls /dev/video*
   # /dev/video0 などが表示されるか確認
   ```

4. 別のデバイス番号を試す
   ```bash
   python detect.py --source 1
   # または
   python detect.py --source 2
   ```

### pipインストールでエラーが発生

**症状**: `error: externally-managed-environment`

**解決策**: 仮想環境を使用する

```bash
# 必ず仮想環境をアクティベートしてからインストール
source yolo_env/bin/activate
pip install -r requirements.txt
```

### メモリ不足エラー

**症状**: `Killed` または `Out of memory`

**解決策**:

1. 他のアプリケーションを終了
2. スワップサイズを増やす（上記参照）
3. より小さいモデルを使用
   ```bash
   python detect.py --model yolov8n.pt
   ```

### YOLOモデルのダウンロードが失敗

**症状**: `Failed to download model`

**解決策**:

1. インターネット接続を確認
2. 手動でダウンロード
   ```bash
   cd models
   wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
   cd ..
   ```

## 次のステップ

セットアップが完了したら、以下を試してみましょう:

1. **基本的な実行**
   ```bash
   python detect.py
   ```

2. **信頼度閾値の調整**
   ```bash
   python detect.py --conf 0.5
   ```

3. **ビデオファイルでのテスト**
   ```bash
   python detect.py --source test_data/sample_video.mp4
   ```

4. **コードの読解**
   - `detect.py`を開いて、各関数の動作を理解してみましょう
   - コメントを読みながら、YOLOの仕組みを学習しましょう

楽しい学習体験を！
