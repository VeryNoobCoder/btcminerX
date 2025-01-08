from flask import Flask, render_template, request, redirect, url_for
import random
import time
from threading import Thread

app = Flask(__name__)

# Global variables
is_mining = False
wallet_address = ""
simulation_output = []
ascii_art = """
  ____ _______ _____ __  __ _____ _   _ ______ _____  
 |  _ \__   __/ ____|  \/  |_   _| \ | |  ____|  __ \ 
 | |_) | | | | |    | \  / | | | |  \| | |__  | |__) |
 |  _ <  | | | |    | |\/| | | | | . ` |  __| |  _  / 
 | |_) | | | | |____| |  | |_| |_| |\  | |____| | \ \ 
 |____/  |_|  \_____|_|  |_|_____|_| \_|______|_|  \_\
                                                      
          
                                        ~Created by @tjm.builds on Snapchat and IG              
"""

# Random word list for seed phrases
words = [
    "robot", "tree", "unicorn", "water", "elephant", "cactus", "mountain", "guitar",
    "alligator", "camera", "pencil", "marker", "dinosaur", "telephone", "mouse", 
    "computer", "rocket", "spaceship", "galaxy", "river", "forest", "tiger", "piano"
]

# Function to generate a random wallet address
def generate_wallet_address(length=42):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(chars) for _ in range(length))

# Function to generate a random seed phrase
def generate_seed_phrase():
    return ' '.join(random.sample(words, 12))

# Mining simulation logic
def mining_simulation():
    global is_mining, simulation_output
    is_mining = True
    simulation_output = []  # Clear previous output

    # Random number of lines between 2000 and 4000
    max_lines = random.randint(2000, 4000)
    simulation_output.append(f"Mining in progress... (Will stop after {max_lines} attempts)")

    # Simulate mining process
    for i in range(max_lines):
        if not is_mining:
            break  # Stop if mining is canceled
        # Generate wallet address or seed phrase alternately
        if i % 2 == 0:
            simulation_output.append(f"Attempting to crack wallet address: {generate_wallet_address()}")
        else:
            simulation_output.append(f"Attempting to crack seed phrase: {generate_seed_phrase()}")
        time.sleep(0.01)  # Simulate delay

    if is_mining:
        simulation_output.append('<span style="color: orange;">Successfully mined 1 BTC. Bitcoin deposited to your wallet.</span>')

    is_mining = False

@app.route("/", methods=["GET", "POST"])
def home():
    global wallet_address, simulation_output

    if request.method == "POST":
        wallet_address = request.form.get("wallet")
        # Start mining in a separate thread
        miner_thread = Thread(target=mining_simulation)
        miner_thread.start()
        return redirect(url_for("mining"))

    return render_template("home.html", ascii_art=ascii_art)

@app.route("/mining")
def mining():
    return render_template("mining.html", simulation_output=simulation_output, mining=is_mining)

@app.route("/stop")
def stop():
    global is_mining
    is_mining = False
    return redirect(url_for("home"))

# Main entry point
if __name__ == "__main__":
    app.run(debug=True)
