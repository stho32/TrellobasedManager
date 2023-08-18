import openai
from library.configuration import load_config

config = load_config()
openai.api_key = config["GPT_API_KEY"]


def send_prompt_to_gpt(prompt, model="text-davinci-002"):
    if config["GPT_API_KEY"] == "your_gpt3.5_api_key":
        return "no api key provided"

    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.8,
    )

    return response.choices[0].text.strip()  # type: ignore
