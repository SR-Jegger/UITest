# utils/model.py

import os
import base64
# from openai import OpenAI
from typing import List, Dict, Any
import dashscope
# API_KEY = os.getenv("OPENAI_API_KEY")
# BASE_URL = os.getenv("OPENAI_BASE_URL")

# class LVMChat:
#     """多模态大模型聊天类"""
    
#     def __init__(self, api_key: str = API_KEY, base_url: str = BASE_URL, 
#                  model: str = "gemini-3-flash-preview"):
#         self.client = OpenAI(api_key=api_key, base_url=base_url)
#         self.model = model
    
#     def _encode_image(self, image_path: str) -> str:
#         """将图片编码为base64"""
#         with open(image_path, "rb") as image_file:
#             return base64.b64encode(image_file.read()).decode('utf-8')
    
#     def get_multimodal_response(self, text: str, image_paths: str) -> str:
#         """
#         最简单的图文对话
        
#         Args:
#             text: 你的问题
#             image_paths: 图片路径
        
#         Returns:
#             模型的回答
#         """
#         # 1. 加载图片
#         base64_image = self._encode_image(image_paths)
        
#         # 2. 构建消息
#         messages = [{
#             "role": "user",
#             "content": [
#                 {"type": "image_url", 
#                  "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
#                 {"type": "text", "text": text}
#             ]
#         }]
        
#         # 3. 调用API
#         response = self.client.chat.completions.create(
#             model=self.model,
#             messages=messages
#         )
        
#         return response.choices[0].message.content


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
        
        # 3. 调用API
        response = dashscope.Generation.call(
            model=self.model,   # 推荐：qwen-plus / qwen-max
            messages=messages,
            # temperature=0,
            # result_format="message",
            api_key=self.api_key  # 使用类中存储的 API Key
    )
        
        return response.choices[0].message.content
