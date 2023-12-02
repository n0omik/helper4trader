import asyncio
from openai import OpenAI
from Config.settings import OPENAI_KEY

client = OpenAI(api_key=OPENAI_KEY)


async def openai_request(symbol):
    modified_symbol = symbol.replace('USDT', '')
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "You are a cryptocurrency expert, skilled in explaining complex concepts. Just tell the truth, don't make things up. A cryptocurrency trader asks you what your project is and what its prospects are. Answer in English and only in 2 paragraphs, no more than 2000 characters."},
            {"role": "user",
             "content": f"Tell me about the main and first project that is founded and launched using the {modified_symbol} coin. In your story, mention who the founder is, what country he is from, how old the project is, what platforms currently support this project, what protocol is used, where the coin is used, and fill in any other information you feel you need to convey. "}
        ]
    )
    answer = completion.choices[0].message.content
    return answer


async def get_project_info_openai(symbol):
    result = await openai_request(symbol)
    return result


#print(asyncio.run(get_project_info("BTCUSDT")))

