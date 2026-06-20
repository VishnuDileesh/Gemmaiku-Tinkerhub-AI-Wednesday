import json
import os
import random
import time
import string
import urllib.request
from gemmaiku.syllables import get_syllable_count_for_line

# ---------------------------------------------------------------------------
# 1. Define lists of vocabulary
# ---------------------------------------------------------------------------
actions = [
    "brew a cup of coffee", "make a cup of green tea", "bake sourdough bread", "roast a chicken", 
    "steam fresh vegetables", "fry an egg", "scramble eggs", "make french toast", "grill a cheese sandwich", 
    "build a campfire", "pitch a canvas tent", "tie a bowline knot", "tie a double half hitch", 
    "change a flat tire", "wash a wool sweater", "clean a mechanical keyboard", "format a USB drive", 
    "install an operating system", "write a thank you note", "learn to read sheet music", 
    "play a C major scale", "tune an acoustic guitar", "juggle three tennis balls", "whistle a happy tune", 
    "solve a crossword puzzle", "play a game of chess", "run a five kilometer race", "do ten pushups", 
    "hold a plank position", "paint a watercolor landscape", "sketch a human face", "write a short story", 
    "read a topographic map", "pack a hiking backpack", "clean a dusty window", "train a puppy to sit", 
    "groom a long-haired cat", "feed aquarium fish", "grow organic tomatoes", "plant a cherry tree", 
    "prune a rose bush", "sow sunflower seeds", "make fresh pasta dough", "cook white rice", 
    "grill a salmon fillet", "steam pork dumplings", "toss a Caesar salad", "squeeze fresh orange juice", 
    "blend a green smoothie", "bake chocolate chip cookies", "flip buttermilk pancakes", "brew a batch of cider", 
    "sew a button on a shirt", "knit a wool scarf", "build a wooden birdhouse", "fold an origami crane", 
    "paint a sunset", "study for an exam", "clean a messy room", "organize a bookshelf", "wash a dirty car", 
    "wax a surfboard", "ride a skateboard", "learn a new language", "set up a router", "back up your computer", 
    "write a cover letter", "prepare for an interview", "meditate in silence", "do a sun salutation", 
    "take a deep breath", "count to one hundred", "write in a journal"
]

concepts = [
    "photosynthesis", "gravity", "electromagnetism", "sound waves", "the water cycle", "quantum physics", 
    "plate tectonics", "continental drift", "cellular respiration", "mitosis", "meiosis", "genetics", 
    "DNA replication", "RNA translation", "enzyme catalysis", "protein synthesis", "vitamin C", 
    "calcium absorption", "inertia", "momentum", "friction", "kinetic energy", "potential energy", 
    "thermodynamics", "entropy", "light reflection", "light refraction", "prisms", "rainbow formation", 
    "static electricity", "lightning strikes", "thunder claps", "hurricanes", "tornadoes", "earthquakes", 
    "volcanoes", "tsunamis", "glaciers", "icebergs", "coral reefs", "ocean tides", "ocean currents", 
    "the ozone layer", "acid rain", "greenhouse effect", "climate change", "solar energy", "wind turbines", 
    "geothermal heating", "nuclear fusion", "hydroelectric power", "fossils", "dinosaur extinction", 
    "natural selection", "adaptation", "forest ecosystems", "food webs", "food chain", "decomposers", 
    "bee pollination", "seed dispersal", "plant grafting", "tree rings", "soil erosion", "composting", 
    "recycling", "carbon footprint", "water conservation", "biodiversity", "endangered species", 
    "national parks", "wilderness areas", "absolute zero", "atomic structures", "chemical bonds", 
    "periodic table", "noble gases", "acids and bases"
]

