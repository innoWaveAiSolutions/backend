import os, json

def create_assistant(client):
    assistant_file_path = 'assistant.json'

    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, 'r') as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data['assistant_id']
            print("Loaded existing assistant ID.")
    else:
        # Path to the directory of the current file (functions.py)
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Path to the knowledge.docx file
        knowledge_path = os.path.join(dir_path, "knowledge.docx")
        file = client.files.create(file=open(knowledge_path, "rb"),
                                purpose='assistants')

        assistant = client.beta.assistants.create(instructions="""
            This is a bot to answer questions about InnoWave Ai Solutions
            """,
                                                model="gpt-4-1106-preview",
                                                tools=[{
                                                    "type": "retrieval"
                                                }],
                                                file_ids=[file.id])

        with open(assistant_file_path, 'w') as file:
            json.dump({'assistant_id': assistant.id}, file)
            print("Created a new assistant and saved the ID.")

        assistant_id = assistant.id

    return assistant_id