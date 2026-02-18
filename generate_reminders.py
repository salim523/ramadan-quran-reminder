#!/usr/bin/env python3
"""
Generate Ramadan Quran reminder messages with daily progress tracking.
Fetches video links from YouTube playlists using the YouTube Data API.
"""

import os
import json
from dotenv import load_dotenv
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs

# Load environment variables
load_dotenv(dotenv_path=".env.local")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in .env.local file")

# Initialize YouTube API client
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def extract_playlist_id(playlist_url):
    """Extract playlist ID from YouTube playlist URL."""
    parsed_url = urlparse(playlist_url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get("list", [None])[0]


def get_daily_motivation(day):
    """Get a unique motivational message for each day of Ramadan."""
    motivations = [
        "Make it count! 💪",  # Day 1
        "Every verse connects you to divine wisdom. 📖",  # Day 2
        "You're building a beautiful habit! 🌟",  # Day 3
        "Feel the peace of Quranic words. ☮️",  # Day 4
        "Progress is progress, no matter how small! ✨",  # Day 5
        "Your dedication will transform your soul. 🕯️",  # Day 6
        "Three hours in, three more to go! 🎯",  # Day 7
        "Consistency unlocks spiritual victories! 🏆",  # Day 8
        "Listen with your heart, not just your ears. ❤️",  # Day 9
        "One-third complete! You're unstoppable! 🚀",  # Day 10
        "Let Allah's words guide your path. 🧭",  # Day 11
        "Reflect on the blessings around you. 🙏",  # Day 12
        "Every day brings new wisdom. 💎",  # Day 13
        "You're halfway through this beautiful journey! 🌙",  # Day 14
        "Full moon energy – shine bright today! ✨",  # Day 15
        "Your family is proud of your commitment! 👨‍👩‍👧‍👦",  # Day 16
        "Ramadan is about inner transformation. 🦋",  # Day 17
        "Stay focused on the final stretch ahead! 🎯",  # Day 18
        "Every verse plants seeds of faith. 🌱",  # Day 19
        "Two-thirds done! Feel the momentum! ⚡",  # Day 20
        "You're closer to the finish line than the start! 🏁",  # Day 21
        "Let your determination inspire others. 💫",  # Day 22
        "Spirituality blooms through daily practice. 🌺",  # Day 23
        "Just one week left – give it your all! 💯",  # Day 24
        "These final days are the most precious! 💝",  # Day 25
        "You've proven you can do anything! 🔥",  # Day 26
        "The reward awaits those who persist. 👑",  # Day 27
        "Three days left – finish strong! 💪",  # Day 28
        "Tomorrow is the last day. Soak in every moment! 🌅",  # Day 29
        "🎉 Last day! Celebrate your achievement! You did it! 🏅",  # Day 30
    ]

    # Return the motivation for the current day (day is 1-indexed)
    return motivations[day - 1] if day <= len(motivations) else "Make it count! 💪"


def get_playlist_videos(playlist_id, max_results=30):
    """Fetch all video links from a playlist."""
    videos = []
    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id,
        maxResults=min(max_results, 50),
        pageToken=None,
    )

    while request and len(videos) < max_results:
        response = request.execute()

        for item in response.get("items", []):
            video_id = item["contentDetails"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append(video_url)
            if len(videos) >= max_results:
                break

        # Get next page token for pagination
        next_page_token = response.get("nextPageToken")
        if next_page_token and len(videos) < max_results:
            request = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=playlist_id,
                maxResults=min(max_results - len(videos), 50),
                pageToken=next_page_token,
            )
        else:
            break

    return videos


def get_moon_phase(day, total_days=30):
    """
    Calculate moon phase for a given day.
    Lunar cycle is ~29.5 days, so we map 30 days to a complete lunar cycle.
    Returns the appropriate moon emoji for that day.
    """
    # 8 phases in a lunar cycle
    moon_phases = [
        "🌑",  # New Moon (day 0-3)
        "🌒",  # Waxing Crescent (day 4-7)
        "🌓",  # First Quarter (day 8-11)
        "🌔",  # Waxing Gibbous (day 12-15)
        "🌕",  # Full Moon (day 16-19)
        "🌖",  # Waning Gibbous (day 20-23)
        "🌗",  # Last Quarter (day 24-26)
        "🌘",  # Waning Crescent (day 27-29)
    ]

    # Map day to phase index (0-7)
    phase_index = int((day / total_days) * 8) % 8
    return moon_phases[phase_index]


def create_progress_bar(current_day, total_days=30):
    """Generate a moon phase progress bar with completed and remaining days."""
    # Show actual moon phases for completed days
    moon_bar = ""
    for day in range(1, current_day + 1):
        moon_bar += get_moon_phase(day, total_days)

    # Fill remaining days with new moon (empty placeholder)
    remaining = total_days - current_day
    moon_bar += "🌑" * remaining

    return moon_bar


def generate_reminders(playlists_file, template_file, output_file):
    """Generate reminders for all 30 days and write to output file."""

    # Load playlist links
    with open(playlists_file, "r") as f:
        playlists = json.load(f)

    # Load template
    with open(template_file, "r") as f:
        template = f.read()

    # Fetch videos from each playlist
    print("Fetching playlists from YouTube...")
    playlist_videos = {}

    for playlist_name, playlist_url in playlists.items():
        print(f"  Fetching {playlist_name}...")
        playlist_id = extract_playlist_id(playlist_url)
        if not playlist_id:
            print(f"    ERROR: Could not extract playlist ID from {playlist_url}")
            continue

        videos = get_playlist_videos(playlist_id, max_results=30)
        playlist_videos[playlist_name] = videos
        print(f"    Retrieved {len(videos)} videos")

    # Verify we have 30 videos in each playlist
    for name, videos in playlist_videos.items():
        if len(videos) < 30:
            print(f"WARNING: {name} has only {len(videos)} videos (expected 30)")

    # Generate reminders for each day
    print("\nGenerating reminders for 30 days...")
    all_reminders = []

    for day in range(1, 31):
        percentage = int((day / 30) * 100)
        progress_bar = create_progress_bar(day, 30)
        motivation = get_daily_motivation(day)

        # Get the video for this day from each playlist (0-indexed)
        urdu_only_link = playlist_videos.get("urdu_only_link", [""])[day - 1]
        arabic_english_link = playlist_videos.get("arabic_english_link", [""])[day - 1]
        arabic_urdu_link = playlist_videos.get("arabic_urdu_link", [""])[day - 1]

        # Replace placeholders in template
        reminder = template.replace("[PERCENTAGE]", str(percentage))
        reminder = reminder.replace("[Percentage]", str(percentage))
        reminder = reminder.replace("[N]", str(day))
        reminder = reminder.replace("[MOTIVATION]", motivation)
        reminder = reminder.replace("[urdu_only_link]", urdu_only_link)
        reminder = reminder.replace("[arabic_english_link]", arabic_english_link)
        reminder = reminder.replace("[arabic_urdu_link]", arabic_urdu_link)
        reminder = reminder.replace("[MOON_PHASE]", progress_bar)

        all_reminders.append(reminder)

    # Write all reminders to output file
    print(f"Writing reminders to {output_file}...")
    with open(output_file, "w") as f:
        f.write("\n".join(all_reminders))

    print(f"✓ Successfully generated reminders for all 30 days!")
    print(f"✓ Output saved to {output_file}")


if __name__ == "__main__":
    generate_reminders(
        playlists_file="playlists.json",
        template_file="template.txt",
        output_file="reminders.txt",
    )
