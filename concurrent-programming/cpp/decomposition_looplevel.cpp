// #include<array>
// #include<chrono>
// #include<iostream>
// #include<thread>

// void WasteCpu(int idx, int item, std::array<int, 10>& outArr)
// {
//     using namespace std::chrono_literals;
//     outArr[idx] = item * item;
//     std::this_thread::sleep_for(2s);
// }

// int main()
// {
//     std::array<int, 10> inArr;
//     std::array<int, 10> outArr;
//     std::array<std::thread, 10> threads;

//     for (size_t i=0; i<10; ++i)
//     {
//         inArr[i] = i;
//     }

//     for (int i=0; i<10; ++i)
//     {
//         threads[i] = std::thread(WasteCpu, i, inArr[i], std::ref(outArr));
//     }

//     for (auto& t: threads)
//     {
//         t.join();
//     }

//     for (int& item : outArr)
//     {
//         std::cout << item << " ";
//     }
//     std::cout << std::endl;
// }
