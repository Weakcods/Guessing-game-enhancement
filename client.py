import socket

HOST = "127.0.0.1"
PORT = 12345

def bot_play(s):
    """ The bot plays the guessing game optimally using binary search. """
    print("🤖 Bot is playing...")
    
    difficulty_prompt = s.recv(1024).decode()
    print(difficulty_prompt)
    difficulty = input("Choose difficulty level (a/b/c): ").strip()
    s.sendall(difficulty.encode())
    
    # Set range based on difficulty
    ranges = {'a': (1, 50), 'b': (1, 100), 'c': (1, 500)}
    low, high = ranges.get(difficulty, (1, 500))
    tries = 0

    while True:
        bot_guess = (low + high) // 2
        tries += 1
        print(f"🤖 Bot guess #{tries}: {bot_guess}")
        s.sendall(str(bot_guess).encode())

        response = s.recv(1024).decode()
        print(response)

        if "won" in response or "Congratulations" in response:
            print(f"🏆 Bot has won in {tries} attempts!")
            # Handle leaderboard display
            if "Leaderboard" in response:
                print(response)
            break

        if "Too high" in response:
            high = bot_guess - 1
        elif "Too low" in response:
            low = bot_guess + 1

def manual_play(s):
    """ Human player mode with scoring system feedback. """
    difficulty_prompt = s.recv(1024).decode()
    print(difficulty_prompt)
    difficulty = input("Choose difficulty level (a/b/c): ").strip()
    s.sendall(difficulty.encode())

    while True:
        prompt = s.recv(1024).decode()
        print(prompt)

        # Check for game completion messages with ratings
        if any(rating in prompt for rating in ["Excellent", "Very Good", "Good/Fair"]):
            if "enter your name" in prompt.lower():
                name = input("Enter your name for the leaderboard: ")
                s.sendall(name.encode())
                # Display final leaderboard
                leaderboard = s.recv(1024).decode()
                print("\n" + leaderboard)
            break

        guess = input("🎯 Enter your guess: ")
        s.sendall(guess.encode())

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("🎮 Connected to the game server!")

            # Handle password authentication
            password_prompt = s.recv(1024).decode()
            print(password_prompt)
            user_password = input("🔒 Enter password: ")
            s.sendall(user_password.encode())

            auth_response = s.recv(1024).decode()
            print(auth_response)

            if "Incorrect password" in auth_response:
                return

            # Game mode selection
            mode_prompt = s.recv(1024).decode()
            print(mode_prompt)
            
            while True:
                try:
                    mode_choice = input().strip().lower()
                    if mode_choice in ['manual', 'bot']:
                        s.sendall(mode_choice.encode())
                        break
                    print("⚠ Invalid choice! Please type exactly 'manual' or 'bot'")
                except EOFError:
                    print("⚠ Error reading input. Please try again.")
                except Exception as e:
                    print(f"⚠ An error occurred: {e}")
                    break

            if mode_choice == "bot":
                bot_play(s)
            else:
                manual_play(s)

        except ConnectionRefusedError:
            print("❌ Cannot connect to the server. Is it running?")
        except Exception as e:
            print(f"❌ An error occurred: {e}")

def client():
    try:
        main()
    except ConnectionRefusedError:
        print("❌ Unable to connect to the server. Please make sure the server is running.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        print("👋 Thanks for playing! See you next time!")

if __name__ == "__main__":
    client()