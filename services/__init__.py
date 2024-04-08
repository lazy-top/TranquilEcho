# from langchain.llms import ollama
# from langchain.callbacks import StreamingStdOutCallbackHandler

# # 初始化ollama
# llm =ollama(model_name='qwen', streaming=True)

# # 定义回调处理器
# class MyStreamingHandler(StreamingStdOutCallbackHandler):
#     def __init__(self):
#         self.buffer = ""

#     def on_new_token(self, token):
#         # 这里处理每个新生成的token
#         self.buffer += token
#         if "\n" in self.buffer:
#             message, self.buffer = self.buffer.split("\n", 1)
#             yield f"data: {message}\n\n"
# # 使用ollama处理用户输入
# def process_user_input(user_input):
#     handler = MyStreamingHandler()
#     llm.predict(user_input, callbacks=[handler])
#     return handler.generate_tokens()