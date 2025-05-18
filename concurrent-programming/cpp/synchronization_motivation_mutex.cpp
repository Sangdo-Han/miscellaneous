// #include <array>
// #include <chrono>
// #include <iostream>
// #include <thread>
// #include <mutex>

// #include "Timer.h"


// void IncreaseA(const int numIter, int* shared_ptr, std::mutex& mtx)
// {
//     int i = 0;
//     using namespace std::chrono_literals;
//     for (int i = 0; i < numIter; ++i)
//     {
//         // Basic Use, but not recommanded
//         // mtx.lock();
//         // ++(*shared_ptr);
//         // mtx.unlock();
//         // std::this_thread::sleep_for(10us); // 자원 획득 이외의 임의 대기는 굳이 lock 구간에서 수행 할 필요 없다.

//         { // mtx는 참조로 전달되었고, lock_guard는 RAII Wrapper 방식으로 code block 이탈 시 lock/unlock 처리
//             std::lock_guard<std::mutex> lk(mtx);
//             ++(*shared_ptr);
//         } // unlock 발생
//         std::this_thread::sleep_for(10us);

//         std::unique_lock<std::mutex> lk(mtx, std::defer_lock);

//         // lk.lock();
//         // int temp = *shared_ptr;
//         // ++temp;
//         // *shared_ptr = temp;
//         // lk.unlock();
//         // std::this_thread::sleep_for(10us);

//     }
// }

// int main()
// {
    
//     Timer timer;
//     std::mutex mtx;
    
//     constexpr int NUM_THREADS = 4;
//     constexpr int NUM_ITERATIONS = 10'000;

//     int shared_value = 0;
    
//     std::array<std::thread, NUM_THREADS> threads;

//     for(int i=0; i<NUM_THREADS; ++i)
//     {
//         threads[i] = std::thread(IncreaseA, NUM_ITERATIONS, &shared_value, std::ref(mtx));
//     }

//     for(int i=0; i<NUM_THREADS; ++i)
//     {
//         threads[i].join();
//     }
//     std::cout << shared_value << "\n";
// }