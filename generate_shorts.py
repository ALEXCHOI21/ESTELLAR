import os
import sys
import io
import wave
import winreg
import time
import random
import subprocess
from dotenv import load_dotenv
from PIL import Image

# 1. Windows Registry-based PATH Refresh for dynamic FFmpeg detection
def refresh_path():
    print("[System] Refreshing system PATH from registry...")
    try:
        # User PATH
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
            user_path, _ = winreg.QueryValueEx(key, "Path")
        # Machine PATH
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment") as key:
            sys_path, _ = winreg.QueryValueEx(key, "Path")
        
        combined_path = f"{user_path};{sys_path}"
        os.environ["PATH"] = combined_path
        print("[System] PATH successfully updated at runtime!")
    except Exception as e:
        print(f"[System] Warning: Could not refresh PATH from registry: {e}")

# Call path refresh immediately
refresh_path()

# Load environments
load_dotenv()

# Verify Gemini API key
gemini_key = os.getenv("GEMINI_API_KEY")
if not gemini_key:
    print("[Error] GEMINI_API_KEY not found in environment. Please check your .env file.")
    sys.exit(1)

# Initialize Google GenAI Client
try:
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=gemini_key)
except ImportError:
    print("[Error] google-genai library is not installed. Please install it first.")
    sys.exit(1)

# Ensure temp directory exists
temp_dir = "temp_assets"
os.makedirs(temp_dir, exist_ok=True)

# 2. Define YouTube Shorts Scenes (AIDA model-based)
SCENES = [
    {
        "id": 1,
        "narrative": "아직도 흔하고 뻔한 커플링 브랜드만 고집하시나요?",
        "subtitle": "아직도 흔한 브랜드만\n고집하시나요?",
        "prompt": "Ultra high-end luxury diamond ring rotating slowly on a dark black velvet surface, warm champagne gold lighting, beautiful reflections, dramatic depth of field, photorealistic, 8k, product shot --ar 9:16",
        "voice": "Kore"
    },
    {
        "id": 2,
        "narrative": "국가공인 보석 감정사가 직접 원석을 고르고, 디자인 공모전 대상을 수상한 디자이너가 만듭니다.",
        "subtitle": "보석 감정사가 직접 고르고\n대상을 수상한 디렉터의 작품",
        "prompt": "An elegant female gemologist carefully inspecting a sparkling gemstone using a magnifying loupe, sketchbooks with jewelry designs on a mahogany desk, warm moody luxury studio lighting, cinematic, photorealistic --ar 9:16",
        "voice": "Kore"
    },
    {
        "id": 3,
        "narrative": "에스텔라의 베스트셀러, 샹달 반지. 손끝에서 뿜어져 나오는 차원이 다른 깊이감과 아우라.",
        "subtitle": "에스텔라 시그니처\n샹달 반지 컬렉션",
        "prompt": "Elegant close-up of a modern gold couple ring with beautiful textures worn on fingers, soft sunlight reflecting warm glow, luxury aesthetics, high fashion, photorealistic --ar 9:16",
        "voice": "Kore"
    },
    {
        "id": 4,
        "narrative": "당신의 가장 소중한 일상을 은하수처럼 영원히 빛내줄 단 하나의 예술적 조각.",
        "subtitle": "은하수처럼 영원히 빛내줄\n단 하나의 예술적 조각",
        "prompt": "A brilliant diamond necklace on a elegant female collarbone silhouette, dark background with subtle star-like sparkles, luxury jewelry commercial look, dreamlike atmosphere, cinematic --ar 9:16",
        "voice": "Kore"
    },
    {
        "id": 5,
        "narrative": "대전 원신흥동에 위치한 에스텔라 쇼룸에서 100% 프라이빗 1:1 맞춤 커스텀을 경험해 보세요.",
        "subtitle": "대전 원신흥동\n100% 프라이빗 예약제 쇼룸",
        "prompt": "Premium high-end jewelry showroom boutique with marble accents, soft warm ambient lighting, elegant glass display cases, cozy private consulting table with velvet chairs, luxurious interior --ar 9:16",
        "voice": "Kore"
    },
    {
        "id": 6,
        "narrative": "지금 네이버 플레이스에서 예약하시거나 유튜브 채널을 방문해 보세요. 예약 문의는 공사이 팔이육 팔삼구구.",
        "subtitle": "유튜브 채널 @조예은-x6y\n지금 '네이버 예약'으로 방문하기",
        "prompt": "Minimalist luxury background with champagne gold particles, elegant typography overlay reading 'ESTELLAR', premium logo intro look, dark theme, smooth golden gradients --ar 9:16",
        "voice": "Kore"
    }
]

# Convert Raw audio/L16 PCM bytes to standard wrapped RIFF WAV
def save_pcm_as_wav(pcm_data, wav_path):
    try:
        with wave.open(wav_path, 'wb') as wav_file:
            wav_file.setnchannels(1)     # Mono
            wav_file.setsampwidth(2)      # 16-bit (2 bytes)
            wav_file.setframerate(24000)  # 24000 Hz sample rate
            wav_file.writeframes(pcm_data)
        return True
    except Exception as e:
        print(f"[Error] Failed to wrap raw PCM to WAV: {e}")
        return False

