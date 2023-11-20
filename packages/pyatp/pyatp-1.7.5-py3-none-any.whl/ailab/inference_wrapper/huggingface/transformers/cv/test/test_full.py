from aiges.dto import Response, ResponseData, DataListNode, DataListCls

"""personal param"""
# model_name = 'vit_patch16_224_in21k'
# full_path = '/data1/cgzhang6/ailab_sdk/src/test/ailabmodel/my_vit_patch16'
# module_name = 'image_classification'
model_name = 'yolos_small'
full_path = '/data1/cgzhang6/ailab_sdk/src/test/ailabmodel/my_yolos_small_50epoch'
module_name = 'object_detection'
""""""

import sys
print(sys.path)

import importlib
module_path = f'ailab.inference_wrapper.huggingface.transformers.cv.{module_name}.wrapper.wrapper_full'
wrapper_module = importlib.import_module(module_path)
Wrapper = getattr(wrapper_module, 'Wrapper')
wrapper = Wrapper()

def Init():
    import os
    os.environ['FULL_MDOEL_PATH'] = full_path
    wrapper.wrapperInit({})

def Once(key, text):
    http_node = DataListNode()
    http_node.key = 'image'
    with open(text, 'rb') as file:
        # 读取文件内容
        image_data = file.read()
    http_node.data = image_data
    http_data = DataListCls()
    http_data.list.append(http_node)
    wrapper.wrapperOnceExec({"atp_patch_id":key}, http_data, key)

if __name__ == '__main__' :
    Init()

    # 图像分类
    # Once(1, '/data1/cgzhang6/images/test_pic/sunflower01.jpg')
    # Once(1, '/data1/cgzhang6/images/test_pic/peony04.jpg')
    # Once(1, '/data1/cgzhang6/images/test_pic/rose03.jpg')
    # Once(1, '/data1/cgzhang6/images/test_pic/lily05.jpg')
    # Once(1, '/data1/cgzhang6/images/test_pic/peony01.jpg')
    # Once(1, '/data1/cgzhang6/images/test_pic/sakura01.jpg')

    # 目标检测
    Once(1, '/data1/cgzhang6/ailab_sdk/src/ailab/inference/test/images/detection/1001.png')
    Once(1, '/data1/cgzhang6/ailab_sdk/src/ailab/inference/test/images/detection/1002.png')
    Once(1, '/data1/cgzhang6/ailab_sdk/src/ailab/inference/test/images/detection/1003.png')
    Once(1, '/data1/cgzhang6/ailab_sdk/src/ailab/inference/test/images/detection/1004.png')
    Once(1, '/data1/cgzhang6/ailab_sdk/src/ailab/inference/test/images/detection/1005.png')
    Once(1, '/data1/cgzhang6/ailab_sdk/src/ailab/inference/test/images/detection/1006.png')
