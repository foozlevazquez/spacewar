import asyncio
import json


# Game state management (simplified)
class GameState:
    def __init__(self):
        self.players = {}  # Player IDs and their data (e.g., position)

    def update_player_position(self, player_id, x, y):
        if player_id in self.players:
            self.players[player_id]["x"] = x
            self.players[player_id]["y"] = y
        else:
            self.players[player_id] = {"x": x, "y": y}

    def get_state(self):
        return self.players


game_state = GameState()


async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"Client connected: {addr}")

    player_id = f"player_{addr[1]}"  # Simple ID for demonstration

    try:
        while True:
            # Receive data from client
            data = await reader.read(1024)
            if not data:
                break
            message = data.decode().strip()
            print(f"Received from {addr}: {message}")

            # Process client message (e.g., player movement)
            try:
                command = json.loads(message)
                if command["type"] == "move":
                    game_state.update_player_position(
                        player_id, command["x"], command["y"]
                    )
                    # Broadcast updated state to all connected clients (not implemented here for brevity)
                    response = json.dumps(
                        {"status": "ok", "game_state": game_state.get_state()}
                    )
                    writer.write(response.encode())
                    await writer.drain()
            except json.JSONDecodeError:
                print(f"Invalid JSON from {addr}: {message}")

    except asyncio.CancelledError:
        pass  # Handle client disconnection gracefully
    finally:
        print(f"Client disconnected: {addr}")
        writer.close()
        await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_client, "0.0.0.0", 18888)

    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Serving on {addrs}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
