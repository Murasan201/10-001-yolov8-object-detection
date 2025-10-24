from ultralytics import YOLO
import psutil

# YOLOモデルを読み込み
model = YOLO('yolov8n.pt')

# Ultralytics公式のサンプル画像を使用
# bus.jpgには、バス、人、車などが写っています
image_url = 'https://ultralytics.com/images/bus.jpg'

print("YOLO推論を実行中...")
print(f"テスト画像: {image_url}")

# 物体検出を実行
results = model(image_url)

print(f"検出完了。結果数: {len(results)}")

# 検出された物体の情報を表示
for result in results:
    boxes = result.boxes
    print(f"\n検出された物体数: {len(boxes)}")
    for box in boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        class_name = result.names[class_id]
        print(f"  - {class_name}: 信頼度 {confidence:.2f}")

# 結果を画像に描画して保存
annotated_image = results[0].plot()
results[0].save('yolo_test_result.jpg')

print("\nテスト完了。結果画像をyolo_test_result.jpgに保存しました。")
print("\nシステムリソース使用状況:")
print(f"CPU使用率: {psutil.cpu_percent()}%")
print(f"メモリ使用率: {psutil.virtual_memory().percent}%")
