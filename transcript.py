from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
)


def extract_video_id(url):
    """
    Extract the YouTube video ID from a YouTube URL.
    """

    parsed_url = urlparse(url)

    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]

    if parsed_url.hostname in ("www.youtube.com", "youtube.com"):
        return parse_qs(parsed_url.query)["v"][0]

    raise ValueError("Invalid YouTube URL.")


def get_transcript(url):
    """
    Retrieve the transcript for a YouTube video.
    """

    video_id = extract_video_id(url)

    try:
        transcript = YouTubeTranscriptApi().fetch(
            video_id,
            languages=["hi", "en"],
        )

        return " ".join(
            item.text
            for item in transcript
        )

    except TranscriptsDisabled:
        raise ValueError(
            "Transcript unavailable: subtitles are disabled for this video."
        )

    except NoTranscriptFound:
        raise ValueError(
            "Transcript unavailable: no Hindi or English transcript "
            "was found for this video."
        )