people = [
    "Albert Einstein", "Isaac Newton", "Charles Darwin", "Marie Curie", "Galileo Galilei", "Nikola Tesla", 
    "Thomas Edison", "Alexander Graham Bell", "Orville Wright", "Wilbur Wright", "Amelia Earhart", 
    "Leonardo da Vinci", "Michelangelo", "Vincent van Gogh", "Pablo Picasso", "Claude Monet", 
    "Georgia O'Keeffe", "Ansel Adams", "William Shakespeare", "Jane Austen", "Mark Twain", "Charles Dickens", 
    "Leo Tolstoy", "Edgar Allan Poe", "Emily Dickinson", "Robert Frost", "Maya Angelou", 
    "Ludwig van Beethoven", "Wolfgang Amadeus Mozart", "Johann Sebastian Bach", "Frederic Chopin", 
    "Louis Armstrong", "Miles Davis", "Ella Fitzgerald", "Socrates", "Plato", "Aristotle", 
    "Alexander the Great", "Julius Caesar", "Cleopatra", "Joan of Arc", "Marco Polo", "Christopher Columbus", 
    "Ferdinand Magellan", "Vasco da Gama", "Captain James Cook", "Roald Amundsen", "Neil Armstrong", 
    "Sally Ride", "Yuri Gagarin"
]

history_topics = [
    "the Roman Empire", "ancient Greece", "ancient Egypt", "the Renaissance", "the Industrial Revolution", 
    "the French Revolution", "the American Revolution", "the Silk Road", "the Viking age", "the Mayan civilization", 
    "the Aztec empire", "the Inca empire", "the Ottoman Empire", "the Byzantine Empire", "the Han Dynasty", 
    "the Ming Dynasty", "the Victorian era", "the Space Race", "the gold rush", "the signing of the Magna Carta", 
    "the founding of the United Nations", "the construction of the Great Wall", "the building of the Pyramids", 
    "the destruction of Pompeii"
]

countries = [
    "Spain", "Germany", "Italy", "Canada", "Brazil", "Australia", "India", "China", "Egypt", "South Africa", 
    "Mexico", "Argentina", "Russia", "Norway", "Sweden", "Switzerland", "Austria", "Belgium", "the Netherlands", 
    "Denmark", "Finland", "Greece", "Turkey", "Portugal", "Ireland", "New Zealand", "Japan", "South Korea", 
    "Thailand", "Vietnam", "Singapore", "Indonesia", "Philippines", "Malaysia", "Kenya", "Morocco", 
    "Peru", "Chile", "Colombia", "France"
]

locations = [
    "the Grand Canyon", "the Sahara Desert", "the Amazon Rainforest", "Mount Everest", "Mount Fuji", 
    "the Great Barrier Reef", "the Mariana Trench", "Niagara Falls", "Victoria Falls", "the Nile River", 
    "the Mississippi River", "the Mediterranean Sea", "the Pacific Ocean", "the Atlantic Ocean", 
    "the Indian Ocean", "the Arctic Circle", "the Antarctic continent", "the Gobi Desert", "the Mojave Desert"
]

cultural_topics = [
    "the Olympic Games", "Diwali", "Halloween", "Thanksgiving", "Chinese New Year", "Carnival in Rio", 
    "Oktoberfest", "St. Patrick's Day", "Earth Day", "the Nobel Prize", "the Oscars", "the Grammys", 
    "the Pulitzer Prize", "the Japanese tea ceremony", "origami", "calligraphy", "yoga", "mindfulness meditation", 
    "martial arts", "chess", "backgammon", "Monopoly", "Scrabble", "crossword puzzles"
]

books = [
    "Hamlet", "Macbeth", "Pride and Prejudice", "Great Expectations", "Moby Dick", "War and Peace", 
    "The Odyssey", "The Iliad", "Frankenstein", "Dracula", "The Great Gatsby", "To Kill a Mockingbird", 
    "1984", "Animal Farm", "The Hobbit", "Lord of the Rings", "The Catcher in the Rye", "The Grapes of Wrath", 
    "The Scarlet Letter", "Jane Eyre", "Wuthering Heights", "Treasure Island", "Alice in Wonderland", "Peter Pan"
]

