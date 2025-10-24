from ultralytics import YOLO
import time

model = YOLO('yolov8n.pt')

# Ultralytics公式のサンプル画像を使用
image_url = 'https://ultralytics.com/images/bus.jpg'

# 複数回実行して平均実行時間を計測
test_times = []

print("ベンチマークテストを実行中...")
print(f"テスト画像: {image_url}")
print("10回の推論を実行して平均時間を計測します。\n")

for i in range(10):
    start_time = time.time()
    results = model(image_url, verbose=False)
    end_time = time.time()

    execution_time = end_time - start_time
    test_times.append(execution_time)
    print(f"実行{i+1}: {execution_time:.2f}秒")

average_time = sum(test_times) / len(test_times)
fps = 1 / average_time

print(f"\n結果:")
print(f"平均実行時間: {average_time:.2f}秒")
print(f"推定FPS: {fps:.1f}")
print(f"最速実行時間: {min(test_times):.2f}秒")
print(f"最遅実行時間: {max(test_times):.2f}秒")
