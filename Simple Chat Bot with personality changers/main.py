import openai
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def main(personality):

    intial_prompt = f"You are a conversational chatbot. Your personality is {personality}"
    messages = [{"role": "system", "content": intial_prompt}]
    while True:
        try:
            user_input = input("You: ")
            messages.append({"role": "user", "content": user_input})
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            messages.append({"role": "assistant", "content": response.choices[0].message.content})
            print(f"Assistant: {response.choices[0].message.content}")
        except KeyboardInterrupt:
            print("Exiting...")
            break

if __name__ == "__main__":
    user_response = input("Are you happy to begin with the default personality? Y/N: ")
    if user_response.capitalize() == "Y":
        main("Friendly and helpful")
    else:
        res = input("What chatbot personality would you like?: ")
        main(res)
