import cv2
import os
import numpy
from PIL import Image
from scipy.spatial import KDTree
from tqdm import tqdm  # 新增進度條

# === 可調整參數 ===
MainPhotoPath = 'demo_photo.jpg' #被製作蒙太奇的圖片
block = 100                     #切塊程度
image_folder = './img'          #放置素材的資料夾(記得先用GetPhoto)
OutputName = 'demo_output.jpg'        #輸出檔案名稱
multiple = 1                    #圖片放大倍數(不建議超過5)

colordb={}
kdtree = None
path_list = []

def AvgColor(Photo):
    #OpenCV
    if isinstance(Photo, numpy.ndarray):  
        b, g, r = cv2.split(Photo)
    #PIL    
    else:
        Photo = numpy.array(Photo)
        r, g, b = Photo[:,:,0], Photo[:,:,1], Photo[:,:,2]
    
    # 一律回傳 RGB 順序
    return [int(numpy.mean(r)), int(numpy.mean(g)), int(numpy.mean(b))]

def PreloadTiles(width, height):
    tile_cache: dict[str, Image.Image] = {}
    for path, _ in tqdm(colordb.items(), desc="預載素材", unit="張"):
        img = Image.open(path).resize((width, height))
        tile_cache[path] = img
    return tile_cache

def ColorDB():
    jpg_files = [f for f in os.listdir(image_folder) if f.lower().endswith('.jpg') and f.startswith('img_')]
    for filename in tqdm(jpg_files, desc="掃描素材", unit="張"):
        full_path = os.path.join(image_folder, filename)
        img = cv2.imread(full_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 轉成 RGB
        avg = AvgColor(img)
        colordb[full_path] = avg
    print(f"總共載入 {len(colordb)} 張圖片")

def FindPhoto(target_color):
    _, idx = kdtree.query(target_color)
    return path_list[idx]

def SpiltPhoto():
    MainPhoto = Image.open(MainPhotoPath)
    w, h = MainPhoto.size

    MainPhoto = MainPhoto.resize((w*multiple, h*multiple))
    w, h = MainPhoto.size

    w = (w // block) * block
    h = (h // block) * block

    MainPhoto = MainPhoto.crop((0, 0, w, h))

    col_wid = w // block
    row_hei = h // block

    bg = Image.new('RGB', (w, h))
    tile_cache = PreloadTiles(col_wid, row_hei)

    # 設定 tqdm 進度條
    total_tiles = block * block
    progress = tqdm(total=total_tiles, desc="合成中", unit="塊")
    
    for i in range(block):
        for j in range(block):
            x = i * col_wid
            y = j * row_hei
            crop = MainPhoto.crop((x, y, x + col_wid, y + row_hei))
            arr = numpy.array(crop)
            avg_color = AvgColor(arr)

            match_path = FindPhoto(avg_color)
            tile = tile_cache[match_path]
            bg.paste(tile, (x, y))

            progress.update(1)  # 更新進度

    bg.save(OutputName)
    print("輸出完成")

def SaveColorDB(path='colordb.txt'):
    with open(path, 'w') as f:
        for key, value in colordb.items():
            f.write(f"{key},{value[0]},{value[1]},{value[2]}\n")

def LoadColorDB(path='colordb.txt'):
    global colordb
    colordb = {}
    with open(path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            path = parts[0]
            rgb = list(map(float, parts[1:]))
            colordb[path] = rgb

def BuildKDTree():
    global kdtree, path_list
    color_vectors = []
    path_list = []
    for path, color in colordb.items():
        color_vectors.append(color)
        path_list.append(path)
    kdtree = KDTree(color_vectors)
    print("KDTree建構完成")

if os.path.exists('colordb.txt'):
    print("已有資料庫，直接載入")
    LoadColorDB()
else:
    ColorDB()
    SaveColorDB()

BuildKDTree()
SpiltPhoto()
