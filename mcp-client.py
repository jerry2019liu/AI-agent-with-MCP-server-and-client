import socket

class MCPClient:
    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port
    
    def send_request(self, input_data):
        # Create socket and connect
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((self.host, self.port))
        
        try:
            # Prepare data
            data_bytes = input_data.encode('utf-8')
            data_len = len(data_bytes).to_bytes(4, byteorder='big')
            
            # Send request
            client_sock.send(data_len + data_bytes)
            
            # Receive response length
            raw_resp_len = client_sock.recv(4)
            resp_len = int.from_bytes(raw_resp_len, byteorder='big')
            
            # Receive response data
            response = b''
            while len(response) < resp_len:
                packet = client_sock.recv(resp_len - len(response))
                if not packet:
                    break
                response += packet
            
            return response.decode('utf-8')
        
        finally:
            client_sock.close()

if __name__ == "__main__":
    client = MCPClient()
    response = client.send_request("Hello MCP Server!")
    print(f"Server response: {response}")
    # Should print: "!revreP SCPM olleH"
