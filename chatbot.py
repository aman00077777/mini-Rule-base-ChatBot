import os
import random

# ==========================================
# 1. Configuration and Data Storage
# ==========================================
LEARNED_DATA_FILE = "learned_responses.txt"

# Predefined intents (at least 20)
INTENTS = {
    "greeting": {"keywords": ["hello", "hi", "hey", "greetings", "sup"], "responses": ["Hello! How's it going?", "Hi there!", "Greetings!"]},
    "goodbye": {"keywords": ["bye", "goodbye", "see ya", "quit", "exit", "stop"], "responses": ["Goodbye!", "See you later!", "Take care!"]},
    "how_are_you": {"keywords": ["how are you", "how do you do", "how are things"], "responses": ["I'm just a script, but I'm doing great! How about you?", "I'm functioning perfectly."]},
    "name": {"keywords": ["what is your name", "who are you", "your name"], "responses": ["I am a Python rule-based chatbot.", "You can call me PyBot."]},
    "age": {"keywords": ["how old are you", "your age"], "responses": ["I was born just a moment ago.", "Age is just a number!"]},
    "creator": {"keywords": ["who made you", "who created you", "your creator"], "responses": ["I was created by Aman Sharma.", "Aman Sharma coded me."]},
    "help": {"keywords": ["help", "support", "assist"], "responses": ["Sure, I can help! Try talking to me, or type 'learn' to teach me something new.", "How can I assist you today?"]},
    "joke": {"keywords": ["tell me a joke", "funny", "make me laugh"], "responses": ["Why do programmers prefer dark mode? Because light attracts bugs!", "There are 10 types of people: those who understand binary, and those who don't."]},
    "study": {"keywords": ["study", "learn", "homework", "assignment"], "responses": ["Remember to take breaks while studying!", "Focus is key. You've got this!"]},
    "weather": {"keywords": ["weather", "rain", "sun", "cloudy", "hot", "cold"], "responses": ["I can't check the weather, but I hope it's nice where you are!", "Look outside!"]},
    "food": {"keywords": ["eat", "food", "hungry", "dinner", "lunch", "breakfast"], "responses": ["I don't eat, but pizza sounds good!", "Make sure to stay hydrated and eat well."]},
    "hobbies": {"keywords": ["hobby", "what do you do", "fun"], "responses": ["I enjoy chatting and learning new phrases from you.", "Processing text is my favorite game."]},
    "music": {"keywords": ["music", "song", "sing", "listen"], "responses": ["I love the sound of keystrokes.", "What's your favorite genre?"]},
    "movies": {"keywords": ["movie", "film", "watch", "cinema"], "responses": ["I like sci-fi movies, especially ones with AI!", "Grab some popcorn!"]},
    "sports": {"keywords": ["sport", "play", "game", "football", "tennis", "cricket"], "responses": ["I'm not very athletic, being a piece of software.", "Esports are my kind of sports."]},
    "sleep": {"keywords": ["sleep", "tired", "bed", "night"], "responses": ["Good night! Have a great sleep.", "Rest is important. Catch some Z's!"]},
    "morning": {"keywords": ["morning", "wake up", "good morning"], "responses": ["Good morning! Have a productive day.", "Rise and shine!"]},
    "evening": {"keywords": ["evening", "good evening"], "responses": ["Good evening! Hope you had a nice day.", "Time to wind down."]},
    "thanks": {"keywords": ["thank you", "thanks", "appreciate"], "responses": ["You're welcome!", "Anytime!", "Glad I could help."]},
    "insult": {"keywords": ["stupid", "idiot", "bad", "dumb"], "responses": ["That's not very nice. Let's keep it positive.", "I'm still learning, please be patient!"]}
}

# Mood dictionaries
MOODS = {
    "happy": ["happy", "great", "awesome", "good", "fantastic", "amazing", "love", "excellent", "yay"],
    "sad": ["sad", "depressed", "bad", "terrible", "cry", "unhappy", "pain", "awful"],
    "angry": ["angry", "mad", "furious", "hate", "annoyed", "frustrated", "irritated"]
}


