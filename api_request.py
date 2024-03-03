import os
from openai import OpenAI
import google.generativeai as genai
import streamlit as st

class GPT:

    def __init__(self, init_prompt, is_4 = True): 
        self.init_prompt = init_prompt
        self.client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
        self.gpt_ver = 'gpt-4-0125-preview' if is_4 else 'gpt-3.5-turbo-0125'
    
    def read_history(self, history): 
        messages = []
        messages.append({"role": "system", "content": self.init_prompt})

        for dict in history: 
            messages.append({
                'role': dict['role'], 
                'content': dict['elements'][0].content if dict['elements'] else ''
            })
        
        return messages

    def answer(self, history):
        messages = self.read_history(history)
        
        stream = self.client.chat.completions.create(model=self.gpt_ver, messages=messages, stream=True)

        return stream
    
    def check_answer(self, history): 
        messages = self.read_history(history)
        
        last_prompt = messages.pop()
        last_prompt['content'] = 'This is a question from this game program framework, for this question please only answer me yes or no in all lower format to keep this program working in a correct way. Now, is the user guessing to the final situation correct? The user may guessed incorrect answer before, so please only focus on the following user answer. If user is asking question just for gathering information or user guess the situation about half or more wrong, please only say no. Only if user guess the entire situation mostly correct please only say yes. Do not include any punctuation, and in all lower case. The user guesses is as following: ' + last_prompt['content']
        messages.append(last_prompt)

        gpt_return = self.client.chat.completions.create(model=self.gpt_ver, messages=messages)

        return gpt_return.choices[0].message.content == 'yes'
    
    def generate_questions(self, history, question, vs_mode=False): 
        pre_messages = self.read_history(history)
        pre_text = ''

        for message in pre_messages: 
            if message['role'] != 'system':
                pre_text = pre_text + 'role: ' + message['role'] + 'content: ' + message['content'] + '\n'
        
        messages = [{"role": "system", "content": "You are now act as an expert player of the situation puzzle, now you get a chance to ask yes or no question that helps you to solve puzzle to the game host. Here is the Question of the situation puzzle: \n" + question + "\n Here is the chat history (If there is no history, feel free to start first question): \n " + pre_text + ("Now, if you think you are ready to guess, please strictly follow this format \'I guess: [input your guess here]\'. Please give very detailed explanation. Else if you think you still need more information, please" if vs_mode else "") + "generate yes or no questions exactly one you need to ask the game host, please must not generate others more ask question unless you are ready to guess. You don't need to say continue to ask questions, just ask directly"}]

        gpt_return = self.client.chat.completions.create(model=self.gpt_ver, messages=messages)
        
        questions = []
        questions.append(gpt_return.choices[0].message.content)

        if vs_mode: 
            return questions[0]
        else: 
            for _ in range(2):
                gpt_return = self.client.chat.completions.create(model=self.gpt_ver, messages=messages)
                questions.append(gpt_return.choices[0].message.content)
            
            return questions
        
    def feedback(self, history): 
        pre_messages = self.read_history(history)
        pre_text = ''

        for message in pre_messages: 
            pre_text = pre_text + 'role: ' + message['role'] + 'content: ' + message['content'] + '\n'
        
        messages = [{"role": "system", "content": "You are now act as an expert player of the situation puzzle. Here is a log of a player playing a situation puzzle with a llm situation puzzle host" + pre_text + "Now, do you have any suggestions would like to provide to this player"}]

        gpt_return = self.client.chat.completions.create(model=self.gpt_ver, messages=messages)

        return gpt_return.choices[0].message.content
        
        

    
class Dalle: 

    def __init__(self, style='colored comic book'): 
        self.client = OpenAI(api_key=st.secrets['GOOGLE_API_KEY'])
        self.style = style
    
    def gen_image(self, answer): 
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=f"I'm designing a game program for situation puzzle. You are a professional illustrator. I'm now going to give you an answer of situation puzzle. Please generate the answer to provide to player in a {self.style} format. Do not put words on image since GenAI would not generate words correctly, only punctuation can be presented if necessary. Here is the answer of situation puzzle: {answer}",
            n=1,
            size="1024x1024", 
            quality="standard"
        )

        return response.data[0].url


class GeminiText: 

    def __init__(self, init_prompt): 
        self.init_prompt = init_prompt
        load_dotenv(dotenv_path='api_key.env')
        genai.configure(api_key=os.getenv('API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')
    
    def read_history(self, history): 
        messages = []
        if len(history) > 0:
            messages.append({"role": "user", "parts": [self.init_prompt + history[0]['elements'][0].content if history[0]['elements'] else '']})

        for i in range(len(history)): 
            if i > 0:
                messages.append({
                    'role': 'model' if history[i]['role'] == 'assistant' else 'user', 
                    'parts': [history[i]['elements'][0].content if history[i]['elements'] else '']
                })
        
        return messages

    def answer(self, history):
        messages = self.read_history(history)
        
        stream = self.model.generate_content(messages, stream=True)

        return stream
    
    def check_answer(self, history): 
        messages = self.read_history(history)
        
        last_prompt = messages.pop()
        last_prompt['parts'] = ['This is a question from this game program framework, for this question please only answer me yes or no in all lower format to keep this program working in a correct way. Now, is the user guessing to the final situation correct? The user may guessed incorrect answer before, so please only focus on the following user answer. If user is asking question just for gathering information or user guess the situation about half or more wrong, please only say no. Only if user guess the entire situation mostly correct please only say yes. Do not include any punctuation, and in all lower case. The user guesses is as following: ' + last_prompt['parts'][0]]
        messages.append(last_prompt)

        gpt_return = self.model.generate_content(messages)

        return gpt_return.text == 'yes'

    def generate_questions(self, history, question, vs_mode=False): 
        pre_messages = self.read_history(history)
        pre_text = ''
        
        for i in range(len(pre_messages)): 
            if i > 0:
                pre_text = pre_text + 'role: ' + pre_messages[i]['role'] + 'parts: ' + pre_messages[i]['parts'][0] + '\n'
        
        messages = [{"role": "user", "parts": "You are now act as an expert player of the situation puzzle, now you get a chance to ask yes or no question that helps you to solve puzzle to the game host. Here is the Question of the situation puzzle: \n" + question + "\n Here is the chat history (If there is no history, feel free to start first question): \n " + pre_text + ("Now, if you think you are ready to guess, please strictly follow this format \'I guess: [input your guess here]\'. Please also explain why. Else if you think you still need more information or keep guessing wrong, please" if vs_mode else "") + "generate yes or no questions exactly one you need to ask the game host, please must not generate others more ask question unless you are ready to guess. You don't need to say continue to ask questions, just ask directly"}]

        gpt_return = self.model.generate_content(messages).text
        
        questions = []
        questions.append(gpt_return)

        if vs_mode: 
            return questions[0]
        else: 
            for _ in range(2):
                gpt_return = self.model.generate_content(messages).text
                questions.append(gpt_return)
            
            return questions
    
    def feedback(self, history): 
        pre_messages = self.read_history(history)
        pre_text = ''

        for message in pre_messages: 
            pre_text = pre_text + 'role: ' + message['role'] + 'parts: ' + message['parts'][0] + '\n'
        
        messages = [{"role": "system", "content": "You are now act as an expert player of the situation puzzle. Here is a log of a player playing a situation puzzle with a llm situation puzzle host" + pre_text + "Now, do you have any suggestions would like to provide to this player"}]

        gpt_return = self.model.generate_content(messages).text

        return gpt_return
        