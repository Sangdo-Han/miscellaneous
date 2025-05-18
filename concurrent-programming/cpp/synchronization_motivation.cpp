// #include <array>
// #include <chrono>
// #include <iostream>
// #include <thread>

// #include "Timer.h"

// void IncreaseA(const int numIter, int* shared_ptr)
// {
//     int i = 0;
//     using namespace std::chrono_literals;
//     for (int i = 0; i < numIter; ++i) {
//         ++(*shared_ptr);
//         std::this_thread::sleep_for(10us);
//     }
// }

// int main()
// {
    
//     Timer timer;
//     constexpr int NUM_THREADS = 4;
//     constexpr int NUM_ITERATIONS = 10'000;

//     int shared_value = 0;
    
//     std::array<std::thread, NUM_THREADS> threads;
    
//     for(int i=0; i<NUM_THREADS; ++i)
//     {
//         threads[i] = std::thread(IncreaseA, NUM_ITERATIONS, &shared_value);
//     }

//     for(int i=0; i<NUM_THREADS; ++i)
//     {
//         threads[i].join();
//     }
    
//     std::cout << shared_value << "\n";

// }