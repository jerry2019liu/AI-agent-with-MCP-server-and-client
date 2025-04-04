import socket
import threading

def handle_client(client_socket):
    try:
        # Receive message length (4-byte header)
        raw_msg_len = client_socket.recv(4)
        if not raw_msg_len:
            return
        msg_len = int.from_bytes(raw_msg_len, byteorder='big')
        
        # Receive full message
        data = b''
        while len(data) < msg_len:
            packet = client_socket.recv(msg_len - len(data))
            if not packet:
                break
            data += packet
        
        # Process data with "AI model" (string reversal for demo)
        input_str = data.decode('utf-8')
        response_str = input_str[::-1]  # Replace with actual model inference
        
        # Prepare response
        response_bytes = response_str.encode('utf-8')
        response_len = len(response_bytes).to_bytes(4, byteorder='big')
        
        # Send response
        client_socket.send(response_len + response_bytes)
    
    finally:
        client_socket.close()

def start_server(host='127.0.0.1', port=9999):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] MCP Server listening on {host}:{port}")
    
    try:
        while True:
            client_sock, addr = server.accept()
            print(f"[+] Accepted connection from {addr[0]}:{addr[1]}")
            client_handler = threading.Thread(
                target=handle_client, 
                args=(client_sock,)
            )
            client_handler.start()
    except KeyboardInterrupt:
        print("\n[*] Shutting down server...")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