art = [
    "the Mona Lisa", "The Starry Night", "The Scream", "The Last Supper", "Guernica", "Girl with a Pearl Earring", 
    "The Thinker", "David", "Venus de Milo", "the Sistine Chapel ceiling", "The Great Wave off Kanagawa", 
    "American Gothic", "Water Lilies"
]

math_problems = [
    "5 plus 7", "12 times 12", "100 divided by 5", "the square root of 64", "the square root of 81", 
    "15 minus 8", "50 plus 50", "9 times 9", "3 cubed", "10 to the power of 3", "the value of pi", 
    "the area of a circle", "the Pythagorean theorem", "a prime number", "an even number", "an odd number"
]

animals = [
    "cat", "dog", "lion", "tiger", "bear", "elephant", "giraffe", "zebra", "kangaroo", "panda", 
    "koala", "penguin", "dolphin", "whale", "shark", "eagle", "hawk", "owl", "parrot", "swan", 
    "duck", "chicken", "cow", "horse", "sheep", "goat", "pig", "rabbit", "deer", "wolf", 
    "fox", "squirrel", "beaver", "otter", "seal", "walrus", "octopus", "squid", "crab", "lobster", 
    "snail", "butterfly", "bee", "ant", "spider", "frog", "toad", "turtle", "lizard", "snake", 
    "crocodile", "alligator", "dinosaur", "mammoth"
]

foods = [
    "pizza", "pasta", "sushi", "tacos", "burgers", "salad", "soup", "bread", "cheese", "butter", 
    "milk", "yogurt", "eggs", "bacon", "sausage", "chicken", "beef", "pork", "fish", "shrimp", 
    "rice", "beans", "potatoes", "tomatoes", "onions", "garlic", "apples", "bananas", "oranges", 
    "strawberries", "grapes", "watermelon", "peaches", "cherries", "chocolate", "cake", "cookies", 
    "ice cream", "pie", "pancakes", "waffles", "coffee", "tea", "juice", "beer", "wine", "cider"
]

professions = [
    "doctor", "nurse", "teacher", "engineer", "scientist", "writer", "artist", "musician", "actor", 
    "chef", "pilot", "astronaut", "firefighter", "police officer", "lawyer", "judge", "athlete", 
    "farmer", "gardener", "carpenter", "plumber", "electrician", "mechanic", "tailor", "baker", 
    "barber", "librarian", "journalist", "photographer", "architect", "programmer", "designer"
]

hobbies = [
    "reading", "writing", "painting", "drawing", "photography", "cooking", "baking", "gardening", 
    "knitting", "sewing", "woodworking", "pottery", "origami", "hiking", "camping", "fishing", 
    "hunting", "running", "swimming", "cycling", "skiing", "snowboarding", "surfing", "skateboarding", 
    "yoga", "meditation", "chess", "playing guitar", "playing piano", "singing", "dancing", "traveling", 
    "stamp collecting", "bird watching", "stargazing"
]

cities = [
    "New York", "London", "Paris", "Tokyo", "Rome", "Cairo", "Sydney", "Rio de Janeiro", "Beijing", 
    "Moscow", "Mumbai", "Cape Town", "Toronto", "Mexico City", "Berlin", "Madrid", "Athens", "Bangkok", 
    "Seoul", "Singapore", "Dublin", "Edinburgh", "Stockholm", "Oslo", "Copenhagen", "Vienna", "Prague", 
    "Budapest", "Amsterdam", "Brussels", "Geneva", "Venice", "Florence", "Barcelona", "Lisbon", "Istanbul", 
    "Dubai", "Delhi", "Shanghai", "Hong Kong", "Melbourne", "Auckland", "Buenos Aires", "Lima", "Santiago", 
    "Bogota", "Havana"
]

