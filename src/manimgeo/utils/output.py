import random
import hashlib

ENABLE_MANIMGEO_COLORFUL_OUTPUT = True

def generate_simple_color():
    """
    简约风格随机色
    :return: 生成的 RGB 颜色值
    """
    # 生成一个较低饱和度的颜色（例如，saturation 在 30% 到 60% 之间）
    saturation = random.uniform(0.3, 0.6)
    lightness = random.uniform(0.4, 0.7)  # 明度范围 40% 到 70%

    # 使用 HSL 转 RGB 的方式生成颜色
    # 色相：随机生成一个色相，范围为 0 到 360 度
    hue = random.randint(0, 360)
    
    # HSL 转 RGB
    return hsl_to_rgb(hue, saturation, lightness)

def hsl_to_rgb(hue, saturation, lightness):
    """
    将 HSL 颜色转换为 RGB
    :param hue: 色相 (0-360)
    :param saturation: 饱和度 (0-1)
    :param lightness: 明度 (0-1)
    :return: RGB 颜色 (0-255)
    """
    c = (1 - abs(2 * lightness - 1)) * saturation
    x = c * (1 - abs(((hue / 60) % 2) - 1))
    m = lightness - c / 2
    
    if 0 <= hue < 60:
        r, g, b = c, x, 0
    elif 60 <= hue < 120:
        r, g, b = x, c, 0
    elif 120 <= hue < 180:
        r, g, b = 0, c, x
    elif 180 <= hue < 240:
        r, g, b = 0, x, c
    elif 240 <= hue < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    r = int((r + m) * 255)
    g = int((g + m) * 255)
    b = int((b + m) * 255)

    return r, g, b

def generate_color_from_id(obj):
    # 获取对象的id并转换为字节序列
    obj_id = id(obj)
    byte_rep = obj_id.to_bytes((obj_id.bit_length() + 7) // 8, byteorder='big')
    
    # 生成SHA1哈希
    hash_bytes = hashlib.sha1(byte_rep).digest()
    
    # 分割哈希字节为hue, saturation, lightness部分
    hue_bytes = hash_bytes[:4]
    saturation_bytes = hash_bytes[4:8]
    lightness_bytes = hash_bytes[8:12]
    
    # 计算hue（0-359）
    hue = int.from_bytes(hue_bytes, byteorder='big') % 360
    
    # 计算saturation（0.3-0.6）
    max_value = 0xFFFFFFFF  # 4字节的最大值
    saturation_scaled = int.from_bytes(saturation_bytes, byteorder='big') / max_value
    saturation = 0.3 + saturation_scaled * (0.6 - 0.3)
    
    # 计算lightness（0.4-0.7）
    lightness_scaled = int.from_bytes(lightness_bytes, byteorder='big') / max_value
    lightness = 0.4 + lightness_scaled * (0.7 - 0.4)
    
    return hsl_to_rgb(hue, saturation, lightness)

def color_text(text, r, g, b):
    """
    将文本转换为指定的 RGB 颜色

    :param text: 要显示的文本
    :param r: 红色通道 (0-255)
    :param g: 绿色通道 (0-255)
    :param b: 蓝色通道 (0-255)
    :return: 带有 RGB 颜色的文本
    """
    # ANSI 转义序列：\033[38;2;r;g;b m 设置前景色
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m" if ENABLE_MANIMGEO_COLORFUL_OUTPUT else text
