import os, sys, json, re
from datetime import datetime, timezone, timedelta

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

# 30 days cutoff: Oct 14, 2026 00:00:00 UTC
cutoff_dt = datetime(2026, 10, 14, 0, 0, 0, tzinfo=timezone.utc)

def extract_in_depth_jsonl(session_id, jsonl_path, min_dt):
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
                    if u_dt and u_dt >= min_dt:
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
                if tool_calls:
                    for tc in tool_calls:
                        name = tc.get('function', {}).get('name') or tc.get('name') or 'tool'
                        args = tc.get('function', {}).get('arguments') or tc.get('args') or ''
                        if isinstance(args, dict):
                            args_str = json.dumps(args, indent=2)
                        else:
                            args_str = str(args)
                        current_agent_parts.append({'time': created_at, 'type': 'tool_call', 'name': name, 'args': args_str})
    
    if current_user:
        u_dt = parse_iso(current_user['time'])
        if u_dt and u_dt >= min_dt:
            exchanges.append({
                'user_time': current_user['time'],
                'user_text': current_user['text'],
                'agent_responses': current_agent_parts
            })
    return exchanges

sessions_in_scope = [
    {
        'id': '273643a6-4305-4642-b191-d2e4059162ac',
        'title': 'Part 1: Architectural Reset & Blueprint Specification (Oct 14–18)',
        'path': '/Users/apple/.gemini/antigravity-ide/brain/273643a6-4305-4642-b191-d2e4059162ac/.system_generated/logs/transcript_full.jsonl',
        'fallback': '/Users/apple/.gemini/antigravity-ide/brain/273643a6-4305-4642-b191-d2e4059162ac/.system_generated/logs/transcript.jsonl'
    },
    {
        'id': '2ccf8b84-0b80-4489-9cbc-3c5709cc4937',
        'title': 'Part 2: The Bull Print Platform Build-Out (Oct 19–22)',
        'path': '/Users/apple/.gemini/antigravity-ide/brain/2ccf8b84-0b80-4489-9cbc-3c5709cc4937/.system_generated/logs/transcript_full.jsonl',
        'fallback': '/Users/apple/.gemini/antigravity-ide/brain/2ccf8b84-0b80-4489-9cbc-3c5709cc4937/.system_generated/logs/transcript.jsonl'
    },
    {
        'id': '96ef1dba-78f2-4790-bd8d-1dbad7261bf9',
        'title': 'Part 3: Multi-Vertical Scaling, Financial Infographics & Data Recovery (Oct 22–Nov 02)',
        'path': '/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/.system_generated/logs/transcript_full.jsonl',
        'fallback': '/Users/apple/.gemini/antigravity-ide/brain/96ef1dba-78f2-4790-bd8d-1dbad7261bf9/.system_generated/logs/transcript.jsonl'
    },
    {
        'id': '98c5d5da-4c41-4f9b-9be0-950d242da364',
        'title': 'Part 4: YouTube Launch, 20-Runner Cloud Matrix, 12-Min Documentaries, VidIQ Max-Out (Nov 01–12)',
        'path': '/Users/apple/.gemini/antigravity-ide/brain/98c5d5da-4c41-4f9b-9be0-950d242da364/.system_generated/logs/transcript_full.jsonl',
        'fallback': '/Users/apple/.gemini/antigravity-ide/brain/98c5d5da-4c41-4f9b-9be0-950d242da364/.system_generated/logs/transcript.jsonl'
    },
    {
        'id': 'b14bfb57-38fe-43ee-a68d-4d418231d22c',
        'title': 'Part 5: Production Verification, Cloud Runner Audit & Complete Backups (Nov 12–13)',
        'path': '/Users/apple/.gemini/antigravity/brain/b14bfb57-38fe-43ee-a68d-4d418231d22c/.system_generated/logs/transcript_full.jsonl',
        'fallback': '/Users/apple/.gemini/antigravity/brain/b14bfb57-38fe-43ee-a68d-4d418231d22c/.system_generated/logs/transcript.jsonl'
    }
]