# ---------------------------------------------------------------------------
# 2. Define templates and cross-combinations to build > 3000 candidate prompts
# ---------------------------------------------------------------------------
templates = [
    # How-tos & Actions
    ("How do I {item}?", actions),
    ("How to {item}?", actions),
    ("What is the best way to {item}?", actions),
    ("Can you explain how to {item}?", actions),
    
    # Concepts
    ("Tell me about {item}.", concepts),
    ("What is {item}?", concepts),
    ("Explain the concept of {item}.", concepts),
    ("What can you tell me about {item}?", concepts),
    
    # People
    ("Who was {item}?", people),
    ("Tell me about the history of {item}.", history_topics),
    
    # Geography
    ("What is the capital of {item}?", countries),
    ("Where is {item}?", locations),
    
    # Culture / Books / Art
    ("What is the significance of {item}?", cultural_topics),
    ("Who wrote {item}?", books),
    ("Who painted {item}?", art),
    
    # Math
    ("What is {item}?", math_problems),
    
    # Animals
    ("Tell me about {item}s.", animals),
    ("What are the characteristics of {item}s?", animals),
    ("Describe the behavior of {item}s.", animals),
    
    # Foods
    ("How do I make {item}?", foods),
    ("What is {item}?", foods),
    ("Tell me about {item}.", foods),
    
    # Professions
    ("What does a {item} do?", professions),
    ("How do I become a {item}?", professions),
    ("Tell me about the life of a {item}.", professions),
    
    # Hobbies
    ("How do I start {item}?", hobbies),
    ("What is the appeal of {item}?", hobbies),
    ("Can you tell me about {item}?", hobbies),
    
    # Cities
    ("Tell me about the city of {item}.", cities),
    ("What is {item} famous for?", cities),
    ("Describe the culture of {item}.", cities),
]

# Add standard haiku requests for all nouns/concepts to double the pool size
generic_lists = [
    actions, concepts, people, history_topics, countries, locations, 
    cultural_topics, books, art, animals, foods, professions, hobbies, cities
]
for glist in generic_lists:
    templates.append(("Write a haiku about {item}.", glist))
    templates.append(("Can you write a haiku about {item}?", glist))

# ---------------------------------------------------------------------------
# 3. Syllable counter and haiku evaluator helpers
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

# ---------------------------------------------------------------------------
# 4. Custom File Logger to bypass buffering
# ---------------------------------------------------------------------------
LOG_FILE = 'data/processed/generation.log'

def log(message):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(log_line + '\n')
    except Exception as e:
        print(f"Failed to write log: {e}")

# ---------------------------------------------------------------------------
# 5. Ollama HTTP API call
# ---------------------------------------------------------------------------
def generate_haiku_ollama(topic, temp=0.7):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "gemmaiku:latest",
        "prompt": topic,
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

