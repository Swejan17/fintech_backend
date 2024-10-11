import os
from dotenv import load_dotenv
# from openai import OpenAI
from pydub import AudioSegment
from langchain_openai import OpenAI
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.aimlapi.com/",
)

def get_transcription(file_path):
    audio_file= open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    return transcription

def segment_audio(filepath):
    name_of_file = filepath.split(".")[0] 
    song = AudioSegment.from_file(filepath)

    duration = len(song)
    segements = duration//(1000*60)
    print(segements,"  ",duration)
    if segements > 0:
        for i in range(0,segements):

            start_time = i*1000*60
            end_time = (i+1)*1000*60
            segment = song[start_time:end_time]
            segment.export(f"{name_of_file}_segment_{i}.mp3", format="mp3")
        segment = song[segements*1000*60:]
        segment.export(f"{name_of_file}_segment_{segements}.mp3", format="mp3")
    else:
        segment = song
        segment.export(f"{name_of_file}_segment_0.mp3", format="mp3")
    return segements

def get_transcription_from_segmented_audio(file_path,segments):
    for i in range(0,segments+1):
        audio_file= open(f"{file_path}_segment_{i}.mp3", "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        open(f"transcribed/{file_path}_segment_{i}.txt","a").write(transcription)
    return transcription



# user_content = """
# how many Rs are there in the word strawberry
# think step by step
# """



# chat_completion = client.chat.completions.create(
#     model="o1-mini",

#     messages=[
#         {"role": "user", "content": user_content},
#     ],
#     max_tokens=2000,
# )

# response = chat_completion.choices[0].message.content
# print("Response:\n", response)