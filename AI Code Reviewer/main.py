import openai
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


prompt = """
You will receive a file's contents as text. Generate a code review for the file.
Indicate what changes should be made to improve its style, performance, readability and maintainability.
If there are any reputable libraries that could be introduced to improve the code, suggest them. Be kind and constructive.
Please make sure that under each step, you include the line number of the change you are referring to.
"""

def code_review(file_path):
    with open("Selected file here", "r") as file:
        content = file.read()
    generated_review = make_code_review_request(content)


def make_code_review_request(file_content):
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Code review the following file: {file_content}"}
    ]


    res = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    print(res.choices[0].message.content)


if __name__ == "__main__":
    code_review("review_file.py")