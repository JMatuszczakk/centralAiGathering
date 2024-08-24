import math

def color_distance(color1, color2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(color1, color2)))

def check_color_similarity(img):
    width, height = img.size
    center_bottom = img.getpixel((width // 2, height - 1))
    bottom_right = img.getpixel((width - 1, height - 1))
    
    similarity_threshold = 10
    print(f"Center bottom: {center_bottom}")
    print(f"Bottom right: {bottom_right}")
    print(f"Color distance: {color_distance(center_bottom, bottom_right)}")
    
    return color_distance(center_bottom, bottom_right) < similarity_threshold
