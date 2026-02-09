# utils/model.py

import os
import base64
from openai import OpenAI
from typing import List, Dict, Any
import dashscope

import requests

def upload_to_smms(image_path: str) -> str:
    """上传本地图片到 sm.ms，返回公网 HTTPS URL"""
    with open(image_path, "rb") as f:
        response = requests.post(
            "https://sm.ms/api/v2/upload",
            files={"smfile": f}
        )
    data = response.json()
    if data.get("success"):
        return data["data"]["url"]  # e.g. "https://i.sm.cn/xxx.jpg"
    else:
        raise RuntimeError(f"上传失败: {data.get('message', '未知错误')}")




class QwenVL:
    """多模态大模型聊天类"""
    
    def __init__(self, model: str = "qwen3-vl-plus"):
        # self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.api_key = "sk-ed54c3fd9a7345c1b72a9a72a30791ce"
    
    def _encode_image(self, image_path: str) -> str:
        """将图片编码为base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def get_multimodal_response(self, text: str, image_paths: str) -> str:
        """
        最简单的图文对话
        
        Args:
            text: 你的问题
            image_paths: 图片路径
        
        Returns:
            模型的回答
        """
        # 1. 加载图片
        base64_image = self._encode_image(image_paths)
        
        # 2. 构建消息
        messages = [{
            "role": "user",
            "content": [
                {"type": "image_url", 
                 "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                {"type": "text", "text": text}
            ]
        }]
        # print(image_paths)
        # # ✅ 使用示例：
        # image_url = upload_to_smms(image_paths)
        # print("上传成功，URL:", image_url)
        # messages = [{
        #     "role": "user",
        #     "content": [
        #         {"type": "image", 
        #          "image": image_url},
        #         {"type": "text", 
        #          "text": text}
        #     ]
        # }]
        
        # 3. 调用API
        response = dashscope.Generation.call(
            model=self.model,   # 推荐：qwen-plus / qwen-max
            messages=messages,
            type="json_object",
            # temperature=0,
            # result_format="message",
            api_key=self.api_key  # 使用类中存储的 API Key
        )
        print(response)
        return response.output.choices[0].message.content
class LVMChat:
    """多模态大模型聊天类"""
    
    def __init__(self, model: str = "qwen3-vl-plus"):
        self.client = OpenAI(api_key="sk-ed54c3fd9a7345c1b72a9a72a30791ce", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
        self.model = model
    
    def _encode_image(self, image_path: str) -> str:
        """将图片编码为base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def get_multimodal_response(self, text: str, image_paths: str) -> str:
        """
        最简单的图文对话
        
        Args:
            text: 你的问题
            image_paths: 图片路径
        
        Returns:
            模型的回答
        """
        # 1. 加载图片
        base64_image = self._encode_image(image_paths)
        
        # 2. 构建消息
        messages = [{
            "role": "user",
            "content": [
                {"type": "image_url", 
                 "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                {"type": "text", "text": text}
            ]
        }]
        
        # 3. 调用API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        
        return response.choices[0].message.content