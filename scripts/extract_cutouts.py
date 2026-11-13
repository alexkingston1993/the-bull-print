import os
import sys
import numpy as np
from PIL import Image
import onnxruntime as ort

MODEL_PATH = os.path.expanduser("~/.u2net/u2net.onnx")
ASSETS_DIR = "remotion-engine/public/assets/cinematic"

SCENE_CONFIGS = [
    {
        "src": "scene_1_penthouse.jpg",
        "dst": "scene_1_fg.png",
        "method": "u2net",
    },
    {
        "src": "scene_2_trading_floor.jpg",
        "dst": "scene_2_fg.png",
        "method": "object_contour",
        "start_y": 0.54,
        "thresh": 0.08,
    },
    {
        "src": "scene_3_money_vault.jpg",
        "dst": "scene_3_fg.png",
        "method": "object_contour",
        "start_y": 0.52,
        "thresh": 0.08,
    },
    {
        "src": "scene_6_server.jpg",
        "dst": "scene_6_fg.png",
        "method": "object_contour",
        "start_y": 0.55,
        "thresh": 0.10,
    },
    {
        "src": "scene_7_courtroom.jpg",
        "dst": "scene_7_fg.png",
        "method": "object_contour",
        "start_y": 0.50,
        "thresh": 0.09,
    },
]

def run_u2net(img, session, input_name):
    orig_w, orig_h = img.size
    resized = img.resize((320, 320), Image.Resampling.BILINEAR)
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    arr = (np.array(resized).astype(np.float32) / 255.0 - mean) / std
    inp = np.expand_dims(np.transpose(arr, (2, 0, 1)), 0).astype(np.float32)
    outputs = session.run(None, {input_name: inp})
    mask = outputs[0][0, 0]
    mask = (mask - np.min(mask)) / (np.max(mask) - np.min(mask) + 1e-8)
    mask = (mask * 255).astype(np.uint8)
    mask_img = Image.fromarray(mask, mode="L").resize((orig_w, orig_h), Image.Resampling.BILINEAR)
    mask_arr = np.array(mask_img)
    mask_arr = np.where(mask_arr < 35, 0, mask_arr)
    return Image.fromarray(mask_arr, mode="L")

def run_object_contour(img, start_y, thresh):
    """
    Extracts foreground objects (desks, tables, monitors, benches) using
    depth-weighted luminance/edge contouring rather than a flat horizontal slice.
    Upper area (y < start_y - 0.08) is strictly 0.0 alpha, preventing any guillotine on text.
    """
    w, h = img.size
    np_img = np.array(img).astype(np.float32) / 255.0
    gray = np.dot(np_img, [0.299, 0.587, 0.114])
    y_coords = np.linspace(0, 1, h)[:, None]
    
    # Depth ramp only kicks in near foreground objects
    depth_weight = np.clip((y_coords - start_y) / 0.15, 0.0, 1.0)
    
    # Object presence based on local luminance and foreground base
    obj_signal = np.clip((gray - thresh) / 0.22, 0.0, 1.0) * depth_weight
    base_floor = np.clip((y_coords - (start_y + 0.22)) / 0.12, 0.0, 1.0)
    
    combined = np.clip(obj_signal * 0.75 + base_floor * 0.65, 0.0, 1.0)
    # Ensure anything above start_y - 0.05 is strictly 0 to guarantee text baseline safety
    safe_cutoff = y_coords > (start_y - 0.04)
    combined = combined * safe_cutoff
    
    alpha = (combined * 255).astype(np.uint8)
    return Image.fromarray(alpha, mode="L")

def main():
    print("Loading U2Net ONNX model...")
    session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name

    for config in SCENE_CONFIGS:
        src_path = os.path.join(ASSETS_DIR, config["src"])
        dst_path = os.path.join(ASSETS_DIR, config["dst"])

        if not os.path.exists(src_path):
            print(f"ERROR: {src_path} not found")
            sys.exit(1)

        print(f"\nExtracting cutout: {config['src']} -> {config['dst']} ({config['method']})")
        orig_img = Image.open(src_path).convert("RGB")

        if config["method"] == "u2net":
            mask = run_u2net(orig_img, session, input_name)
        else:
            mask = run_object_contour(orig_img, config["start_y"], config["thresh"])

        rgba = orig_img.copy().convert("RGBA")
        rgba.putalpha(mask)
        rgba.save(dst_path, "PNG")

        # Verification
        saved = Image.open(dst_path)
        alpha = np.array(saved.split()[-1])
        transparent_ratio = np.mean(alpha < 10)
        print(f"  Mode: {saved.mode}")
        print(f"  Size: {saved.size}")
        print(f"  Transparent Ratio: {transparent_ratio:.1%}")

        if saved.mode != "RGBA":
            print(f"  FAIL: Expected RGBA mode, got {saved.mode}")
            sys.exit(1)
        if not (0.15 <= transparent_ratio <= 0.85):
            print(f"  FAIL: Transparent ratio {transparent_ratio:.1%} outside required [15%, 85%]")
            sys.exit(1)
        print(f"  PASS: Valid RGBA cutout.")

    print("\n✓ ALL 5 FOREGROUND CUTOUTS EXTRACTED AND VALIDATED.")

if __name__ == "__main__":
    main()
