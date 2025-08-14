"""
AIHandler is a utility class that is used to interact with OpenAI by managing prompts, responses, and conversation context.

Key features include:
- Initializing an OpenAI client with customizable settings.
- Building and maintaining conversation history between the user and assistant.
- Extracting and parsing code snippets from AI responses.
- Saving and loading message context and arbitrary data to and from files.
"""


from openai import OpenAI

class AIHandler():

    def __init__(self, key=None, role=None, print_message=None, model="gpt-3.5-turbo-16k", **kwargs):
        super().__init__(**kwargs)
        self.client = OpenAI(api_key=key)
        self.role = role
        self.messages_send = []
        self.messages_received = []
        self.messages_received_parsed_code = []
        self.errors = []
        self.print_message = print_message
        self.model = model


    def save_context(self, context, path):
        text2save = ""
        for idx in range(len(context)):
            element = context[idx]
            text2save = text2save + "role - " + element["role"] + "\n"
            text2save = text2save + "content:\n"
            content = element["content"].split("\n")
            for index in range(len(content)):
                line = content[index]
                text2save = text2save + line + "\n"

            text2save = text2save + "\n\n=================================================\n\n"

        with open(path, 'w') as file:
            file.write(text2save)

    def create_context(self):
        context = [{"role": "system", "content": self.role}]
        for idx in range(len(self.messages_send)):
            context.append({"role": "user", "content": self.messages_send[idx]})
            context.append({"role": "assistant", "content": self.messages_received[idx]})

        return context


    def _parse_message(self, message):
        if self.print_message:
            print("------ start message")
            print(message)
            print("------   end message")

        split_message = message.split("\n")

        code = False
        result = []
        tmp = []
        for line in split_message:
            if line.startswith("```") and len(tmp) != 0:
                result.append("\n".join(tmp))
                tmp = []
                break

            if code:
                tmp.append(line)

            if line.startswith("```"):
                code = True
                tmp = []

        if len(result) == 0:
            return message
        return "\n".join(result)

    def save2file(self, data, path):
        file = open(path, "w")
        file.writelines(data)
        file.close()

    def readFromFile(self, path):
        file = open(path, 'r')
        lines = file.readlines()
        return "".join(lines)