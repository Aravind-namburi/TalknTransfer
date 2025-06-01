# TalknTransfer

A peer-to-peer socket-based chat application that supports real-time messaging and file transfers. Built using Python and multithreading.

## Description

This project demonstrates the fundamentals of socket programming by implementing a simple chat program. Two users (e.g., Alice and Bob) can run the program, connect using port numbers, and start exchanging messages. Additionally, files can be transferred using a special command.

## How to Run

### Prerequisites
- Python 3.x installed on your system

### Steps
1. Open **two terminals** — one for Alice and one for Bob.
2. Run the following command in both terminals:
   ```bash
   python3 main.py
   ```
3. Each instance will prompt you to:
   - Enter a **name**.
   - The program will display the **server port** it's listening on.
4. Now, enter the **target port** from the other instance to establish a connection.

   - Example:
     - Alice sees port 5000, Bob sees port 6000.
     - Alice enters `6000`, Bob enters `5000`.

5. Once connected:
   - Type messages and hit Enter to chat.
   - Use the following command to transfer a file:
     ```bash
     transfer <filename>
     ```

     Example:
     ```bash
     transfer sample.txt
     ```
   - The file will be saved as `new_sample.txt` on the receiver's side.

6. To exit, type:
   ```bash
   exit
   ```

## Features

- Real-time bidirectional messaging
- File transfer using TCP sockets
- Multithreaded design (separate read and write threads)
- Automatic server port allocation
- Cross-platform compatibility (Windows, macOS, Linux)

## Technologies Used

- Python 3
- `socket` module
- `threading` module

## File Structure

- `main.py`: The main application script
- `README.md`: Project documentation

## Authors

- Aravind Namburi
- Course: CNT 5106 - Computer Network Fundamentals
- University of Florida

## Notes

- Only works over `localhost` for local demo purposes.
- Make sure the file you want to send exists in the current directory.
- Received files are prefixed with `new_` to avoid overwriting.

---
