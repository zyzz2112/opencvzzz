import cv2
import numpy as np
import pyautogui
from pynput.mouse import Button, Controller
import time

# Tạo đối tượng chuột
mouse = Controller()

# Tải nhiều hình ảnh mẫu mà bạn muốn tìm
templates = [
    cv2.imread('test1.png', 0),
    cv2.imread('test2.png', 0),
    cv2.imread('test3.png', 0)
]

# Kiểm tra xem tất cả hình ảnh có được tải thành công không
for idx, template in enumerate(templates):
    if template is None:
        print(f"Không thể tải hình ảnh mẫu {idx + 1}.")
        exit()

while True:
    # Chụp màn hình hiện tại
    screenshot = pyautogui.screenshot()
    
    # Chuyển đổi ảnh screenshot thành grayscale
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    
    # Lặp qua từng hình ảnh mẫu
    for idx, temp in enumerate(templates):
        # Tìm vị trí của hình ảnh mẫu trong screenshot
        result = cv2.matchTemplate(screenshot, temp, cv2.TM_CCOEFF_NORMED)
        
        # Ngưỡng để quyết định sự khớp
        threshold = 0.8  # Bạn có thể điều chỉnh ngưỡng này

        # Tìm vị trí trong kết quả khớp trên ngưỡng
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            # Tính tọa độ của điểm cần click
            temp_height, temp_width = temp.shape
            center_x = max_loc[0] + temp_width // 2
            center_y = max_loc[1] + temp_height // 2

            # Click vào vị trí đó mà không di chuyển chuột
            mouse.position = (center_x, center_y)
            mouse.click(Button.left, 1)
            print(f"Đã click vào mẫu {idx + 1} tại vị trí: ({center_x}, {center_y})")
        else:
            print(f"Không tìm thấy hình ảnh mẫu {idx + 1} phù hợp.")
    
    # Đợi một thời gian ngắn để tránh quá tải CPU
    time.sleep(1)
