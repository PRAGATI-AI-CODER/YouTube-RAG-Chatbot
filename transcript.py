from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
from urllib.parse import urlparse, parse_qs


def extract_video_id(url):
    parsed_url = urlparse(url)

    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]

    if parsed_url.hostname in ("www.youtube.com", "youtube.com"):
        return parse_qs(parsed_url.query)["v"][0]

    raise ValueError("Invalid YouTube URL")


def get_transcript(url):
    video_id = extract_video_id(url)

    try:
        transcript = YouTubeTranscriptApi().fetch(
            video_id,
            languages=["hi", "en"]
        )

        return " ".join(item.text for item in transcript)

    except NoTranscriptFound:
        print("No supported transcript found.")
        return None


if __name__ == "__main__":
    url = input("Enter YouTube URL: ")

    transcript = get_transcript(url)

    if transcript:
        print("\nTranscript Preview:\n")
        print(transcript[:1000])