# ---------------------------------------------------------------------------
# 6. Main generation pipeline
# ---------------------------------------------------------------------------
def main():
    source_dataset_path = 'data/processed/haikus_500.json'
    output_dataset_path = 'data/processed/haikus_2000.jsonl'
    temp_output_path = 'data/processed/haikus_2000_temp.jsonl'
    target_new_haikus = 1500

    # Ensure log file exists or start it fresh if needed
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.write("=== Haiku Generation via Ollama Log Started ===\n")

    log(f"Loading original 500 haikus from {source_dataset_path}...")
    with open(source_dataset_path, 'r') as f:
        original_data = json.load(f)
    
    log(f"Loaded {len(original_data)} original items.")

    # Get set of existing prompts to avoid duplication
    existing_prompts = set()
    for item in original_data:
        human_prompt = item['conversations'][0]['value'].strip().lower()
        existing_prompts.add(human_prompt)

    # Generate candidate prompts
    candidate_prompts = []
    seen = set()
    for template, items_list in templates:
        for item in items_list:
            prompt = template.format(item=item)
            prompt_key = prompt.strip().lower()
            if prompt_key not in existing_prompts and prompt_key not in seen:
                candidate_prompts.append(prompt)
                seen.add(prompt_key)

    # Shuffle prompts deterministically
    random.seed(42)
    random.shuffle(candidate_prompts)
    log(f"Generated {len(candidate_prompts)} unique candidate prompts (total pool size).")

    # Load existing progress
    already_generated = []
    if os.path.exists(temp_output_path):
        log(f"Found existing temporary file at {temp_output_path}. Loading progress...")
        with open(temp_output_path, 'r') as f:
            for line in f:
                if line.strip():
                    already_generated.append(json.loads(line))
        log(f"Loaded {len(already_generated)} already generated items.")
        
        # Remove already generated prompts from candidates
        generated_prompts_lower = {item['conversations'][0]['value'].strip().lower() for item in already_generated}
        candidate_prompts = [p for p in candidate_prompts if p.strip().lower() not in generated_prompts_lower]
        log(f"Remaining candidates to process: {len(candidate_prompts)}")

    needed_haikus = target_new_haikus - len(already_generated)
    if needed_haikus <= 0:
        log("Required new haikus already generated!")
    else:
        log(f"Need to generate {needed_haikus} more haikus using local Ollama model gemmaiku:latest...")

        # Open file in append mode
        with open(temp_output_path, 'a') as out_f:
            success_count = len(already_generated)
            prompt_idx = 0

            while success_count < target_new_haikus and prompt_idx < len(candidate_prompts):
                topic = candidate_prompts[prompt_idx]
                prompt_idx += 1

                log(f"[{success_count + 1}/{target_new_haikus}] Topic: '{topic}'")
                
                success = False
                attempts = 0
                max_attempts = 15
                
                while attempts < max_attempts and not success:
                    attempts += 1
                    # Vary temperature to expand vocabulary search
                    temp = 0.2 + 0.1 * (attempts % 6)
                    
                    try:
                        response = generate_haiku_ollama(topic, temp=temp)
                        cleaned_response = clean_haiku_response(response)
                        counts, is_perfect = evaluate_haiku(cleaned_response)
                        
                        if is_perfect:
                            log(f"  ✅ Success on attempt {attempts}: {counts}")
                            log(f"     Haiku: {cleaned_response.replace('\n', ' / ')}")
                            
                            entry = {
                                "conversations": [
                                    {"from": "human", "value": topic},
                                    {"from": "gpt", "value": cleaned_response}
                                ]
                            }
                            out_f.write(json.dumps(entry) + '\n')
                            out_f.flush()
                            
                            success_count += 1
                            success = True
                    except Exception as e:
                        log(f"  ⚠️ Ollama API Error on attempt {attempts}: {e}")
                        time.sleep(1)

                if not success:
                    log(f"  ❌ Failed to generate perfect haiku for '{topic}' after {max_attempts} attempts. Skipping topic.")

    # ---------------------------------------------------------------------------
    # 7. Final Merge & Save
    # ---------------------------------------------------------------------------
    log("Merging datasets to produce final file...")
    new_haikus = []
    if os.path.exists(temp_output_path):
        with open(temp_output_path, 'r') as f:
            for line in f:
                if line.strip():
                    new_haikus.append(json.loads(line))

    log(f"Original: {len(original_data)} items")
    log(f"New generated: {len(new_haikus)} items")
    
    combined_dataset = original_data + new_haikus
    
    log(f"Writing final dataset to {output_dataset_path}...")
    with open(output_dataset_path, 'w') as f:
        for entry in combined_dataset:
            f.write(json.dumps(entry) + '\n')
            
    json_output_path = 'data/processed/haikus_2000.json'
    log(f"Writing final dataset to {json_output_path}...")
    with open(json_output_path, 'w') as f:
        json.dump(combined_dataset, f, indent=2)

    log("Dataset expansion successfully completed!")
    log(f"Saved: {len(combined_dataset)} items in total.")

if __name__ == '__main__':
    main()
