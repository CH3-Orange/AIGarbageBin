
# coding: utf-8

import time
import json
import numpy as np
import tensorflow as tf
from PIL import Image

# 加载模型并分配张量
interpreter = tf.lite.Interpreter(model_path="./converted_model.tflite")
interpreter.allocate_tensors()
# 获取输入输出张量
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
# print(input_details)
# print(output_details)

#加载分类
with open("./garbage_classify_rule.json", 'r',encoding='utf-8') as load_f:
            load_dict = json.load(load_f)




image = Image.open(r'D:\Program\Python\RaspberryPi\AIGarbageBin\From\image.png').convert('RGB').resize(
            (224, 224), Image.ANTIALIAS)
image = np.array(image,dtype=np.float32).reshape(input_details[0]['shape'])
# start =time.process_time #计算时间
interpreter.set_tensor(input_details[0]['index'],image)
interpreter.invoke()
output_data = interpreter.get_tensor(output_details[0]['index'])
pred_label = np.argmax(output_data[0])
# elapsed = (time.process_time - start)
# print("Time used:",elapsed,"ms")
print(pred_label)
print(load_dict[str(pred_label)])
