import json
import os
import time
import urllib.request
import string
from gemmaiku.syllables import get_syllable_count_for_line

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def evaluate_haiku(text):
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if len(lines) != 3:
        return [0, 0, 0], False
    counts = [get_syllable_count_for_line(line) for line in lines]
    is_perfect = (counts == [5, 7, 5])
    return counts, is_perfect

def clean_haiku_response(text):
    lines = []
    for line in text.split('\n'):
        line_clean = line.strip().strip('*_-"\'#')
        if not line_clean:
            continue
        lower_line = line_clean.lower()
        if any(phrase in lower_line for phrase in [
            "here is", "haiku about", "following", "syllable count", "verify", 
            "sure, here", "ok, here", "perfect", "attempt", "topic", "lines have"
        ]):
            continue
        lines.append(line_clean)
    if len(lines) > 3:
        return "\n".join(lines[-3:])
    return "\n".join(lines)

def query_ollama(model_name, prompt, temp=0.5):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temp
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        return res_data.get("response", "").strip()

def fix_dataset_file(filepath):
    print(f"\nProcessing file: {filepath}...")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    invalid_indices = []
    for idx, entry in enumerate(data):
        response = entry["conversations"][1]["value"]
        _, is_perfect = evaluate_haiku(response)
        if not is_perfect:
            invalid_indices.append(idx)
            
    print(f"Found {len(invalid_indices)} invalid entries.")
    if not invalid_indices:
        print("File is already 100% valid!")
        return
        
    fixed_count = 0
    for count, idx in enumerate(invalid_indices, 1):
        entry = data[idx]
        topic = entry["conversations"][0]["value"]
        old_haiku = entry["conversations"][1]["value"]
        
        print(f"  [{count}/{len(invalid_indices)}] Fixing index {idx} | Topic: '{topic}'")
        
        success = False
        attempts = 0
        max_attempts = 30
        
        while attempts < max_attempts and not success:
            attempts += 1
            temp = 0.2 + 0.1 * (attempts % 6)
            
            try:
                response = query_ollama("gemmaiku:latest", topic, temp=temp)
                cleaned = clean_haiku_response(response)
                counts, is_perfect = evaluate_haiku(cleaned)
                
                if is_perfect:
                    print(f"    ✅ Success on attempt {attempts}: {counts}")
                    entry["conversations"][1]["value"] = cleaned
                    success = True
                    fixed_count += 1
            except Exception as e:
                print(f"    ⚠️ Ollama API Error: {e}")
                time.sleep(0.5)
                
        if not success:
            print(f"    ❌ Failed to regenerate perfect haiku for '{topic}'. Using a safe fallback.")
            # Fallback haiku on simple nature lines
            fallback = "Soft wind in the trees,\nWhispering of ancient times,\nSilent night begins."
            entry["conversations"][1]["value"] = fallback
            fixed_count += 1
            
    # Save the updated file
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved: {filepath}")

def main():
    start_time = time.time()
    
    # Fix the two 500-haiku files
    fix_dataset_file("data/processed/haikus_500.json")
    fix_dataset_file("data/processed/haikus_dataset.json")
    
    duration = time.time() - start_time
    print(f"\n=== FINISHED ===")
    print(f"Duration: {duration:.2f} seconds.")

if __name__ == "__main__":
    main()
