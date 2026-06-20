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

def main():
    dataset_path = "data/processed/haikus_2000.json"
    print(f"Loading dataset from {dataset_path}...")
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print(f"Loaded {len(data)} entries.")
    
    invalid_indices = []
    for idx, entry in enumerate(data):
        response = entry["conversations"][1]["value"]
        _, is_perfect = evaluate_haiku(response)
        if not is_perfect:
            invalid_indices.append(idx)
            
    print(f"Found {len(invalid_indices)} invalid entries in the dataset.")
    
    if not invalid_indices:
        print("Dataset is already 100% valid under the new syllable counter!")
        return

    # Keep track of statistics
    fixed_count = 0
    start_time = time.time()
    
    for count, idx in enumerate(invalid_indices, 1):
        entry = data[idx]
        topic = entry["conversations"][0]["value"]
        old_haiku = entry["conversations"][1]["value"]
        
        print(f"\n[{count}/{len(invalid_indices)}] Fixing entry {idx} | Topic: '{topic}'")
        print(f"  Old Invalid Haiku: {old_haiku.replace('\n', ' / ')}")
        
        success = False
        attempts = 0
        max_attempts = 30
        
        while attempts < max_attempts and not success:
            attempts += 1
            temp = 0.2 + 0.1 * (attempts % 6)
            
            try:
                # Query local fine-tuned gemmaiku to rewrite the haiku
                response = query_ollama("gemmaiku:latest", topic, temp=temp)
                cleaned = clean_haiku_response(response)
                counts, is_perfect = evaluate_haiku(cleaned)
                
                if is_perfect:
                    print(f"  ✅ Success on attempt {attempts}: {counts}")
                    print(f"     New Haiku: {cleaned.replace('\n', ' / ')}")
                    entry["conversations"][1]["value"] = cleaned
                    success = True
                    fixed_count += 1
            except Exception as e:
                print(f"  ⚠️ Ollama API Error on attempt {attempts}: {e}")
                time.sleep(0.5)
                
        if not success:
            print(f"  ❌ Failed to regenerate perfect haiku for '{topic}' after {max_attempts} attempts.")
            
    # Save the updated files
    print("\nSaving corrected dataset...")
    
    # Save JSON
    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved JSON back to {dataset_path}")
    
    # Save JSONL
    jsonl_path = "data/processed/haikus_2000.jsonl"
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for entry in data:
            f.write(json.dumps(entry) + "\n")
    print(f"Saved JSONL back to {jsonl_path}")
    
    duration = time.time() - start_time
    print(f"\n=== FINISHED ===")
    print(f"Fixed: {fixed_count}/{len(invalid_indices)} entries.")
    print(f"Duration: {duration:.2f} seconds.")

if __name__ == "__main__":
    main()
