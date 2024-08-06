from openai import OpenAI
# pip install openai

client = OpenAI()
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key="sk-proj-WxSl7ehGk2PnwzCHcDwT3BlbkYFJFMj6bYTk9G1bqZaFTcj",
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a virtual assistant name jarvis skilled in general tasks like Alex and Google Cloud"},
    {"role": "user", "content": "What is coding"}
  ]
)

print(completion.choices[0].message.content)