# Get wave file duration in seconds using python wave module (now possible with proper headers)
def get_wav_duration(file_path):
    try:
        with wave.open(file_path, 'rb') as wav:
            frames = wav.getnframes()
            rate = wav.getframerate()
            return frames / float(rate)
    except Exception as e:
        print(f"[Error] Failed to calculate duration for {file_path}: {e}")
        return 5.0  # Fallback duration

# Generate Voiceover & Image for a scene with exponential backoff retries
def generate_assets(scene):
    scene_id = scene["id"]
    narrative = scene["narrative"]
    prompt = scene["prompt"]
    voice = scene["voice"]
    
    img_path = os.path.join(temp_dir, f"scene{scene_id}.jpg")
    wav_path = os.path.join(temp_dir, f"scene{scene_id}.wav")
    
    # --- 1. Generate Voiceover Audio (TTS) ---
    # We overwrite the old corrupted WAV files to apply correct PCM header wrapping
    print(f"[Scene {scene_id}] Generating Voiceover Audio...")
    delay = 3.0
    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash-preview-tts',
                contents=narrative,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=voice
                            )
                        )
                    )
                )
            )
            
            # Find and write audio data
            audio_bytes = None
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.mime_type.startswith("audio/"):
                    audio_bytes = part.inline_data.data
                    break
            
            if audio_bytes:
                # Crucial step: convert raw audio/L16 PCM stream to standard RIFF WAV file
                success = save_pcm_as_wav(audio_bytes, wav_path)
                if success:
                    print(f"[Scene {scene_id}] Wrapped raw PCM into standard WAV successfully.")
                    break
                else:
                    raise Exception("Failed to wrap PCM to WAV.")
            else:
                raise Exception("No inline audio data returned.")
        except Exception as e:
            if "429" in str(e) or "resource exhausted" in str(e).lower():
                sleep_time = delay + random.uniform(1.0, 3.0)
                print(f"[Scene {scene_id}] TTS Rate limit (429) encountered. Retrying in {sleep_time:.2f}s...")
                time.sleep(sleep_time)
                delay *= 2.0
            else:
                print(f"[Scene {scene_id}] TTS Error: {e}")
                break
                
    # Introduce small cooling sleep to prevent consecutive 429
    time.sleep(1.5)

    # --- 2. Generate Image (Imagen 4) ---
    # If the image was already successfully generated, we keep it to conserve tokens.
    if os.path.exists(img_path) and os.path.getsize(img_path) > 1024:
        print(f"[Scene {scene_id}] Image already exists. Skipping.")
    else:
        print(f"[Scene {scene_id}] Generating Premium Image (Imagen 4)...")
        delay = 4.0
        for attempt in range(5):
            try:
                result = client.models.generate_images(
                    model='imagen-4.0-generate-001',
                    prompt=prompt,
                    config=dict(
                        number_of_images=1,
                        aspect_ratio="9:16",
                        output_mime_type="image/jpeg",
                    )
                )
                
                if result.generated_images:
                    generated_image = result.generated_images[0]
                    image = Image.open(io.BytesIO(generated_image.image.image_bytes))
                    image.save(img_path)
                    print(f"[Scene {scene_id}] Image generated and saved successfully.")
                    break
                else:
                    raise Exception("No image returned from API.")
            except Exception as e:
                if "429" in str(e) or "resource exhausted" in str(e).lower():
                    sleep_time = delay + random.uniform(1.0, 3.0)
                    print(f"[Scene {scene_id}] Image Gen Rate limit (429). Retrying in {sleep_time:.2f}s...")
                    time.sleep(sleep_time)
                    delay *= 2.0
                else:
                    print(f"[Scene {scene_id}] Image Gen Error: {e}")
                    break
        
        # Cooling delay
        time.sleep(2.0)

