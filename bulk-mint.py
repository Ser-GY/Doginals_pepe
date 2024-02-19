import sys
import subprocess
import time

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print("Output from command:")
    print(result.stdout)
    if result.stderr:
        print("Error in command:")
        print(result.stderr)
    return result

def main():
    # Print received command-line arguments for debugging
    print("Received arguments:", sys.argv)

    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 6:
        print(f"Received {len(sys.argv) - 1} arguments, but expected 5.")
        print("Usage: python3 bulk-mint.py <address> <ticker> <amount> <interval_seconds> <num_loops>")
        sys.exit(1)

    # Extract command-line arguments
    address = sys.argv[1]
    ticker = sys.argv[2]
    amount = sys.argv[3]
    interval_seconds = int(sys.argv[4])
    num_loops = int(sys.argv[5])

    print("Address:", address)
    print("Ticker:", ticker)
    print("Amount:", amount)
    print("Interval Seconds:", interval_seconds)
    print("Number of Loops:", num_loops)

    # Loop for the specified number of times
    for _ in range(num_loops):
        # Construct the command to mint tokens
        mint_command = ["node", ".", "drc-20", "mint", address, ticker, str(amount)]

        # Run the minting command
        result_mint = run_command(mint_command)

        # Wait for the specified interval before the next iteration
        time.sleep(interval_seconds)

if __name__ == "__main__":
    main()
