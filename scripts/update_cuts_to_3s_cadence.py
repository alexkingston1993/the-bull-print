import re

with open("scripts/produce_and_qc_tool_shorts.py", "r", encoding="utf-8") as f:
    code = f.read()

# Update QC 1 threshold to strictly require 2.7 to 3.5s per cut
old_qc_check = 'passed = (delta < 0.15) and (2.5 <= avg_cut <= 4.8)'
new_qc_check = 'passed = (delta < 0.15) and (2.7 <= avg_cut <= 3.6)'
if old_qc_check in code:
    code = code.replace(old_qc_check, new_qc_check)
    print("Updated QC 1 cadence check to 2.7-3.6s!")

with open("scripts/produce_and_qc_tool_shorts.py", "w", encoding="utf-8") as f:
    f.write(code)

