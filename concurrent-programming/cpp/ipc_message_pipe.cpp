// #include <iostream>
// #include <thread>
// #include <string>
// #include <chrono>
// #include <vector>
// #include <sstream>
// #include <cstring>
// // UNIX dependency - POSIX . Not working in Windows
// #include <unistd.h> // for pipe(), write(), read()

// #include "Timer.h"

// struct ThreadMessage
// {
//     int messageNumber;
//     std::string message;
// };

// class PipedThread
// {
// public:
//     PipedThread(std::string name, int pipeNum, int numMessages, void(*threadJob)(int, int)) // use function pointer
//     :m_Name(name)
//     ,m_PipeNum(pipeNum)
//     ,m_Thread(threadJob, pipeNum, numMessages)
//     {
//         std::cout << "Initiated " << m_Name <<" Thread: " << std::this_thread::get_id() << "\n";
//     }
//     void Join()
//     {
//         m_Thread.join();
//     }
// private:
//     std::string m_Name;
//     std::thread m_Thread;
//     int m_PipeNum;
// };

// void WriteToPipe(const int writeFd, const int numMessages)
// {
//     using namespace std::chrono_literals;
//     std::stringstream message[numMessages];

//     for (int i=0; i<numMessages; i++)
//     {
//         std::this_thread::sleep_for(1s);
//         for (int j=0; j<i+1; j++)
//         {
//             message[i] << "Pika! ";
//         }
//         std::string stringMessage = message[i].str();
//         ThreadMessage messageWritten = {i, stringMessage};
//         write(writeFd, &messageWritten, sizeof(messageWritten));
//         std::cout << "[Writer] Message " << i+1 << " Sented \n";  
//     }
// }

// void ReadFromPipe(const int readerFd, const int numMessages)
// {
//     std::stringstream messages[numMessages];

//     for (int i=0; i < numMessages ; i++)
//     {
//         ThreadMessage messageReceived;
//         read(readerFd, &messageReceived, sizeof(messageReceived));
//         std::cout << "[Reader] Message " << i+1 << " was " << messageReceived.message <<"\n";  

//     }

// }

// int main()
// {
//     Timer timer;

//     int pipeFds[2];
//     const int numMessages = 2;

//     if (pipe(pipeFds) == -1) {
//         std::cerr << "Pipe creation failed!\n";
//         return 1;
//     }

//     PipedThread writerThread = {"Writer", pipeFds[1], numMessages, WriteToPipe}; // 1 is writer
//     PipedThread readerThread = {"Reader", pipeFds[0], numMessages, ReadFromPipe};  // 0 is reader

//     writerThread.Join();
//     readerThread.Join();
// }