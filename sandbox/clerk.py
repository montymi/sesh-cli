import ollama 
import re
from datetime import datetime
from pprint import pprint
#import json
import speech_recognition as sr
import pyttsx3
import argparse
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import time

recognizer = sr.Recognizer()

SALUTES = ["exit", "quit", "q", "bye", "goodbye"]
HABITS = ["\nPlease add tags to categorize the above text. The tags should be formatted like [tag: <tag-name>] and should be placed at the bottom of the page.", "\nPlease add one confidence score to the end of your answer in the format [Confidence: 0-99] with no other symbols."]
WELCOME = "Welcome to SESH! This is the Clerk, here to assist with your private virtual library."

class Librarian:
    def __init__(self):
        pass

    def save(self, data: list):
        with open('log.txt', 'a') as file:
            for item in data:
                file.write(str(item) + '\n')

    def load(self, file):
        if file is None:
            with open('log.txt', 'r') as file:
                lines = file.readlines()
            return lines

    def call(self, prompt, tags):
        print(f"Librarian received call for:\n1. Prompt: {prompt}\n2. Tags: {tags}")
        return 1

    def find(self, id):
        print(f"Librarian received find request for document id: {id}")
        return f"Results for document {id}"

class Clerk:
    _instance = None  # Class variable to store the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.model = kwargs.get('model', 'mistral')
            cls._instance.clock_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cls._instance._logs = []
            cls._instance.librarian = Librarian()
        print(WELCOME)
        return cls._instance
    
    def __str__(self):
        clerk_string = f"        (o_  Current Model: {self.model}\n  c_  \\\\\_\  Clock-In Time: {self.clock_in}\n\\\)   <____) Conversations: {len(self._logs)//2}\n"
        return clerk_string
    
    def ask(self, prompt):
        prompt = self._prompt_flagging_(prompt)
        response = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': prompt}])
        message = self._response_flagging_(response, prompt) 
        if message is None: return
        else: 
            print("<<<", message)
            return response['message']

    def chat(self):
        print(self)
        while True:
            prompt = input(">>> ")
            flagged = self._prompt_flagging_(prompt)
            if flagged is None: break
            else: new_prompt = flagged
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._logs.append({'time': time, 'role': 'user', 'content': new_prompt})

            response = ollama.chat(model=self.model, messages=self._logs)
            message = self._response_flagging_(response, prompt) 
            if message is None: return
            else: print(f"<<< {message}")


    def _prompt_flagging_(self, prompt):
        if prompt.lower() in SALUTES:
                print("Goodbye!")
                return None
        elif prompt.lower() == "self":
            print(self)
            return "Tell me about yourself, what can you do for me? Short response."
        for habit in HABITS:
            prompt += habit
        return prompt
    
    def _response_flagging_(self, response, prompt):
        done: bool = response['done']
        total_duration: int = response['total_duration']
        load_duration: int = response['load_duration']
        prompt_eval_duration: int = response['prompt_eval_duration']
        eval_count: int = response['eval_count']
        eval_duration: int = response['eval_duration']
        if done is not True:
            print("Response interrupted, rerunning...")
            return self.ask(prompt)
        tags = re.findall(r'\[(?:tag|tags):\s*([^[\]]+)\]', response['message']['content'], flags=re.IGNORECASE)
        cleaned = set()
        for tag in tags:
            if "," in tag:
                cleaned.update(tag.strip() for tag in tag.split(","))
            else:
                cleaned.add(tag.strip())
        response['message']['tags'] = list(cleaned) if cleaned else None
        confidence_match = re.search(r'\[Confidence: (\d{1,2})\]', response['message']['content'])
        if confidence_match:
            confidence: int = int(confidence_match.group(1))
            if confidence < 75:
                print("Sorry for the delay... I have to talk to the librarian to give a more confident answer.")
                code = input("Server Code: ")
                username = input("Username: ")
                if not self.librarian.login(code, username): print("Invalid login credentials")
                docs = self.librarian.call(prompt, cleaned)
                if docs > 0:
                    return self.librarian.find(docs)
        self._logs.append(response['message'])
        return response['message']['content']
    
    @property
    def logs(self):
        # usage: Clerk.logs
        for log in self._logs:
            pprint(log)
        if input("Save logs (y/n): ") == "y":
            self.librarian.save(self._logs)
    
    def load(self, data=None):
        if input("Load Clerk logs (y/n): ") == "y":
            lines = self.librarian.load(data)
            log_prompt = ""
            for line in lines:
                log_prompt += line
            data = "Could you remember these conversations for me? List the topics discussed." + str(log_prompt)
            self.ask(data)


