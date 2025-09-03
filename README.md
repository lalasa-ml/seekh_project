# seekh_project

# 🎬 Auto Subtitle Generator (Multi-language → English)

This project takes any video (with spoken audio in Hindi, Telugu, or other supported languages) and automatically generates **English subtitles**.  

It uses:
- **SpeechRecognition** (`recognize_google`) to convert speech → text.  
- **deep-translator (GoogleTranslator)** to translate recognized text → English.  
- **MoviePy** to overlay the subtitles onto the video.  

---

## 🚀 Features
- Works with **any spoken language** (Hindi, Telugu, Tamil, etc.) → subtitles in **English**.  
- Splits audio into chunks for better accuracy.  
- Subtitles are auto-timed and added to the bottom of the video.  
- Final video is exported with hard-coded English subtitles.





## 🛠️ Tech Stack

Python 3.9+

OpenCV – For video recording

PyAudio – For audio recording

MoviePy – For merging audio/video and rendering subtitles

SpeechRecognition – For speech-to-text conversion

Googletrans – (Optional) for future translation support

ImageMagick – For rendering text (needed by MoviePy)


## ⚠️ On Windows, also install ImageMagick and update its path in the script:

change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
})



## 🔮 Future Improvements

🌐 Support for dialects and accents to improve transcription accuracy.

⏱ Make subtitle generation dynamic and real-time for live streams.

🌍 Enable subtitles in multiple output languages (not just English).

🎛 User controls for font style, size, and subtitle placement.
