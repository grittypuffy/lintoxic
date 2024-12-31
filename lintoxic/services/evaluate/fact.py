import aiohttp
import logging
from lintoxic.constants.fact import FACT_CHECKER_API_ENDPOINT as url
from lintoxic.constants.fact import FACT_CHECKER_API_HEADERS as headers

async def check_fact_accuracy(text: str):
    data: dict = {
        "text": text
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                contents = await response.json()
                true_facts: int = 0
                false_contents: list[dict] = []

                for content in contents:
                    if content["is_correct"]:
                        true_facts += 1
                    else:
                        false_contents.append(content)
                accuracy: float = (true_facts / len(contents)) * 100
                return FactCheckResponse(accuracy=accuracy, text=text, false_information=false_contents if false_contents else None)
            else:
                raise Exception(f"{response.status}")

