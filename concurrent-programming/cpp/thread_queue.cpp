// #include <iostream>
// #include <chrono>
// #include <thread>
// #include <queue>
// #include <array>

// #include "Timer.h"
// #include "ThreadSafeUtils.h"

// void SwapOnce(tsafe::DeQueue<int>* srcQueue, tsafe::DeQueue<int>* destQueue)
// {
//     tsafe::Printer safePrint;

//     using namespace std::chrono_literals;
//     std::this_thread::sleep_for(1s);

//     int srcTemp = srcQueue->PopFront();
//     int destTemp = destQueue->PopFront();
//     destQueue->PushBack(srcTemp);
//     srcQueue->PushBack(destTemp);

//     safePrint.Print("Swapped!\n");
// }

// int main()
// {
//     Timer timer;

//     std::array<std::thread, 50> threads;

//     tsafe::DeQueue<int> srcQueue("src-queue");
//     tsafe::DeQueue<int> destQueue("dest-queue");

//     for (int i=0; i<50; i++)
//     {
//         srcQueue.PushBack(1);
//         destQueue.PushBack(2);
//     }
//     srcQueue.SetDone();
//     destQueue.SetDone();

//     for (std::thread& t : threads)
//     {
//         t = std::thread(SwapOnce, &srcQueue, &destQueue);
//     }

//     for (std::thread& t : threads)
//     {
//         t.join();
//     }

//     for (int i=0; i<50; i++)
//     {
//         std::cout << srcQueue.PopFront() << " ";
//     }
//     std::cout << "\n";

// }

// // int main() 
// // {
// //     tsafe::DeQueue<int> srcQueue("src-queue");
// //     tsafe::DeQueue<int> destQueue("dest-queue");
// //     tsafe::Printer printer;

// //     for (int i = 0; i < 50; ++i) {
// //         srcQueue.PushBack(i);
// //     }
// //     srcQueue.SetDone();

// //     std::array<std::thread, 5> threads;

// //     for (auto& t : threads) {
// //         t = std::thread(
// //             &tsafe::DeQueue<int>::SendOneElement,
// //             &srcQueue,
// //             &destQueue
// //         );
// //     }

// //     for (auto& t : threads) {
// //         t.join(); // Join the threads
// //     }


// //     for (int i = 0; i < 50; ++i) {
// //         auto x = destQueue.PopFront();
// //         std::cout << x << " ";
// //     }
    
// //     return 0;
// // }