# Render scene into a standalone video clip with Ken Burns zoom effect and Subtitles
def render_scene_clip(scene):
    scene_id = scene["id"]
    subtitle = scene["subtitle"]
    
    img_path = os.path.join(temp_dir, f"scene{scene_id}.jpg")
    wav_path = os.path.join(temp_dir, f"scene{scene_id}.wav")
    clip_path = os.path.join(temp_dir, f"scene{scene_id}.mp4")
    
    if not os.path.exists(img_path) or not os.path.exists(wav_path):
        print(f"[Scene {scene_id}] Missing assets. Skipping rendering.")
        return None
        
    duration = get_wav_duration(wav_path)
    print(f"[Scene {scene_id}] Rendering Video Clip (Duration: {duration:.2f}s)...")
    
    # Text sanitization for FFmpeg drawtext filter
    sub_lines = subtitle.split('\n')
    font_path = "C\\:/Windows/Fonts/malgun.ttf"
    
    # Build FFmpeg drawtext filters for dual lines
    drawtext_filters = []
    if len(sub_lines) == 1:
        text = sub_lines[0].replace("'", "\\'").replace(":", "\\:")
        drawtext_filters.append(
            f"drawtext=fontfile='{font_path}':text='{text}':fontcolor=white:fontsize=44:x=(w-text_w)/2:y=h-250:box=1:boxcolor=black@0.4:boxborderw=15"
        )
    else:
        for idx, line in enumerate(sub_lines):
            text = line.replace("'", "\\'").replace(":", "\\:")
            y_pos = "h-280" if idx == 0 else "h-210"
            drawtext_filters.append(
                f"drawtext=fontfile='{font_path}':text='{text}':fontcolor=white:fontsize=44:x=(w-text_w)/2:y={y_pos}:box=1:boxcolor=black@0.4:boxborderw=12"
            )
            
    drawtext_str = ",".join(drawtext_filters)
    
    # FFmpeg zoompan and drawtext filter
    zoom_filter = "zoompan=z='min(zoom+0.0006,1.2)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=25"
    video_filter = f"{zoom_filter},{drawtext_str}"
    
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", img_path,
        "-i", wav_path,
        "-c:v", "libx264",
        "-t", f"{duration:.2f}",
        "-vf", video_filter,
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        clip_path
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        print(f"[Scene {scene_id}] Rendered successfully: {clip_path}")
        return clip_path
    except subprocess.CalledProcessError as e:
        print(f"[Scene {scene_id}] FFmpeg render failed! Error: {e.stderr.decode('utf-8', errors='ignore')}")
        return None

# Concatenate all rendered scenes and mix background music (BGM)
def finalize_video():
    print("[Finalize] Merging all scenes into the final video...")
    
    list_path = os.path.join(temp_dir, "concat_list.txt")
    with open(list_path, "w", encoding="utf-8") as f:
        for scene in SCENES:
            clip_path = f"scene{scene['id']}.mp4"
            f.write(f"file '{clip_path}'\n")
            
    raw_output = "estellar_shorts_raw.mp4"
    final_output = "estellar_shorts.mp4"
    
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_path,
        "-c", "copy",
        raw_output
    ]
    
    try:
        subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        print("[Finalize] Successfully merged raw video!")
    except subprocess.CalledProcessError as e:
        print(f"[Finalize] Concatenation failed: {e.stderr.decode('utf-8', errors='ignore')}")
        return
        
    # Mix BGM if bgm.mp3 exists in the project root
    bgm_path = "bgm.mp3"
    if os.path.exists(bgm_path):
        print(f"[Finalize] BGM '{bgm_path}' detected! Mixing audio with voiceover...")
        cmd_bgm = [
            "ffmpeg", "-y",
            "-i", raw_output,
            "-i", bgm_path,
            "-filter_complex", "[1:a]volume=0.08,adelay=0|0[bgm];[0:a][bgm]amix=inputs=2:duration=first[a]",
            "-map", "0:v",
            "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            final_output
        ]
        try:
            subprocess.run(cmd_bgm, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            print(f"[Finalize] Success! Final mixed video saved as: '{final_output}'")
            try: os.remove(raw_output)
            except: pass
        except subprocess.CalledProcessError as e:
            print(f"[Finalize] BGM mixing failed: {e.stderr.decode('utf-8', errors='ignore')}. Keeping raw video as '{final_output}'")
            os.rename(raw_output, final_output)
    else:
        print("[Finalize] No bgm.mp3 found. Final video generated without background music.")
        if os.path.exists(final_output):
            os.remove(final_output)
        os.rename(raw_output, final_output)
        print(f"[Finalize] Final video saved as: '{final_output}'")

def main():
    print("==================================================")
    print("      💎 ESTELLAR PREMIUM SHORTS GENERATOR 💎     ")
    print("==================================================")
    
    # Step 1: Generate assets for each scene
    print("\n--- [Step 1] Generating Multimodal AI Assets ---")
    for scene in SCENES:
        generate_assets(scene)
        
    # Step 2: Render each scene into a video clip
    print("\n--- [Step 2] Rendering Dynamic Video Clips ---")
    rendered_clips = []
    for scene in SCENES:
        clip = render_scene_clip(scene)
        if clip:
            rendered_clips.append(clip)
            
    if len(rendered_clips) < len(SCENES):
        print("\n[Warning] Some scenes failed to render. Cannot finalize video.")
        sys.exit(1)
        
    # Step 3: Finalize and merge
    print("\n--- [Step 3] Finalizing Video Synthesis ---")
    finalize_video()
    
    print("\n==================================================")
    print("✨ Process Completed! Video is ready in your folder.")
    print("File: d:\\CDR_SynologyDrive\\00_AI_AGENT\\02_마케팅\\에스텔라 주얼리 홈페이지 및 홍보\\estellar_shorts.mp4")
    print("==================================================")

if __name__ == "__main__":
    main()
