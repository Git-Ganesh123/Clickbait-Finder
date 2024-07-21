from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import requests
import json
from flask import Flask, request
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# Input YouTube video URL
video_url = input("Enter the YouTube video URL: ")

# API key
GEMINI_API_KEY = "key"
genai.configure(api_key=GEMINI_API_KEY)

# Generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Get the video title
r = requests.get(video_url)
soup = BeautifulSoup(r.text, features="html.parser")
title_tag = soup.find("title")
title = title_tag.get_text() if title_tag else "Unknown Title"
print(f"Video Title: {title}")


def extract_id(url):
    if "youtube.com/watch?v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("/")[-1]
    return None


video_id = extract_id(video_url)

if video_id:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([item['text'] for item in transcript])
        print(f"Transcript: {transcript_text}")

        response = model.generate_content(
            f"Analyze the similarity between the following title and transcript:\n\nTitle: {title}\n\nTranscript: {transcript_text}\n\nProvide a similarity percentage in numerical format with a % symbol from 1-100, with 100 being the most similar and 1 being the least"
        )

        response_text = response.text if hasattr(response, 'text') else str(response)

        print(f"GPT Response: {response_text}")

        similarity_percentage = None
        for line in response_text.split('\n'):
            if "%**" in line:
                try:
                    similarity_percentage = float(line.split('%')[0].split()[-1])
                    break
                except ValueError:
                    continue



        match = re.search(r'(\d+)%', response_text)

        if match:
            percentage = int(match.group(1))
            print(f"Clickbait Percentage: {percentage}% accurate")
        else:
            print("Percentage not found.")

    except Exception as e:
        print(f"Error fetching transcript: {e}")
else:
    print("Invalid YouTube URL.")

if __name__ == '__main__':
    app.run
