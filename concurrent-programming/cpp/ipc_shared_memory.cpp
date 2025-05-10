// #include <iostream>
// #include <thread>
// #include <string>
// #include <chrono>
// #include <mutex>

// static const int s_NumData =5;
// static int s_SharedArr[s_NumData];
// std::mutex mutex;


// void ProduceJob(unsigned int producingSeconds)
// {
    
//     std::cout << std::this_thread::get_id() << "\n";
//     auto producingTime = std::chrono::seconds(producingSeconds);
//     std::this_thread::sleep_for(producingTime);
//     for (int idx=0; idx<s_NumData; idx++)
//     {
//         std::lock_guard<std::mutex> lk(mutex);
//         std::cout << "Writing [" << idx << "] data \n";
//         s_SharedArr[idx] = idx;
//     }
// }

// void ConsumeJob(unsigned int penaltySeconds) {
//     for (int idx = 0; idx < s_NumData; idx++) {
//         while (true) {
//             {
//                 std::lock_guard<std::mutex> lk(mutex);
//                 if (s_SharedArr[idx] != -1) {
//                     std::cout << "Consumer read [" << idx << "] data: " << s_SharedArr[idx] << "\n";
//                     break;
//                 }
//             }
//             std::cout << "Consumer: No data at index " << idx << ", waiting " << penaltySeconds << " sec\n";
//             std::this_thread::sleep_for(std::chrono::seconds(penaltySeconds));
//         }
//     }
// }


// int main()
// {
//     for (int idx=0; idx<s_NumData; idx++)
//     {
//         s_SharedArr[idx] = -1;
//     }
//     const int numThread = 2;
//     std::thread threads[numThread];
//     threads[0] = std::thread(ProduceJob,1);  
//     threads[1] = std::thread(ConsumeJob,2);

//     for (int idx=0; idx < numThread; idx++)
//     {
//         threads[idx].join();
//     }
// }
