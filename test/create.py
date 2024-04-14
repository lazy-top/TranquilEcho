import ollama

# 运行Llama 2模型
response = ollama.chat(
  model='qwen',
  messages=[
    {
      'role': 'system',
      'content': '作为一名心理咨询师，你的职责是帮助患者解决心理问题并提供有效的建议。请描述你如何倾听患者，并根据他们的需求提供适当的建议和支持。你的回答应包括建立信任关系的方法，了解患者的感受和想法，提供实用的建议和指导，以及跟进和帮助患者实现他们的目标。请提供具体的例子和案例，以帮助患者更好地理解你的建议，并提高你的专业性和可信度。让我们一步步来思考。让我们一步一步来思考'
    },
  {
    'role': 'user',
    'content': '我头有点痛，想找个人聊聊。',
  },],
  stream=True,
                       )
ollama.generate()

for chunk in response:
  print(chunk['message']['content'], end='', flush=True)
