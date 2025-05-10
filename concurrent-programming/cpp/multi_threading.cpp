// #include <chrono>
// #include <iostream>
// #include <mutex>
// #include <string>
// #include <sstream>
// #include <thread>

// #include <unistd.h>
// #include <sys/types.h>

// #include "Timer.h"
// #include "ThreadSafeUtils.h"

// void ExecuteThread(int idx, int sleepSeconds, ThreadSafePrinter& printer)
// {
//     pid_t threadPID = getpid();
//     std::thread::id threadID = std::this_thread::get_id();

//     std::ostringstream ss;
//     ss << "Thread - "<< idx << " ("<< threadID << ") in PID (" << threadPID << ")" << "\n";

//     printer.Print(ss.str());

//     std::this_thread::sleep_for(std::chrono::seconds(sleepSeconds));
// }

// int main()
// {
//     Timer timer;
//     ThreadSafePrinter safePrinter;

//     const int NUM_THREAD = 5;
//     const int SLEEP_SECONDS = 2;

//     std::thread threads[NUM_THREAD];

//     for (int i=0; i < NUM_THREAD; i++)
//     {
//         threads[i] = std::thread(ExecuteThread, i, SLEEP_SECONDS, std::ref(safePrinter));
//     }

//     for ( int i=0; i < NUM_THREAD; i++)
//     {
//         threads[i].join();
//     }

// }
