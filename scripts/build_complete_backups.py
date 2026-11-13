import os, sys, json, re, glob
from datetime import datetime, timezone

def clean_user_text(text):
    if not text: return ''
    m = re.search(r'<USER_REQUEST>(.*?)</USER_REQUEST>', text, re.DOTALL)
    if m:
        text = m.group(1).strip()
    text = re.sub(r'<ADDITIONAL_METADATA>.*?</ADDITIONAL_METADATA>', '', text, flags=re.DOTALL).strip()
    text = re.sub(r'<USER_SETTINGS_CHANGE>.*?</USER_SETTINGS_CHANGE>', '', text, flags=re.DOTALL).strip()
    return text.strip()

def parse_iso(dt_str):
    if not dt_str: return None
    try:
        dt_str = dt_str.replace('Z', '+00:00')
        return datetime.fromisoformat(dt_str)
    except:
        return None

def extract_session_jsonl(session_id, jsonl_path, include_tools=False, min_dt=None):
    exchanges = []
    current_user = None
    current_agent_parts = []
    
    with open(jsonl_path, 'r', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try:
                obj = json.loads(line)
            except:
                continue
            
            src = obj.get('source')
            tp = obj.get('type')
            created_at = obj.get('created_at', '')
            content = obj.get('content', '') or ''
            tool_calls = obj.get('tool_calls')
            
            if src == 'USER_EXPLICIT' or tp == 'USER_INPUT':
                if current_user:
                    u_dt = parse_iso(current_user['time'])
                    if not min_dt or (u_dt and u_dt >= min_dt):
                        exchanges.append({
                            'user_time': current_user['time'],
                            'user_text': current_user['text'],
                            'agent_responses': current_agent_parts
                        })
                clean_text = clean_user_text(content)
                if not clean_text and content: clean_text = content.strip()
                current_user = {'time': created_at, 'text': clean_text}
                current_agent_parts = []
            elif tp in ['PLANNER_RESPONSE', 'AGENT_RESPONSE'] or src == 'MODEL':
                if content:
                    current_agent_parts.append({'time': created_at, 'type': 'text', 'text': content})
                if include_tools and tool_calls:
                    for tc in tool_calls:
                        name = tc.get('function', {}).get('name') or tc.get('name') or 'tool'
                        args = tc.get('function', {}).get('arguments') or tc.get('args') or ''
                        if isinstance(args, dict):
                            args_str = json.dumps(args)
                        else:
                            args_str = str(args)
                        if len(args_str) > 250:
                            args_str = args_str[:250] + '...'
                        current_agent_parts.append({'time': created_at, 'type': 'tool_call', 'name': name, 'args': args_str})
    
    if current_user:
        u_dt = parse_iso(current_user['time'])
        if not min_dt or (u_dt and u_dt >= min_dt):
            exchanges.append({
                'user_time': current_user['time'],
                'user_text': current_user['text'],
                'agent_responses': current_agent_parts
            })
    return exchanges

antigravity_sessions = [
    {
        'id': 'a58a9d74-3165-499b-9965-becbdc0736b3',
        'title': 'Session 1: Kickoff & Setup (MoneyPrinterTurbo Local Video App)',
        'date_str': '2026-05-28 13:57 → 17:55 UTC',
        'path': '/Users/apple/.gemini/antigravity-ide/brain/a58a9d74-3165-499b-9965-becbdc0736b3/.system_generated/logs/transcript_full.jsonl',
        'fallback': '/Users/apple/.gemini/antigravity-ide/brain/a58a9d74-3165-499b-9965-becbdc0736b3/.system_generated/logs/transcript.jsonl'
    },
    {
        'id': '14689606-338b-4a66-9918-0ac1cc4a59f2',
        'title': 'Session 2: YouTube OAuth, Audio Ingestion & Pipeline Scaffolding',
        'date_str': '2026-06-14 05:13 → 12:36 UTC',
        'path': '/Users/apple/.gemini/antigravity-ide/brain/14689606-338b-4a66-9918-0ac1cc4a59f2/.system_generated/logs/transcript_full.jsonl',
        'fallback': '/Users/apple/.gemini/antigravity-ide/brain/14689606-338b-4a66-9918-0ac1cc4a59f2/.system_generated/logs/transcript.jsonl'
    },
    {
        'id': '785ab425-0a83-44ae-bdcf-5a6bf54156a8',
        'title': 'Session 3: Coding Agent Multi-Folder Exploration',
        'date_str': '2026-06-15 17:57 → 18:17 UTC',
        'path': '/Users/apple/.gemini/antigravity-ide/brain/785ab425-0a83-44ae-bdcf-5a6bf54156a8/.system_generated/logs/transcript_full.jsonl',
        'fallback': '/Users/apple/.gemini/antigravity-ide/brain/785ab425-0a83-44ae-bdcf-5a6bf54156a8/.system_generated/logs/transcript.jsonl'
    },
    {
        'id': '273643a6-4305-4642-b191-d2e4059162ac',
        'title': 'Session 4: Architectural Blueprint & Project Restructuring',
        'date_str': '2026-10-11 14:45 → 2026-10-18 19:37 UTC',
        'path': '/Users/apple/.gemini/antigravity-ide/brain/273643a6-4305-4642-b191-d2e4059162ac/.system_generated/logs/transcript_full.jsonl',
        'fallback': '/Users/apple/.gemini/antigravity-ide/brain/273643a6-4305-4642-b191-d2e4059162ac/.system_generated/logs/transcript.jsonl'
    },
    {
        'id': '2ccf8b84-0b80-4489-9cbc-3c5709cc4937',
        'title': 'Session 5: The Bull Print Platform Core Build-Out (Website, SEO, Financial Tools)',
        'date_str': '2026-10-19 03:43 → 2026-10-22 18:20 UTC',
        'path': '/Users/apple/.gemini/antigravity-ide/brain/2ccf8b84-0b80-4489-9cbc-3c5709cc4937/.system_generated/logs/transcript_full.jsonl',
        'fallback': '/Users/apple/.gemini/antigravity-ide/brain/2ccf8b84-0b80-4489-9cbc-3c5709cc4937/.system_generated/logs/transcript.jsonl'
    },
    {
        'id': '96ef1dba-78f2-4790-bd8d-1dbad7261bf9',
        'title': 'Session 6: Production Scaling, Multi-Vertical Automation, Data Recovery',
        'date_str': '2026-10-22 18:25 → 2026-11-02 00:09 UTC',
        'path': '/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/.system_generated/logs/transcript_full.jsonl',
        'fallback': '/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/.system_generated/logs/transcript.jsonl'
    },
    {
        'id': '98c5d5da-4c41-4f9b-9be0-950d242da364',
        'title': 'Session 7: YouTube Channel Launch, 20-Runner Cloud Matrix, 12-Min Documentaries, VidIQ Max-Out',
        'date_str': '2026-11-01 20:08 → 2026-11-12 18:37 UTC',
        'path': '/Users/apple/.gemini/antigravity-ide/brain/98c5d5da-4c41-4f9b-9be0-950d242da364/.system_generated/logs/transcript_full.jsonl',
        'fallback': '/Users/apple/.gemini/antigravity-ide/brain/98c5d5da-4c41-4f9b-9be0-950d242da364/.system_generated/logs/transcript.jsonl'
    },
    {
        'id': 'b14bfb57-38fe-43ee-a68d-4d418231d22c',
        'title': 'Session 8: Current Status Audit, Cloud Runner Verification & Complete Archive Generation',
        'date_str': '2026-11-12 18:45 → 2026-11-13 00:20 UTC',
        'path': '/Users/apple/.gemini/antigravity/brain/b14bfb57-38fe-43ee-a68d-4d418231d22c/.system_generated/logs/transcript_full.jsonl',
        'fallback': '/Users/apple/.gemini/antigravity/brain/b14bfb57-38fe-43ee-a68d-4d418231d22c/.system_generated/logs/transcript.jsonl'
    }
]

print('Starting File 1 generation: COMPLETE_PROJECT_CONVERSATION_BACKUP.md')
with open('COMPLETE_PROJECT_CONVERSATION_BACKUP.md', 'w', encoding='utf-8') as out:
    out.write('# The Bull Print — Complete Project Conversation & Development Archive\n\n')
    out.write('**Project:** The Bull Print (`bullprintmedia.com`) / Video Automation Pipeline / Autonomous Cloud Production Matrix\n')
    out.write('**Coverage:** Complete chronological project history from inception (May 28, 2026) to present (November 13, 2026)\n')
    out.write(f'**Generated At:** {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}\n\n')
    out.write('---\n\n')
    
    out.write('## Executive Summary & Strategic Evolution\n\n')
    out.write('1. **Phase 1: Inception & MoneyPrinterTurbo Scaffolding (May–June 2026)**\n')
    out.write('   - Initial objective: Free automated short-form video creation for financial content.\n')
    out.write('   - Local dependencies: Whisper, Edge-TTS/Coqui XTTS, PIL canvas drawing, and FFmpeg.\n')
    out.write('   - Discovery: Local Mac rendering caused thermal throttling and took 15+ minutes per video. Reusing image plates resulted in repetitive, low-engagement shorts.\n\n')
    
    out.write('2. **Phase 2: OpenCode Hermes Orchestration & Channel Scaffolding (June 2026)**\n')
    out.write('   - Automated daily market update video generation for Nifty/Sensex/BankNifty.\n')
    out.write('   - Automated audio voice cloning with Alex reference audio (`prabhat_ref_conversational.wav`).\n')
    out.write('   - Initial YouTube Data API v3 OAuth setup and upload integration.\n\n')
    
    out.write('3. **Phase 3: Architectural Pivot to "The Bull Print" (October 11–18, 2026)**\n')
    out.write('   - Transformation into an institutional financial media brand: **The Bull Print** (`bullprintmedia.com`).\n')
    out.write('   - Transition from simple shorts to a dual format: high-CTR YouTube shorts and 12-minute deep-dive investigative documentaries.\n')
    out.write('   - Architectural rule established: **100% Cloud Execution Only** (Zero local rendering).\n\n')
    
    out.write('4. **Phase 4: Full-Stack Web Platform & Financial Tools Build-Out (October 19–22, 2026)**\n')
    out.write('   - Production website launched with dark financial aesthetic, glassmorphism UI, interactive trading tools (Option Greeks, SIP/CAGR, Margin Calculators).\n')
    out.write('   - Automated SEO article publishing system with bespoke SVG/PNG infographics and JSON-LD structured data.\n')
    out.write('   - Deployed on Vercel with automated continuous deployment.\n\n')
    
    out.write('5. **Phase 5: Multi-Vertical Expansion & Anti-Hallucination Guardrails (October 22–November 02, 2026)**\n')
    out.write('   - 5 content verticals supported: Indian Equities, Global Macro/Forex, Crypto/DeFi, Commodities/Energy, and Institutional Order Flow.\n')
    out.write('   - Zero-database affiliate telemetry ledger with transparent tracking and compliance.\n')
    out.write('   - Automated recovery and indexing of historical conversational records.\n\n')
    
    out.write('6. **Phase 6: YouTube Channel Launch & Cloud Parallel Video Matrix (November 01–12, 2026)**\n')
    out.write('   - YouTube channel launch: Multi-project OAuth credential pool with automatic token rotation (Slot 1, Slot 2, Slot 3).\n')
    out.write('   - 20-runner parallel GitHub Actions cloud matrix (`parallel_video_matrix.yml`): distributes video rendering across parallel cloud runners, reducing render time from 40 mins to under 4 mins.\n')
    out.write('   - Dual-T4 GPU Kaggle cloud runner integration for 12-minute documentaries (WazirX Heist, Luna Collapse, Masterclass Series).\n')
    out.write('   - Strict Master Blueprint Enforcement: Zero frame reuse, dynamic kinetic 3D typography, mobile safe zones, and 100/100 VidIQ SEO score optimization.\n\n')
    
    out.write('7. **Phase 7: Cloud Runner Audit & Comprehensive Backup (November 12–13, 2026)**\n')
    out.write('   - Verification of successful parallel GitHub Actions execution (Run `43213505935` / Video `https://youtu.be/Jj8e7ZsufSQ`).\n')
    out.write('   - Audit of Kaggle GPU kernels (`mpt-masterclass-*` completed).\n')
    out.write('   - Comprehensive end-to-end conversation backup generation.\n\n')
    
    out.write('## Master Session Index\n\n')
    out.write('| Session ID | Date / Time | Title | Prompts | Source |\n')
    out.write('|---|---|---|---|---|\n')
    
    # Process and write all Antigravity sessions
    all_exchanges_by_session = []
    for s in antigravity_sessions:
        p = s['path'] if os.path.exists(s['path']) else s['fallback']
        if not os.path.exists(p):
            continue
        exs = extract_session_jsonl(s['id'], p, include_tools=False)
        all_exchanges_by_session.append((s, exs))
        out.write(f'| `{s["id"]}` | {s["date_str"]} | {s["title"]} | {len(exs)} | Antigravity IDE |\n')
    
    out.write('\n---\n\n')
    
    # Write chronological exchanges for every session
    for s, exs in all_exchanges_by_session:
        out.write(f'# {s["title"]}\n\n')
        out.write(f'**Session ID:** `{s["id"]}`  \n')
        out.write(f'**Period:** {s["date_str"]}  \n')
        out.write(f'**Total User Prompts:** {len(exs)}\n\n')
        
        for i, ex in enumerate(exs, 1):
            out.write(f'---\n\n### 🧑 USER [Exchange {i}] · {ex["user_time"]}\n\n')
            out.write(ex['user_text'] + '\n\n')
            
            for resp in ex['agent_responses']:
                if resp['type'] == 'text':
                    out.write(f'### 🤖 AGENT · {resp["time"]}\n\n')
                    out.write(resp['text'] + '\n\n')
        out.write('\n\n')

print('COMPLETE_PROJECT_CONVERSATION_BACKUP.md created successfully.')
