import json
import time
import urllib.request
import os
import matplotlib.pyplot as plt
from gemmaiku.syllables import get_syllable_count_for_line

# ---------------------------------------------------------------------------
# Evaluation Topics (10 diverse prompts)
# ---------------------------------------------------------------------------
test_topics = [
    "artificial intelligence",
    "the French Revolution",
    "making chocolate chip cookies",
    "black holes in space",
    "the culture of Tokyo",
    "how to grow organic tomatoes",
    "William Shakespeare",
    "quantum computing",
    "learning to play chess",
    "Mount Everest climb"
]

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

def run_experiment_for_model(model_name, label):
    print(f"\nEvaluating Model: {model_name} ({label})...")
    results = []
    
    for idx, topic in enumerate(test_topics, 1):
        print(f"[{idx}/10] Testing topic: '{topic}'")
        attempts = 0
        max_attempts = 30
        success = False
        final_haiku = ""
        final_counts = []
        start_time = time.time()
        
        while attempts < max_attempts and not success:
            attempts += 1
            # Vary temperature slightly across attempts
            temp = 0.2 + 0.1 * (attempts % 6)
            
            # Format prompt slightly differently if it's the base model to guide it
            if "gemma3" in model_name and "gemmaiku" not in model_name:
                prompt_text = (
                    "Write a strictly 5-7-5 syllable haiku about: What is the capital of France?\n"
                    "Paris holds the key,\n"
                    "City of lights, grand and bright,\n"
                    "Capital stands proud.\n\n"
                    f"Write a strictly 5-7-5 syllable haiku about: {topic}"
                )
            else:
                # Our fine-tuned model already knows to output haikus
                prompt_text = topic
                
            try:
                response = query_ollama(model_name, prompt_text, temp=temp)
                cleaned = clean_haiku_response(response)
                counts, is_perfect = evaluate_haiku(cleaned)
                
                if is_perfect:
                    success = True
                    final_haiku = cleaned
                    final_counts = counts
            except Exception as e:
                print(f"  Error on attempt {attempts}: {e}")
                time.sleep(0.5)
                
        duration = time.time() - start_time
        print(f"  Result: {'✅ Success' if success else '❌ Failed'} in {attempts} attempts ({duration:.2f}s)")
        if success:
            print(f"  Haiku: {final_haiku.replace('\n', ' / ')}")
            
        results.append({
            "topic": topic,
            "success": success,
            "attempts": attempts if success else max_attempts,
            "haiku": final_haiku,
            "counts": final_counts,
            "duration_s": duration
        })
        
    return results

def main():
    print("=== Starting Gemmaiku Evaluation Experiment ===")
    
    # 1. Run base model
    base_results = run_experiment_for_model("gemma3:1b", "Base Gemma-3 1B")
    
    # 2. Run fine-tuned model
    gemmaiku_results = run_experiment_for_model("gemmaiku:latest", "Fine-Tuned Gemmaiku 1B")
    
    # 3. Analyze and Compile Results
    data = {
        "base_model": base_results,
        "gemmaiku_model": gemmaiku_results
    }
    
    # Save results as JSON
    os.makedirs("scratch", exist_ok=True)
    with open("scratch/evaluation_results.json", "w") as f:
        json.dump(data, f, indent=2)
    print("\nSaved raw results to scratch/evaluation_results.json")
    
    # 4. Generate Matplotlib Comparison Chart
    topics_short = [t[:15] + "..." if len(t) > 15 else t for t in test_topics]
    base_attempts = [r["attempts"] for r in base_results]
    gemmaiku_attempts = [r["attempts"] for r in gemmaiku_results]
    
    x = range(len(test_topics))
    width = 0.35
    
    plt.figure(figsize=(12, 6))
    plt.bar([i - width/2 for i in x], base_attempts, width, label='Base Gemma-3 1B (Few-shot)', color='#E74C3C')
    plt.bar([i + width/2 for i in x], gemmaiku_attempts, width, label='Fine-Tuned Gemmaiku 1B (Zero-shot)', color='#2ECC71')
    
    plt.xlabel('Topics')
    plt.ylabel('Attempts to Get 5-7-5 Haiku (Lower is Better)')
    plt.title('Haiku Syllabus Matching Performance: Base vs. Fine-Tuned Model')
    plt.xticks(x, topics_short, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    
    # Ensure assets folder exists
    os.makedirs("assets", exist_ok=True)
    plt.savefig("assets/evaluation_chart.png")
    print("Saved comparison chart to assets/evaluation_chart.png")
    
    # Write a quick text summary to console
    base_avg = sum(base_attempts) / len(test_topics)
    gemmaiku_avg = sum(gemmaiku_attempts) / len(test_topics)
    print(f"\n=== SUMMARY RESULTS ===")
    print(f"Base Gemma-3 1B: Average attempts: {base_avg:.2f}")
    print(f"Fine-Tuned Gemmaiku 1B: Average attempts: {gemmaiku_avg:.2f}")
    print("Averages include failures (penalized at 30 attempts).")

if __name__ == "__main__":
    main()
