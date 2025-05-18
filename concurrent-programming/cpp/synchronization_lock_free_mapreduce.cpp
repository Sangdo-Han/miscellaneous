// #include <array>
// #include <chrono>
// #include <iostream>
// #include <thread>
// #include <numeric> // for accumulation

// #include "Timer.h"

// void IncreaseA(const int numIter, int idx, int* sharedArray)
// {
//     using namespace std::chrono_literals;
//     for (int i = 0; i < numIter; ++i) {
//         ++(*(sharedArray + idx)); // only conducted in the designed buffers, no race-condition occurs.
//         std::this_thread::sleep_for(10us);
//     }
// }

// int main()
// {
//     constexpr int NUM_THREADS = 4;
//     constexpr int NUM_ITERATIONS = 10'000;

//     std::array<int, NUM_THREADS> lkFreeArray;
//     for (int idx=0; idx<NUM_THREADS; ++idx)
//     {
//         lkFreeArray[idx] = 0;
//     }

//     std::array<std::thread, NUM_THREADS> threads;
//     {
//         Timer timer;
//         for(int i = 0; i < NUM_THREADS; ++i)
//         {
//             // Pass the address of the array's first element
//             threads[i] = std::thread(IncreaseA, NUM_ITERATIONS, i, &lkFreeArray[0]);
//         }

//         for(int i = 0; i < NUM_THREADS; ++i)
//         {
//             threads[i].join();
//         }
//     }

//     std::cout << std::accumulate(lkFreeArray.begin(), lkFreeArray.end(), 0) << "\n";
// }