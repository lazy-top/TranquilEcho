import ollama

# 运行Llama 2模型
response = ollama.chat(
  model='qwen',
  messages=[
  {
    'role': 'user',
    'content': '你能做什么呢？',
  },],
  stream=True,
                       )

for chunk in response:
  print(chunk['message']['content'], end='', flush=True)