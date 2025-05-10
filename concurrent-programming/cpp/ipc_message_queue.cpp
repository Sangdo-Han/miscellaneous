// #include <chrono>
// #include <iostream>
// #include <mutex>
// #include <thread>
// #include <string>
// #include <queue>
// #include <deque>
// #include <array>
// #include <sstream>
// #include <atomic>
// #include "Timer.h"

// struct QueueThreadSafe
// {
//     QueueThreadSafe(std::string id)
//     : m_ID(id), m_Done(false) {}

//     std::string m_ID;
//     std::deque<std::string> m_Data;
//     std::mutex m_Mutex;
//     std::condition_variable m_CV;
//     std::atomic<bool> m_Done;
// };

// void ConsumeTime(QueueThreadSafe& queue)
// {
//     using namespace std::chrono_literals;
//     std::this_thread::sleep_for(1s);
//     std::cout << "Thread ["<< std::this_thread::get_id() << "] finalizes the job. (spends some time) \n"; 
// }

// void SwapQueue(QueueThreadSafe& srcQueue, QueueThreadSafe& destQueue) {
//     // Timer timer;
//     std::thread::id threadID = std::this_thread::get_id();
    
//     while (true) {
//         std::string data;
//         {
//             std::unique_lock<std::mutex> src_lk(srcQueue.m_Mutex);
//             srcQueue.m_CV.wait(
//                 src_lk, [&srcQueue] { return !srcQueue.m_Data.empty() || srcQueue.m_Done; }
//             );

//             if (srcQueue.m_Data.empty() && srcQueue.m_Done) {
//                 break;
//             }

//             data = srcQueue.m_Data.front();
//             srcQueue.m_Data.pop_front();
//         }

//         std::stringstream tempStr;
//         tempStr << "[" << threadID << "] :" << data;
//         std::string processedData = tempStr.str();

//         {
//             std::lock_guard<std::mutex> dest_lk(destQueue.m_Mutex);
//             destQueue.m_Data.push_back(processedData);
//         }
//         destQueue.m_CV.notify_one();
//     }
//     ConsumeTime(destQueue);
// }

// int main()
// {
//     Timer timer;
//     const int numThreads = 2;
//     const int numDummyStrings = 100;

//     QueueThreadSafe srcQueue("srcQueue");
//     QueueThreadSafe destQueue("destQueue");

//     for (int idx = 0; idx < numDummyStrings; idx++)
//     {
//         std::stringstream tempStr;
//         tempStr << "Data - " << idx;
//         srcQueue.m_Data.push_back(tempStr.str());
//     }

//     std::array<std::thread, numThreads> threads;

//     // Start worker threads
//     for (std::thread& thread : threads)
//     {
//         thread = std::thread(SwapQueue, std::ref(srcQueue), std::ref(destQueue));
//     }

//     {
//         std::lock_guard<std::mutex> lock(srcQueue.m_Mutex);
//         srcQueue.m_Done = true; // Mark queue as done
//     }
//     srcQueue.m_CV.notify_all(); // Wake up all threads

//     // Wait for all threads to finish
//     for (auto& thread : threads)
//     {
//         thread.join();
//     }

//     // Print results
//     for (auto& datum : destQueue.m_Data)
//     {
//         std::cout << datum << "\n";
//     }

//     return 0;
// }
