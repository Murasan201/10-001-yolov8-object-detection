#!/usr/bin/env python3
"""
YOLOv8初回実行テスト
Ultralytics公式のサンプル画像を使ってYOLOモデルが正常に動作するか確認するテストスクリプト
要件定義書: 10-001_YOLO物体検出アプリ_要件定義書.md
"""

import sys

# 標準ライブラリ
# （このスクリプトではサードパーティのみを使用）

# サードパーティライブラリ
import psutil
from ultralytics import YOLO


def load_model(model_path='yolov8n.pt'):
    """
    YOLOv8モデルを読み込む

    Args:
        model_path (str): モデルファイルのパス（デフォルト: yolov8n.pt）

    Returns:
        YOLO: 読み込まれたYOLOモデル
    """
    try:
        model = YOLO(model_path)
        return model
    except Exception as e:
        print(f'[モデル読み込み]エラー: {e}')
        print('対処方法: モデルファイルが存在するか確認してください')
        print(f'ヒント: {model_path} が現在のディレクトリにあるか確認')
        sys.exit(1)


def run_inference(model, image_url):
    """
    物体検出推論を実行して結果を表示

    Args:
        model (YOLO): YOLOv8モデル
        image_url (str): 推論対象の画像URL

    Returns:
        list: 推論結果のリスト
    """
    try:
        print('YOLO推論を実行中...')
        print(f'テスト画像: {image_url}')

        # 物体検出を実行
        results = model(image_url)

        print(f'検出完了。結果数: {len(results)}')

        # 検出された物体の情報を表示
        for result in results:
            boxes = result.boxes
            print(f'\n検出された物体数: {len(boxes)}')
            for box in boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = result.names[class_id]
                print(f'  - {class_name}: 信頼度 {confidence:.2f}')

        return results

    except Exception as e:
        print(f'[推論実行]エラー: {e}')
        print('対処方法: インターネット接続を確認するか、ローカルのモデルを使用してください')
        sys.exit(1)


def save_result(results, output_path='yolo_test_result.jpg'):
    """
    推論結果を画像ファイルとして保存

    Args:
        results (list): 推論結果のリスト
        output_path (str): 保存先ファイルパス
    """
    try:
        results[0].save(output_path)
        print(f'\nテスト完了。結果画像を {output_path} に保存しました。')
    except Exception as e:
        print(f'[結果保存]エラー: {e}')
        print('対処方法: 書き込み権限を確認してください')


def show_system_resources():
    """
    システムリソース使用状況を表示
    """
    print('\nシステムリソース使用状況:')
    print(f"CPU使用率: {psutil.cpu_percent()}%")
    print(f"メモリ使用率: {psutil.virtual_memory().percent}%")


def main():
    """
    メイン関数：YOLOv8の初回実行テストを実行
    """
    # Ultralytics公式のサンプル画像を使用
    # bus.jpgには、バス、人、車などが写っています
    image_url = 'https://ultralytics.com/images/bus.jpg'

    # YOLOモデルを読み込み
    model = load_model('yolov8n.pt')

    # 物体検出を実行
    results = run_inference(model, image_url)

    # 結果を画像に描画して保存
    save_result(results)

    # システムリソース情報を表示
    show_system_resources()


if __name__ == '__main__':
    main()
