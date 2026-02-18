# Ramadan Quran Reminder Generator

A Python program that generates personalized daily Ramadan reminders with Quran listening links and progress tracking. Fetches video links from YouTube playlists using the YouTube Data API and creates 30 customized reminder messages.

## Features

- 🎬 **Fetches YouTube Playlist Videos**: Automatically retrieves all 30 videos from each Quran playlist
- 🌙 **Moon Phase Progress Tracker**: Displays daily progress using lunar phases that cycle through a complete lunar month
- 📊 **Progress Tracking**: Shows daily progress with percentage completion
- 🌐 **Multi-Language Support**: Generates reminders for three playlist variants:
  - Urdu only
  - Arabic/English
  - Arabic and Urdu
- 📝 **Template-Based Generation**: Customizable reminder messages using template substitution
- 📤 **Batch Output**: Generates all 30 reminders in a single organized file

## Project Structure

```
ramadan-quran-reminder/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (API key)
├── generate_reminders.py     # Main script
├── template.txt              # Reminder message template
├── playlists.json            # YouTube playlist URLs
└── reminders.txt             # Generated output file
```

## Prerequisites

- Python 3.7 or higher
- YouTube Data API key (Get it from [Google Cloud Console](https://console.cloud.google.com/))
- Internet connection (to fetch from YouTube API)

## Installation

1. **Clone or download this project** to your local machine

2. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your YouTube API key** in `.env`:
   ```
   YOUTUBE_API_KEY=your_api_key_here
   ```

## Configuration

### `.env` File

Store your YouTube API key:

```
YOUTUBE_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### `playlists.json`

Add your YouTube playlist URLs:

```json
{
  "urdu_only_link": "https://www.youtube.com/playlist?list=PLjMdlvowxr_0IZ13u1fEZM7XEycYvIFTe",
  "arabic_english_link": "https://www.youtube.com/playlist?list=PL8LzbcfKeLJcW2NmjwWdW24gASZfF5s_L",
  "arabic_urdu_link": "https://www.youtube.com/playlist?list=PL8LzbcfKeLJd-MH1t7QpFUP1ZykCtHhkJ"
}
```

### `template.txt`

Customize your reminder message. Available placeholders:

- `[Percentage]` - Completion percentage (0-100)
- `[N]` - Current day number (1-30)
- `[MOON_PHASE]` - Moon phase progress bar showing lunar phases (🌑→🌒→🌓→🌔→🌕→🌖→🌗→🌘)
- `[urdu_only_link]` - First video link from Urdu playlist
- `[arabic_english_link]` - First video link from Arabic/English playlist
- `[arabic_urdu_link]` - First video link from Arabic/Urdu playlist

Example template:

```
Ramadan Mubarak!

This Ramadan, we have 30 days to fast and reflect on our lives. We can take 30 minutes to listen to the Quran and understand its teachings. By listening to the link below, you will have completed [Percentage]% of the Quran.

Urdu only - [urdu_only_link]
Arabic/English - [arabic_english_link]
Arabic and Urdu - [arabic_urdu_link]

Progress (Day [N]/30):
[MOON_PHASE] [Percentage]%

Keep us in your prayers, and may Allah bless us all.
Ameen.
```

## Usage

Run the script:

```bash
python generate_reminders.py
```

The program will:

1. ✅ Load your API key from `.env`
2. ✅ Read playlist URLs from `playlists.json`
3. ✅ Load the template from `template.txt`
4. ✅ Fetch 30 videos from each YouTube playlist
5. ✅ Generate 30 customized reminder messages
6. ✅ Calculate progress for each day (percentage and progress bar)
7. ✅ Write all reminders to `reminders.txt`

### Output

The generated `reminders.txt` will contain reminders for all 30 days, each with:

- Day counter (Day X/30)
- Completion percentage
- Moon phase progress bar showing lunar progression through the 30 days
- Video links for each playlist variant
- Divider separating each day's reminder

Example output for Day 1:

```
Ramadan Mubarak!

This Ramadan, we have 30 days to fast and reflect...

Urdu only - https://www.youtube.com/watch?v=VIDEO_ID_1
Arabic/English - https://www.youtube.com/watch?v=VIDEO_ID_2
Arabic and Urdu - https://www.youtube.com/watch?v=VIDEO_ID_3

Progress (Day 1/30):
🌑                             3%

Keep us in your prayers, and may Allah bless us all.
Ameen.
```

Example output for Day 15 (halfway - shows Full Moon):

```
Progress (Day 15/30):
🌑🌑🌑🌒🌒🌒🌒🌓🌓🌓🌓🌔🌔🌔🌕  50%
```

Example output for Day 30 (complete cycle):

```
Progress (Day 30/30):
🌑🌑🌑🌒🌒🌒🌒🌓🌓🌓🌓🌔🌔🌔🌕🌕🌕🌕🌖🌖🌖🌖🌗🌗🌗🌗🌘🌘🌘🌑 100%
```

## Dependencies

- **google-api-python-client** (1.12.8) - YouTube Data API client
- **python-dotenv** (1.0.0) - Environment variable management

Install all dependencies:

```bash
pip install -r requirements.txt
```

## How It Works

1. **Playlist Fetching**: Extracts playlist IDs from YouTube URLs and fetches all 30 videos using the YouTube API
2. **Moon Phase Calculation**: Maps each day (1-30) to a lunar phase in an 8-phase lunar cycle:
   - Days 1-3: New Moon 🌑
   - Days 4-7: Waxing Crescent 🌒
   - Days 8-11: First Quarter 🌓
   - Days 12-15: Waxing Gibbous 🌔
   - Days 16-19: Full Moon 🌕
   - Days 20-23: Waning Gibbous 🌖
   - Days 24-27: Last Quarter 🌗
   - Days 28-30: Waning Crescent 🌘
3. **Progress Bar Generation**: Creates a moon phase progress bar that grows each day, showing which phases have passed
4. **Percentage Calculation**: Calculates completion percentage as `(day / 30) * 100`
5. **Template Generation**: Replaces all placeholders with actual data for each day
6. **Batch Output**: Writes all 30 reminders to a single file with separators

## Troubleshooting

### API Key Error

```
ValueError: YOUTUBE_API_KEY not found in .env file
```

**Solution**: Ensure your `.env` file contains `YOUTUBE_API_KEY=your_key_here`

### Playlist Not Found

```
ERROR: Could not extract playlist ID from [URL]
```

**Solution**: Verify your YouTube URLs are correct in `playlists.json`

### Insufficient Videos

```
WARNING: [playlist_name] has only X videos (expected 30)
```

**Solution**: Your playlist may have fewer than 30 videos. The script will use available videos.

## Getting a YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the YouTube Data API v3
4. Create an API key in Credentials
5. Copy the key to your `.env` file

## Notes

- Make sure each playlist has at least 30 videos
- The script respects YouTube API rate limits
- Video links are displayed in chronological order from each playlist
- Moon phase progress bar tracks the lunar cycle progression through the 30 days
- The moon phase starts at New Moon (🌑) and progresses through all 8 phases, completing the cycle by day 30
- Each day's reminder shows all moon phases up to that day (cumulative display)

## Future Enhancements

- Add scheduling to send reminders on specific times
- Email/SMS integration for automatic reminders
- Support for multiple languages in template
- Web interface for easy configuration
- Database storage for reminder history

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please refer to the inline code documentation or contact the maintainer.

---

**Ramadan Mubarak!** 🌙