# ==========================================
# 2. File Handling for Learning Mode
# ==========================================
def load_learned_responses(filename):
    """Loads learned responses from a text file."""
    learned = {}
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '|' in line:
                    keyword, response = line.split('|', 1)
                    learned[keyword.lower()] = response
    return learned

def save_learned_response(filename, keyword, response):
    """Saves a new learned response to the text file."""
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"{keyword.lower()}|{response}\n")


# ==========================================
# 3. Core Chatbot Logic
# ==========================================
def detect_mood(user_input):
    """Detects the user's mood based on keywords."""
    words = user_input.lower().split()
    for word in words:
        if word in MOODS["happy"]:
            return "happy"
        elif word in MOODS["sad"]:
            return "sad"
        elif word in MOODS["angry"]:
            return "angry"
    return "neutral"

def find_intent(user_input):
    """Finds the best matching intent based on keywords."""
    user_input_lower = user_input.lower()
    for intent, data in INTENTS.items():
        for keyword in data["keywords"]:
            if keyword in user_input_lower:
                return intent
    return None

def find_learned_response(user_input, learned_data):
    """Finds a response from the user-taught database."""
    user_input_lower = user_input.lower()
    for keyword, response in learned_data.items():
        if keyword in user_input_lower:
            return response
    return None

def generate_response(user_input, context, learned_data):
    """Generates a response considering mood, context, learned rules, and intents."""
    mood = detect_mood(user_input)
    
    # 1. Mood-based overrides
    if mood == "sad":
        return "I sense that you're feeling down. I'm here for you. Tell me more."
    elif mood == "angry":
        return "You seem upset. Taking a deep breath might help. Let's talk calmly."
    
    # 2. Context-based overrides
    if len(context) > 0:
        last_intent = context[-1]
        if last_intent == "joke" and ("good" in user_input.lower() or "haha" in user_input.lower()):
            context.append("reaction") # Update context
            return "Glad you liked the joke! Want another one?"
            
    # 3. Check learned responses first
    learned_resp = find_learned_response(user_input, learned_data)
    if learned_resp:
        return f"[Learned] {learned_resp}"
        
    # 4. Check predefined intents
    intent = find_intent(user_input)
    if intent:
        context.append(intent)
        
        # Adjust response slightly based on happy mood
        base_response = random.choice(INTENTS[intent]["responses"])
        if mood == "happy":
            return f"That's great energy! {base_response}"
        return base_response
        
    # 5. Fallback response
    return "I'm not sure how to respond to that. You can type 'learn' to teach me!"


# ==========================================
# 4. Main Chat Loop & Interface
# ==========================================
def run_chatbot():
    print("=====================================================")
    print("🤖 Welcome to PyBot - The Core Python Chatbot!")
    print("Type 'quit' or 'exit' to stop.")
    print("Type 'learn' to teach me a new response.")
    print("=====================================================")
    
    # Load any previously learned info
    learned_data = load_learned_responses(LEARNED_DATA_FILE)
    context = [] # List to store conversation history
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
                
            input_lower = user_input.lower()
            
            # Exit condition
            if input_lower in INTENTS["goodbye"]["keywords"]:
                print(f"PyBot: {random.choice(INTENTS['goodbye']['responses'])}")
                break
                
            # Learning mode
            if input_lower == "learn":
                print("PyBot: Awesome! Entering learning mode.")
                new_keyword = input("What keyword or phrase should I listen for? ").strip()
                if new_keyword:
                    new_response = input(f"What should I say when you type '{new_keyword}'? ").strip()
                    if new_response:
                        save_learned_response(LEARNED_DATA_FILE, new_keyword, new_response)
                        learned_data[new_keyword.lower()] = new_response
                        print(f"PyBot: Got it! I've learned to respond to '{new_keyword}'.")
                    else:
                        print("PyBot: Response cannot be empty. Learning cancelled.")
                else:
                    print("PyBot: Keyword cannot be empty. Learning cancelled.")
                continue

            # Generate and print response
            response = generate_response(user_input, context, learned_data)
            print(f"PyBot: {response}")
            
            # Keep context size manageable (last 5 intents)
            if len(context) > 5:
                context = context[-5:]
                
        except (KeyboardInterrupt, EOFError):
            print("\nPyBot: System interrupted. Goodbye!")
            break

if __name__ == "__main__":
    run_chatbot()
