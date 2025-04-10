# Number Guessing Game 🎮

A client-server based number guessing game with multiple difficulty levels, bot play, and a leaderboard system.

## 🔑 Game Access
- **Password**: `Joshua`

## 🚀 Getting Started

### Prerequisites
- Python 3.x installed on your system
- Basic understanding of terminal/command prompt usage

### Running the Game

1. First, start the server:
```bash
python server.py
```

2. Then, in a new terminal window, start the client:
```bash
python client.py
```

## 🎯 How to Play

1. When you start the client, you'll be prompted to enter the password
2. After successful authentication, you can choose between two game modes:
   - `manual`: Play the game yourself
   - `bot`: Let an AI play optimally using binary search

3. Select a difficulty level:
   - `a`: Numbers between 1-50
   - `b`: Numbers between 1-100
   - `c`: Numbers between 1-500

4. Start guessing! The game will tell you if your guess is too high or too low

## 🏆 Performance Rating System

Your performance is rated based on the number of attempts:
- **Excellent**: 1-5 guesses
- **Very Good**: 6-20 guesses
- **Good/Fair**: 21+ guesses

## 📊 Leaderboard

The game maintains a leaderboard that tracks:
- Player name
- Number of attempts
- Difficulty level

The leaderboard is automatically updated after each successful game completion.

## 🤖 Bot Mode

The bot uses an optimal binary search algorithm to find the number in the most efficient way possible. It's a great way to learn optimal guessing strategies!

## 🔍 Tips for Success

1. Use binary search strategy - guess in the middle of the possible range
2. Remember your previous guesses and adjust accordingly
3. The smaller the range (easier difficulty), the better chance for an "Excellent" rating

## ⚠️ Troubleshooting

If you can't connect to the server:
1. Make sure the server is running first
2. Verify that no other program is using port 12345
3. Check that your firewall isn't blocking the connection