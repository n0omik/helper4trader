from Config.settings import OPENAI_KEY
from openai import OpenAI

client = OpenAI(api_key=OPENAI_KEY)


async def get_project_info(symbol):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": "You are a cryptocurrency expert, skilled in explaining complex concepts with creative flair. A cryptocurrency trader asks you what your project is and what its prospects are. Answer in English and only in 2 paragraphs, no more than 2000 characters."},
    {"role": "user", "content": f"Tell me about a project that has a {symbol} coin behind it. Who is the founder, how old is the project, what platforms are there, where the coin is used."}
  ]
)
  return completion.choices[0].message


