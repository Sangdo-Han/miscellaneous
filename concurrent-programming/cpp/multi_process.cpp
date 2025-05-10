// #include <iostream>
// #include <chrono>

// // UNIX dependency - POSIX . Not working in Windows
// #include <unistd.h>

// #include <sys/types.h>
// #include <sys/wait.h>
// #include <thread>
// #include "Timer.h"

// void SleepFor(int sleepSeconds)
// {
//     auto sleepLiteral = std::chrono::seconds(sleepSeconds);
//     std::this_thread::sleep_for(sleepLiteral);
// }

// void RunChild(int sleepSeconds) {
//     Timer timer;
//     pid_t currPID = getpid();
//     SleepFor(sleepSeconds);
//     std::cout << "Child process PID: " << currPID << std::endl;
// }

// void RunParent(int numChildren = 3, int sleepSeconds = 2) {
//     pid_t currPID = getpid();
//     std::cout << "Parent process PID: " << currPID << std::endl;

//     for (int i = 0; i < numChildren; ++i) {
//         pid_t PID = fork();
        
//         if (PID < 0) {
//             std::cerr << "Fork failed" << std::endl;
//         } else if (PID == 0) {
//             RunChild(sleepSeconds);
//             _exit(0); // Terminate child process
//         }
//     }
    
//     // Parent waits for all children to finish
//     for (int i = 0; i < numChildren; ++i) {
//         waitpid(-1, nullptr, 0);
//     }
// }

// int main() {
//     Timer timer;
//     const int numChildren = 3;
//     const int sleepSeconds = 2;
//     RunParent(numChildren, sleepSeconds);
//     return 0;
// }
