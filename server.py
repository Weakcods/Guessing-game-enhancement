import socket
import random
import json


difficulty = 'a'
last_difficulty = 'a'
host = '127.0.0.1'
port = 12345
banner = """
🎮 Welcome to the Number Guessing Game! 🎮

Please select your mode:
👤 Manual - Play the game yourself
🤖 Bot - Let an AI guess optimally
Type 'manual' or 'bot' to begin: """

def generate_random_int(difficulty):
    if difficulty == 'a':
        return random.randint(1, 50)
    elif difficulty == 'b':
        return random.randint(1, 100)
    elif difficulty == 'c':
        return random.randint(1, 500)

def update_leaderboard(name, score, difficulty, leaderboard):
    leaderboard.append({"name": name, "score": score, "difficulty": difficulty})
    leaderboard.sort(key=lambda x: x["score"])
    return leaderboard[:10]

def save_leaderboard(leaderboard):
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f)

def load_leaderboard():
    try:
        with open("leaderboard.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def filter_leaderboard_by_difficulty(leaderboard, difficulty):
    return [entry for entry in leaderboard if entry["difficulty"] == difficulty]

def format_leaderboard(leaderboard):
    formatted = "🏆 Top Players 🏆\n"
    for i, entry in enumerate(leaderboard, 1):
        formatted += f"{i}. Player: {entry['name']}, Attempts: {entry['score']}\n"
    return formatted

PASSWORD = "Joshua"

def authenticate(conn):
    conn.sendall("🔒 Please enter the password to play: ".encode('utf-8'))
    
    try:
        entered_password = conn.recv(1024).decode('utf-8').strip()
        
        if entered_password == PASSWORD:
            conn.sendall("✅ Access granted! Let's play!\n".encode('utf-8'))
            return True
        else:
            conn.sendall("❌ Incorrect password. Connection closing...\n".encode('utf-8'))
            return False
    except:
        return False

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)

    print(f"🚀 Server is running on {host}:{port}")
    
    while True:
        try:
            print("Waiting for connection...")
            conn, addr = s.accept()
            print(f"New client connected: {addr[0]}")
            
            if not authenticate(conn):
                conn.close()
                continue
                
            conn.sendall(banner.encode('utf-8'))
            mode = conn.recv(1024).decode().strip()

            if mode == "bot":
                bot_guessing_game(conn)
            elif mode == "manual":
                manual_guessing_game(conn)
            else:
                conn.sendall("❌ Invalid choice! Please enter 'manual' or 'bot'.".encode('utf-8'))
        except Exception as e:
            print(f"Error handling connection: {e}")
        finally:
            if conn:
                conn.close()

def bot_guessing_game(conn):
    """ The bot plays using binary search. """
    conn.sendall("🎮 Choose difficulty (a/b/c): ".encode('utf-8'))
    difficulty = conn.recv(1024).decode().strip()
    
    low, high = 1, 50 if difficulty == 'a' else 100 if difficulty == 'b' else 500
    guessme = random.randint(low, high)  # Random target number
    tries = 0
    leaderboard = load_leaderboard()

    conn.sendall("🤖 Bot is playing...\n".encode('utf-8'))

    while True:
        bot_guess = (low + high) // 2  # Binary search optimization
        tries += 1
        conn.sendall(f"🤖 Bot guesses: {bot_guess}\n".encode('utf-8'))

        if bot_guess == guessme:
            # Determine performance rating
            if tries <= 5:
                rating = "Excellent"
            elif tries <= 20:
                rating = "Very Good"
            else:
                rating = "Good/Fair"
                
            conn.sendall(f"🎉 {rating}! Bot won in {tries} attempts!\n".encode('utf-8'))
            # Add bot to leaderboard
            update_leaderboard("Bot-Player", tries, difficulty, leaderboard)
            save_leaderboard(leaderboard)
            
            # Show leaderboard
            conn.sendall(("\nLeaderboard:\n" + format_leaderboard(filter_leaderboard_by_difficulty(leaderboard, difficulty))).encode('utf-8'))
            break
        elif bot_guess > guessme:
            high = bot_guess - 1
            conn.sendall("📉 Too high! Adjusting...\n".encode('utf-8'))
        elif bot_guess < guessme:
            low = bot_guess + 1
            conn.sendall("📈 Too low! Adjusting...\n".encode('utf-8'))

    conn.close()


def manual_guessing_game(conn):
    """ Standard guessing game for human players. """
    conn.sendall("🎮 Choose difficulty (a/b/c): ".encode('utf-8'))
    difficulty = conn.recv(1024).decode().strip()
    guessme = generate_random_int(difficulty)
    tries = 0
    leaderboard = load_leaderboard()
    conn.sendall("🎯 Enter your guess: ".encode('utf-8'))

    while True:
        client_input = conn.recv(1024).decode().strip()

        if client_input.isdigit():
            guess = int(client_input)
            tries += 1

            if guess == guessme:
                # Determine performance rating
                if tries <= 5:
                    rating = "Excellent"
                elif tries <= 20:
                    rating = "Very Good"
                else:
                    rating = "Good/Fair"
                
                conn.sendall(f"🎉 {rating}! You won in {tries} attempts!\nPlease enter your name: ".encode('utf-8'))
                name = conn.recv(1024).decode().strip()
                update_leaderboard(name, tries, difficulty, leaderboard)
                save_leaderboard(leaderboard)
                
                # Show leaderboard
                conn.sendall(("\nLeaderboard:\n" + format_leaderboard(filter_leaderboard_by_difficulty(leaderboard, difficulty))).encode('utf-8'))
                break
            elif guess > guessme:
                conn.sendall("📉 Too high! Try a lower number: ".encode('utf-8'))
            elif guess < guessme:
                conn.sendall("📈 Too low! Try a higher number: ".encode('utf-8'))
        else:
            conn.sendall("❌ Invalid input! Enter a number: ".encode('utf-8'))

    conn.close()

def server():
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
    if WindowsError:
        print("Windows Error.")



if __name__ == "__main__":
    server()