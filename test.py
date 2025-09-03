import os
import moviepy.editor as mp
from moviepy.editor import TextClip, CompositeVideoClip
import speech_recognition as sr
from moviepy.config import change_settings
from deep_translator import GoogleTranslator   # ✅ translation library

# ===== Windows & ImageMagick for TextClip =====
change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
})

# ---------- Globals ----------
input_video = "lalasa_telugu.mp4"      # <--- Replace with your video file
temp_audio_export = "temp_audio.wav"
output_with_subtitles = "video_with_subtitles.mp4"

translator = GoogleTranslator(source="auto", target="en")   # auto-detect → English

# ---------- Convert audio (from video) to text with translation ----------
def convert_video_audio_to_text(video_path, chunk_seconds=20):
    recognizer = sr.Recognizer()
    video = mp.VideoFileClip(video_path)

    # Export audio as PCM WAV
    video.audio.write_audiofile(
        temp_audio_export,
        fps=16000,
        nbytes=2,
        codec='pcm_s16le',
        ffmpeg_params=["-ac", "1"],  # mono
        verbose=False,
        logger=None
    )

    total_duration = video.audio.duration or 0.0
    print(f"[INFO] Audio duration: {total_duration:.2f}s")

    translated_texts = []
    try:
        with sr.AudioFile(temp_audio_export) as source:
            processed = 0.0
            while processed < total_duration - 1e-3:
                remaining = total_duration - processed
                seg = min(chunk_seconds, remaining)
                audio_data = recognizer.record(source, duration=seg)
                processed += seg

                if not audio_data.frame_data:
                    break
                try:
                    # Auto-detect spoken language
                    piece = recognizer.recognize_google(audio_data)
                    print(f"[SR] Recognized (raw): {piece}")

                    # Translate recognized text → English
                    translated = translator.translate(piece)
                    translated_texts.append(translated)
                    print(f"[TR] Translated → {translated}")

                except sr.UnknownValueError:
                    print("[SR] Chunk not understood; skipping.")
                except sr.RequestError as e:
                    print(f"[SR] API error: {e}; stopping.")
                    break
    finally:
        if os.path.exists(temp_audio_export):
            os.remove(temp_audio_export)

    text = " ".join(translated_texts).strip()
    print(f"[OK] Final translated text length: {len(text)}")
    return text

# ---------- Create subtitle clips ----------
def create_subtitle_clips(text, video_duration, frame_w=640):
    words = text.split()
    if not words:
        return []

    chunk_size = 6  # words per subtitle
    subtitle_chunks = [words[i:i+chunk_size] for i in range(0, len(words), chunk_size)]

    clip_duration = max(video_duration / len(subtitle_chunks), 0.5)
    start_time = 0.0

    subtitle_clips = []
    for chunk in subtitle_chunks:
        subtitle_text = " ".join(chunk)
        try:
            txt_clip = TextClip(
                subtitle_text,
                fontsize=32,
                color='white',
                size=(int(frame_w * 0.9), 120),
                method='caption'
            )
        except Exception:
            txt_clip = TextClip(
                subtitle_text,
                fontsize=32,
                color='white',
                font='DejaVu-Sans',
                size=(int(frame_w * 0.9), 120),
                method='caption'
            )
        txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(clip_duration).set_start(start_time)
        subtitle_clips.append(txt_clip)
        start_time += clip_duration
    return subtitle_clips

# ---------- Add subtitles to video ----------
def add_subtitles_to_video(video_path, subtitle_clips):
    if not subtitle_clips:
        print("[INFO] No subtitles generated.")
        return
    video = mp.VideoFileClip(video_path)
    final_video = CompositeVideoClip([video] + subtitle_clips)
    final_video.write_videofile(output_with_subtitles, codec="libx264", audio_codec="aac", threads=4)
    print(f"[OK] Final video with subtitles saved to {output_with_subtitles}")

# ---------- Main ----------
def main():
    text = convert_video_audio_to_text(input_video, chunk_seconds=20)

    if text:
        with mp.VideoFileClip(input_video) as vid:
            subtitle_clips = create_subtitle_clips(text, vid.duration, frame_w=vid.w)
        add_subtitles_to_video(input_video, subtitle_clips)
    else:
        print("[INFO] No text recognized, skipping subtitle creation.")

if __name__ == "__main__":
    main()




