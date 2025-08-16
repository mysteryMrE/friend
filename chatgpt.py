import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class ChatGPT:
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.OPENAI_API_KEY)

    def generate_response(self, prompt):

        response = self.client.chat.completions.create(
            model="gpt-5-nano-2025-08-07",
            messages=[
                {
                    "role": "user",
                    "content": f"answer in less than 15 words: {prompt}",
                }
            ],
        )
        return response.choices[0].message.content.strip()


if __name__ == "__main__":
    user_input = input("You: ")
    chat_gpt = ChatGPT()
    response = chat_gpt.generate_response(user_input)
    print("ChatGPT: " + response)
