import os
import openai
from app.retriever import find_relevant_content

openai.api_key = os.getenv("OPENAI_API_KEY")

def build_prompt(question, course_content, discourse_content):
    prompt = f"Answer the following question:\n\n{question}\n\n"
    prompt += "Here is some related course content:\n"
    for item in course_content:
        prompt += f"- {item['title']}\n"

    prompt += "\nHere are some related Discourse posts:\n"
    for item in discourse_content:
        prompt += f"- {item['title']} ({item['url']})\n"

    prompt += "\nGive a helpful and concise answer based on the above."
    return prompt

def answer_question(question, image=None):  # ✅ Accept image argument
    course_content, discourse_content = find_relevant_content(question)

    prompt = build_prompt(question, course_content, discourse_content)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    answer = response['choices'][0]['message']['content']
    links = [{"url": item["url"], "text": item["title"]} for item in discourse_content]

    return {
        "answer": answer,
        "links": links
    }
