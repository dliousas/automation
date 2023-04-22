import os
import yt_dlp as youtube_dl
from pydub import AudioSegment

# Set the output directory for the cleaned audio files
output_dir = '/Users/demetriliousas/Library/CloudStorage/OneDrive-UniversityofMassachusetts/Music'

# Change the working directory to the tmp directory
os.chdir('tmp')
# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Create youtube-dl options dictionary
ydl_opts = {
    'format': 'bestaudio',
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


# Continuously prompt for video links until the user inputs ctrl+c
while True:
    try:
        # Get the YouTube video URL from the user
        url = input("Enter a YouTube video link: ")

        # Download the video to the tmp directory as an mp3 file
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # Set the audio path to the downloaded mp3 file
            audio_path = f"{info['title']}.mp3"
            print(f"Video downloaded to {audio_path}.")

        # Load the audio file and remove silence over 1 second
        audio = AudioSegment.from_file(audio_path, format="mp3")
        audio = audio.split_to_mono()[0]

        # Remove silence from the audio file
        audio = audio.strip_silence(silence_len=1000, silence_thresh=-40)
        print("Silence removed from audio file.")
        # Delete all tags on the audio file
        audio.export(audio_path, format="mp3", tags={})
        print("Tags removed from audio file.")

        # Export the cleaned audio file to the output directory
        title = os.path.splitext(os.path.basename(audio_path))[0]
        output_path = os.path.join(output_dir, f"{title}.mp3")
        audio.export(output_path, format="mp3")

        print(f"Audio file cleaned and stripped of silence and exported to {output_path}.")
        # Delete everything in the tmp directory
        for file in os.listdir():
            os.remove(file)

    except KeyboardInterrupt:
        # Exit the loop if the user inputs ctrl+c
        print("Exiting...")
        break
