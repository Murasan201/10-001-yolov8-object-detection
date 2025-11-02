#!/usr/bin/env python3
"""
YOLOv8パフォーマンスベンチマークテスト
YOLOv8モデルの推論パフォーマンスを測定するテストスクリプト
要件定義書: 10-001_YOLO物体検出アプリ_要件定義書.md
"""

import sys
import time

# 標準ライブラリ
# （time は標準ライブラリ）

# サードパーティライブラリ
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


def run_benchmark(model, image_url, num_runs=10):
    """
    ベンチマークテストを実行して推論時間を計測

    Args:
        model (YOLO): YOLOv8モデル
        image_url (str): テスト用画像のURL
        num_runs (int): 実行回数（デフォルト: 10）

    Returns:
        list: 各実行の実行時間（秒）のリスト
    """
    test_times = []

    print('ベンチマークテストを実行中...')
    print(f'テスト画像: {image_url}')
    print(f'{num_runs}回の推論を実行して平均時間を計測します。\n')

    try:
        for i in range(num_runs):
            start_time = time.time()
            # verbose=False: ログ出力を抑制
            results = model(image_url, verbose=False)
            end_time = time.time()

            execution_time = end_time - start_time
            test_times.append(execution_time)
            print(f'実行{i + 1}: {execution_time:.2f}秒')

        return test_times

    except Exception as e:
        print(f'[ベンチマーク実行]エラー: {e}')
        print('対処方法: インターネット接続を確認するか、ローカルのモデルを使用してください')
        sys.exit(1)


def print_results(test_times):
    """
    ベンチマーク結果を計算して表示

    Args:
        test_times (list): 各実行の実行時間（秒）のリスト
    """
    if not test_times:
        print('エラー: テスト結果がありません')
        return

    # 統計情報を計算
    average_time = sum(test_times) / len(test_times)
    fps = 1 / average_time

    print('\n結果:')
    print(f'平均実行時間: {average_time:.2f}秒')
    print(f'推定FPS: {fps:.1f}')
    print(f'最速実行時間: {min(test_times):.2f}秒')
    print(f'最遅実行時間: {max(test_times):.2f}秒')


def main():
    """
    メイン関数：ベンチマークテストを実行
    """
    # Ultralytics公式のサンプル画像を使用
    # bus.jpgには、バス、人、車などが写っています
    image_url = 'https://ultralytics.com/images/bus.jpg'

    # YOLOモデルを読み込み
    model = load_model('yolov8n.pt')

    # ベンチマークテストを実行
    test_times = run_benchmark(model, image_url, num_runs=10)

    # 結果を表示
    print_results(test_times)


if __name__ == '__main__':
    main()
