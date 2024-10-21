# If necessary, install the openai Python library by running 
# pip install openai

from openai import OpenAI

client = OpenAI(
	base_url="https://lkskr2st3kpkh4kt.us-east-1.aws.endpoints.huggingface.cloud/v1/", 
	api_key="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" 
)

chat_completion = client.chat.completions.create(
	model="tgi",
	messages=[
    {
        "role": "user",
     
        "content": "What is deep learning?"
    }
],
	top_p=None,
	temperature=None,
	max_tokens=150,
	stream=False,
	seed=None,
	frequency_penalty=None,
	presence_penalty=None
)

for message in chat_completion:
	print(message.choices[0].delta.content, end="")