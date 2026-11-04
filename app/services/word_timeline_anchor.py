#!/usr/bin/env python3
"""
app/services/word_timeline_anchor.py
The Bull Print — Hypit/WhisperX Word-Level Visual Timeline Anchor.

Replaces fixed-second cuts with precise word-level synchronization:
- Maps words, financial entities, and clauses to sub-second audio timestamps
- Triggers visual events (stat slams, highlighter sweeps, red laser cuts) exactly on spoken words
- Eliminates visual desynchronization between speech and on-screen graphics
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class SpokenWordBeat:
    word: str
    start: float
    end: float
    confidence: float = 1.0
    is_entity: bool = False
    entity_type: Optional[str] = None  # e.g., 'CURRENCY', 'PERCENTAGE', 'REGULATION', 'CRITICAL_KEYWORD'


@dataclass
class VisualEventTrigger:
    timestamp: float
    action_type: str  # e.g., 'HIGHLIGHT_SWEEP', 'STAT_SLAM', 'LASER_STRIKE', 'CAMERA_DIVE'
    payload: Dict
    associated_word: str


class WordTimelineAnchor:
    """
    Parses WhisperX word-level transcriptions and aligns them to video scenes.
    Generates exact micro-second triggers for the rendering engine.
    """
    CRITICAL_KEYWORDS = {
        "trap": "CRITICAL_KEYWORD",
        "slashed": "CRITICAL_KEYWORD",
        "zero": "CRITICAL_KEYWORD",
        "denied": "CRITICAL_KEYWORD",
        "exclusion": "REGULATION",
        "sub-limit": "REGULATION",
        "proportionate": "REGULATION",
        "98.4%": "PERCENTAGE",
        "61.2%": "PERCENTAGE",
        "10,00,000": "CURRENCY",
        "4,88,000": "CURRENCY",
    }

    def __init__(self):
        self.words: List[SpokenWordBeat] = []
        self.triggers: List[VisualEventTrigger] = []

    def load_from_whisperx(self, segments: List[Dict]):
        """
        Loads alignment data from standard WhisperX JSON format:
        [{"start": 0.0, "end": 2.5, "words": [{"word": "The", "start": 0.1, "end": 0.3}, ...]}]
        """
        self.words.clear()
        for seg in segments:
            for w in seg.get("words", []):
                cleaned = w["word"].strip().lower()
                entity_type = None
                for kw, kw_type in self.CRITICAL_KEYWORDS.items():
                    if kw in cleaned:
                        entity_type = kw_type
                        break
                
                beat = SpokenWordBeat(
                    word=w["word"],
                    start=float(w["start"]),
                    end=float(w["end"]),
                    confidence=float(w.get("score", 1.0)),
                    is_entity=(entity_type is not None),
                    entity_type=entity_type
                )
                self.words.append(beat)

    def extract_visual_triggers(self) -> List[VisualEventTrigger]:
        """
        Generates deterministic visual triggers from the word beats.
        """
        triggers = []
        for beat in self.words:
            w_lower = beat.word.strip().lower()
            
            # Stat slam on percentages
            if "%" in w_lower or beat.entity_type == "PERCENTAGE":
                triggers.append(VisualEventTrigger(
                    timestamp=beat.start,
                    action_type="STAT_SLAM",
                    payload={"value": beat.word},
                    associated_word=beat.word
                ))
            
            # Highlighter sweep on regulatory terms
            elif beat.entity_type == "REGULATION" or "clause" in w_lower:
                triggers.append(VisualEventTrigger(
                    timestamp=beat.start,
                    action_type="HIGHLIGHT_SWEEP",
                    payload={"clause": beat.word},
                    associated_word=beat.word
                ))
            
            # Laser strike or alert badge on critical warning words
            elif beat.entity_type == "CRITICAL_KEYWORD":
                triggers.append(VisualEventTrigger(
                    timestamp=beat.start,
                    action_type="LASER_STRIKE",
                    payload={"keyword": beat.word},
                    associated_word=beat.word
                ))

        self.triggers = triggers
        return triggers


if __name__ == "__main__":
    anchor = WordTimelineAnchor()
    mock_segments = [
        {"start": 0.0, "end": 4.0, "words": [
            {"word": "The", "start": 0.1, "end": 0.3},
            {"word": "98.4%", "start": 0.4, "end": 0.9},
            {"word": "claim", "start": 1.0, "end": 1.3},
            {"word": "settlement", "start": 1.4, "end": 1.9},
            {"word": "trap", "start": 2.0, "end": 2.5},
        ]}
    ]
    anchor.load_from_whisperx(mock_segments)
    t = anchor.extract_visual_triggers()
    print(f"Loaded {len(anchor.words)} words, extracted {len(t)} visual triggers.")
    for trig in t:
        print(f"[{trig.timestamp:.2f}s] {trig.action_type} on '{trig.associated_word}'")
