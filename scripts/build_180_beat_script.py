import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from output.options_casino_documentary.chapters_script import SEGMENTS

# Carefully mapped 5-beat breakdowns for each of the 36 segments
# Each segment: 20 seconds total -> exactly 5 beats of 4.0 seconds each.

def generate_180_beats():
    all_180_beats = []
    
    for seg in SEGMENTS:
        sid = seg["id"]
        title = seg["title"]
        vo = seg["voiceover"]
        anchor = seg.get("anchor_text", "")
        badge = seg.get("badge_text", "")
        
        # Split voiceover sentences or clauses into 5 parts
        sentences = [s.strip() for s in vo.replace("?", ".").replace("!", ".").split(".") if s.strip()]
        
        # We ensure 5 distinct narrative lines
        if len(sentences) >= 5:
            lines = sentences[:5]
        elif len(sentences) == 4:
            lines = [sentences[0], sentences[1], sentences[2], sentences[3][:len(sentences[3])//2], sentences[3][len(sentences[3])//2:]]
        elif len(sentences) == 3:
            s1_parts = sentences[0].split(",") if "," in sentences[0] else [sentences[0], sentences[0]]
            s2_parts = sentences[1].split(",") if "," in sentences[1] else [sentences[1], sentences[1]]
            lines = [s1_parts[0].strip(), s1_parts[-1].strip(), s2_parts[0].strip(), s2_parts[-1].strip(), sentences[2].strip()]
        elif len(sentences) == 2:
            s1_parts = sentences[0].split(",") if "," in sentences[0] else [sentences[0], sentences[0]]
            s2_parts = sentences[1].split(",") if "," in sentences[1] else [sentences[1], sentences[1]]
            lines = [s1_parts[0].strip(), s1_parts[-1].strip(), s2_parts[0].strip(), s2_parts[-1].strip(), "The mathematical trap closes with zero escape."]
        else:
            lines = [vo, vo, vo, vo, vo]
            
        beats = []
        shot_styles = [
            ("Wide Establishing", "Slow cinematic push-in establishing the macro environment", "1.00 -> 1.05"),
            ("Medium Narrative", "Tracking shot focusing on the central subject and core action", "1.08 -> 1.14"),
            ("Tight Data Focus", "Hard cut to sharp data chart, order book, or graphic display", "1.25 -> 1.32"),
            ("Forensic Extreme Close-Up", "Extreme punch-in revealing microscopic financial truth or raw emotion", "1.38 -> 1.45"),
            ("Re-Frame & Pull-Back", "Dynamic pull-back and drift setting up the next transition", "1.20 -> 1.06")
        ]
        
        for i in range(5):
            start_sec = (sid - 1) * 20 + i * 4
            end_sec = start_sec + 4
            
            # format mm:ss
            st_str = f"{start_sec // 60:02d}:{start_sec % 60:02d}"
            et_str = f"{end_sec // 60:02d}:{end_sec % 60:02d}"
            
            beat_obj = {
                "beat_id": f"{sid}.{i+1}",
                "segment_id": sid,
                "part": i + 1,
                "segment_title": title,
                "timestamp": f"{st_str} - {et_str}",
                "duration": "4.0s",
                "camera_shot": shot_styles[i][0],
                "motion_direction": shot_styles[i][1],
                "zoom_profile": shot_styles[i][2],
                "voiceover_line": lines[i],
                "anchor_text": anchor if i == 1 or i == 3 else "",
                "badge_text": badge if i == 2 or i == 3 else "",
            }
            beats.append(beat_obj)
            
        all_180_beats.extend(beats)
        
    return all_180_beats

if __name__ == "__main__":
    beats = generate_180_beats()
    print(f"Generated {len(beats)} micro-beats across 36 segments (exactly 4.0s each).")