class Recognize:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def record_audio(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
        return audio

    def recognize_speech(self, audio):
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            text = ""
        except sr.RequestError:
            print("Sorry, there was an error processing your request.")
            text = ""
        return text

    def speak_text(self, command):
        self.engine.say(command) 
        self.engine.runAndWait()


class Conversation:
    def __init__(self, clerk):

        ## Initialization
        self.clerk = clerk
        self.window = tk.Tk()

        ##Protocols
        self.window.protocol("WM_DELETE_WINDOW", self.end_program)

        ##Visuals
        self.window.title("Clerk Communicator")

        self.notebook = ttk.Notebook(self.window)
        self.notebook.grid(row=0, column=0, columnspan=2, sticky='nsew')

        self.conversation_area = scrolledtext.ScrolledText(self.notebook, bg='light yellow', wrap=tk.WORD)
        self.conversation_area.grid(row=1, column=0, columnspan=2, sticky='nsew')
        self.conversation_area.config(state='disabled')
        self.conversation_area.tag_config('user', justify='right')
        self.conversation_area.tag_config('waiting', justify='center')

        self.user_input = tk.Entry(self.window, bg='light grey')
        self.user_input.grid(row=2, column=0, sticky='ew')
        self.user_input.bind('<Return>', lambda event: self.ask_ai())

        self.send_button = tk.Button(self.window, text="SEND", command=self.send_message, bg='light green')
        self.send_button.grid(row=2, column=1)

        self.conversation_area.tag_config("user", foreground="blue")
        self.conversation_area.tag_config("clerk", foreground="red")

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)


    def ask_ai(self):
        user_message = self.send_message()
        self.receive_message(user_message)


    def send_message(self):
        user_message = self.user_input.get()
        if user_message:
            self.conversation_area.config(state='normal')
            self.conversation_area.insert(tk.END, "User:\n"+ user_message + '\n\n', 'user')
            self.conversation_area.insert(tk.END, "Awaiting response...\n\n", 'waiting')
            self.conversation_area.update_idletasks()
        
        return user_message

    def receive_message(self, user_message):

        start_time = time.time()

        clerk_response = self.clerk.ask(user_message)
        response_content = clerk_response['content'] if 'content' in clerk_response else 'No response'

        end_time = time.time()

        elapsed_time = end_time - start_time

        self.conversation_area.insert(tk.END, '\n' + "CLERK:\n" + response_content + '\nTime for response: ' + str(round(elapsed_time, 1)) + 'seconds\n\n', "clerk")
        self.conversation_area.config(state='disabled')

        self.user_input.delete(0, tk.END)


    def run(self):
        self.window.mainloop()

    def end_program(self):
        self.window.quit()
        self.window.destroy()


def parse_args():
    parser = argparse.ArgumentParser(description="Clerk: A conversational AI assistant for your private virtual library.")
    parser.add_argument("--tts", action='store_true', help='Enable text to speech')
    args = parser.parse_args()
    print(args)
    return args

# Start the conversation

def main():
    args = parse_args()
    init_clerk = Clerk()

    if args.tts:
        recognizer = Recognize()
        audio = recognizer.record_audio()
        text = recognizer.recognize_speech(audio)
        
        response = init_clerk.ask(text)

        recognizer.speak_text(response['content'])

    else:
        conversation = Conversation(init_clerk)
        conversation.run()
        response = init_clerk.chat()

    if input("Show logs (y/n): ") == "y": 
        init_clerk.logs


if __name__ == "__main__":
    main()
    

