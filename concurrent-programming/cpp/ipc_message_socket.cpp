// #include <iostream>
// #include <cstring>  // For memset()
// #include <sys/socket.h>
// #include <sys/un.h> // For local file sockets
// #include <unistd.h> // For close(), unlink()
// #include <thread>
// #include <chrono>

// const char* SOCKET_FILE_PATH = "./mailBox";

// class Client
// {
// public:
//     Client()
//     {
//         m_Socket = socket(AF_UNIX, SOCK_STREAM, 0);
//         if (m_Socket == -1)
//         {
//             perror("Client: Socket creation failed");
//             exit(EXIT_FAILURE);
//         }

//         memset(&m_Client, 0, sizeof(m_Client));
//         m_Client.sun_family = AF_UNIX;
//         strncpy(m_Client.sun_path, SOCKET_FILE_PATH, sizeof(m_Client.sun_path) - 1);
//     }

//     void SendMessageLoop(int numMessages)
//     {
//         int messageCount = 1;
//         while (messageCount < numMessages)
//         {
//             int sock = socket(AF_UNIX, SOCK_STREAM, 0);
//             if (connect(sock, (struct sockaddr*)&m_Client, sizeof(m_Client)) == -1)
//             {
//                 perror("Client: Connection failed");
//                 close(sock);
//                 return;
//             }

//             std::string message = "Message " + std::to_string(messageCount++);
//             send(sock, message.c_str(), message.size(), 0);
//             close(sock);

//             std::this_thread::sleep_for(std::chrono::milliseconds(60));
//         }
//         ++messageCount;
//     }

// private:
//     int m_Socket;
//     struct sockaddr_un m_Client;
// };

// class Server
// {
// public:
//     Server()
//     {
//         m_Socket = socket(AF_UNIX, SOCK_STREAM, 0);
//         if (m_Socket == -1)
//         {
//             perror("Server: Socket creation failed");
//             exit(EXIT_FAILURE);
//         }

//         memset(&m_Server, 0, sizeof(m_Server));
//         m_Server.sun_family = AF_UNIX;
//         strncpy(m_Server.sun_path, SOCKET_FILE_PATH, sizeof(m_Server.sun_path) - 1);

//         unlink(SOCKET_FILE_PATH);

//         if (bind(m_Socket, (struct sockaddr*)&m_Server, sizeof(m_Server)) == -1)
//         {
//             perror("Server: Bind failed");
//             close(m_Socket);
//             exit(EXIT_FAILURE);
//         }

//         if (listen(m_Socket, 5) == -1)
//         {
//             perror("Server: Listen failed");
//             close(m_Socket);
//             exit(EXIT_FAILURE);
//         }
//     }

//     ~Server()
//     {
//         close(m_Socket);
//         unlink(SOCKET_FILE_PATH);
//     }

//     void ReceiveMessage()
//     {
//         while (true)
//         {
//             std::cout << "Server: Waiting for a client...\n";

//             int clientSocket = accept(m_Socket, nullptr, nullptr);
//             if (clientSocket == -1)
//             {
//                 perror("Server: Accept failed");
//                 continue;
//             }

//             char messageBuffer[1024] = {0};
//             recv(clientSocket, messageBuffer, sizeof(messageBuffer), 0);
//             std::cout << "Server received: " << messageBuffer << "\n";

//             close(clientSocket);
//         }
//     }

// private:
//     int m_Socket;
//     struct sockaddr_un m_Server;
// };

// int main()
// {
//     Server server;
//     std::thread serverThread(&Server::ReceiveMessage, &server); // not server.ReceiveMessage (binded funciton only can be used as function call)

//     sleep(1); // system sleep

//     Client client;
//     std::thread clientThread(&Client::SendMessageLoop, &client, 10);

//     serverThread.join();
//     clientThread.join();

// }