print('Generating LAST_30_DAYS_IN_DEPTH_CONVERSATION_BACKUP.md...')
with open('LAST_30_DAYS_IN_DEPTH_CONVERSATION_BACKUP.md', 'w', encoding='utf-8') as out:
    out.write('# The Bull Print — In-Depth Conversation Backup (Past 30 Days)\n\n')
    out.write('**Timeframe:** October 14, 2026 00:00:00 UTC → November 13, 2026 (Present)\n')
    out.write('**Level of Detail:** In-Depth (Full user prompts, complete assistant responses, executed commands, GitHub Actions runs, Kaggle GPU jobs, YouTube uploads, and SEO optimizations)\n')
    out.write(f'**Generated At:** {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}\n\n')
    out.write('---\n\n')
    
    out.write('## 30-Day Chronological Milestone Log\n\n')
    out.write('- **Oct 14 – 18:** Established Master Blueprint (`.agents/rules/MASTER_BLUEPRINT.md`). Enforced 100% Cloud Execution (zero local rendering) and Zero Frame Reuse mandates.\n')
    out.write('- **Oct 19 – 22:** Built and deployed The Bull Print website (`bullprintmedia.com`) with glassmorphism UI, interactive Option Greeks/SIP/CAGR calculators, and automated article publishing.\n')
    out.write('- **Oct 22 – Nov 02:** Scaled multi-vertical engine across Equities, Crypto, Forex, and Macro. Built automated SVG/PNG infographics and zero-DB affiliate telemetry tracking.\n')
    out.write('- **Nov 01 – Nov 08:** Deployed YouTube multi-project OAuth pool with token rotation (`Slot 1`, `Slot 2`, `Slot 3`). Built 12-minute documentary engine for high-leverage investigative features (FTX, Terra Luna, WazirX Heist, Masterclass series).\n')
    out.write('- **Nov 08 – Nov 12:** Implemented 20-runner parallel GitHub Actions video matrix (`parallel_video_matrix.yml`), slashing 60-second video render time to ~3m 50s. Maxed out VidIQ SEO scores (100/100) across all public channel videos with verified article interlinks.\n')
    out.write('- **Nov 12 – 13:** Verified successful cloud execution of sample short on GitHub Actions (Run `43213505935`, video `https://youtu.be/Jj8e7ZsufSQ`) and verified completed Dual-T4 Kaggle GPU masterclass kernels.\n\n')
    out.write('---\n\n')
    
    for s in sessions_in_scope:
        p = s['path'] if os.path.exists(s['path']) else s['fallback']
        if not os.path.exists(p): continue
        exs = extract_in_depth_jsonl(s['id'], p, cutoff_dt)
        if not exs: continue
        
        out.write(f'# {s["title"]}\n\n')
        out.write(f'**Session ID:** `{s["id"]}`  \n')
        out.write(f'**Active Exchanges in Window:** {len(exs)}\n\n')
        
        for i, ex in enumerate(exs, 1):
            out.write(f'---\n\n### 🧑 USER [Exchange {i}] · {ex["user_time"]}\n\n')
            out.write(ex['user_text'] + '\n\n')
            
            for resp in ex['agent_responses']:
                if resp['type'] == 'text':
                    out.write(f'### 🤖 AGENT · {resp["time"]}\n\n')
                    out.write(resp['text'] + '\n\n')
                elif resp['type'] == 'tool_call':
                    out.write(f'> ⚡ **Tool Action:** `{resp["name"]}`\n')
                    args_text = resp["args"]
                    if '\n' in args_text:
                        out.write(f'```json\n{args_text}\n```\n\n')
                    else:
                        out.write(f'> `{args_text}`\n\n')
        out.write('\n\n')

print('LAST_30_DAYS_IN_DEPTH_CONVERSATION_BACKUP.md created successfully.')
