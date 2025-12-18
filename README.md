#蒙太奇拼貼產生器(Montage Generator)
這是一個使用 Python 實作的圖片蒙太奇生成工具。
它能夠從影片中擷取畫面作為素材，並透過 KD-Tree 演算法快速進行色彩比對，將一張主圖片（Main Photo）用成千上萬張的微小素材圖片拼貼重組而成。

##特色
- 影片轉素材：內建工具可自動將影片 (.mp4) 依時間間隔截圖，建立素材庫。
- 高效能比對：使用 scipy.spatial.KDTree 進行色彩空間搜尋，比傳統逐一比對快上許多。
- 快取機制：首次執行會分析素材顏色並建立 colordb.txt 資料庫，大幅加速後續執行速度。
- 進度顯示：整合 tqdm 進度條，隨時掌握素材掃描與圖片合成進度。

##環境需求
請確保您的 Python 環境已安裝以下套件：
- numpy
- scipy
- tqdm
- opencv-python
- pillow
可以直接輸入以下指令安裝
```
pip install opencv-python numpy pillow scipy tqdm
```

##檔案結構
- main.py: 主程式，使用 KD-Tree 演算法生成蒙太奇拼貼，
- prepare_photo.py: 影片轉素材，將你準備的影片切分成可以用於生成蒙太奇圖片的素材。

##使用方法

### Step 1. 準備素材
使用 prepare_photo.py 將你的影片轉換成素材圖片，存放在 ./img 的目錄下。
請修改prepare_photo.py程式碼中的 test.mp4 修改為你的影片名稱，並放置於同一目錄下。
```
cap = cv2.VideoCapture('test.mp4')
```

### Step 2. 產生蒙太奇
1. 準備一張需要被生成的圖片，將其命名為 MainPhoto.jpg 並放在專案根目錄。
2. 確認參數進行修改。
    - MainPhotoPath：被生成圖片路徑，請確認與你的檔案名稱一致。
    - block：切塊程度。數值越小，拼貼的顆粒越細緻（圖片張數越多），但計算時間會變長。
    - image_folder：放置素材的資料夾(記得先用GetPhoto)。
    - OutputName：輸出檔案名稱。
    - multiple：放大倍數。若原圖解析度太低，可調高此數值放大輸出成果 (建議不超過 5)。
3. 執行主程式 main.py。

## 範例成果
以下是使用本工具生成的蒙太奇拼貼範例：

| 原始圖片 | 蒙太奇成果 |
| :---: | :---: |
| ![Original](demo_photo.jpg) | ![Result](demo_output.jpg) |

