// #include <iostream>
// #include <mutex>
// #include <thread>
// #include <random>
// #include <vector>
// #include <unordered_map>

// #include "Timer.h"

// struct Task
// {
//     int ID;
//     int Input;
//     void (*Callback) (int, int);
// };

// std::unordered_map<int, std::vector<int>> results;
// std::mutex resultMutex;
// std::mutex printMutex;

// void ProcessTask(const Task& task)
// {
//     std::this_thread::sleep_for(std::chrono::milliseconds(100));
//     int result = task.Input * 2;
//     task.Callback(task.ID, result);
// }

// void CategorizeBy4(int taskID, int result)
// {
//     int category = result % 4;
//     {
//         std::lock_guard<std::mutex> lk(resultMutex);
//         results[category].push_back(result);
//     }
//     {
//         std::lock_guard<std::mutex> lk2(printMutex);
//         std::cout << "Task " << taskID
//           << " completed with result : " << result << "\n";
//     }
// }

// int main()
// {
//     Timer timer;
//     std::vector<Task> tasks;
//     std::random_device rd;
//     std::mt19937 gen(rd());
//     std::uniform_int_distribution<int> distrib(1, 100);

//     for (int i=0; i<20; ++i)
//     {
//         tasks.push_back({i, distrib(gen), CategorizeBy4});
//     }

//     std::vector<std::thread> threads;
//     for (const auto& task : tasks)
//     {
//         threads.emplace_back(ProcessTask, task);
//     }

//     for (auto& thread: threads)
//     {
//         if (thread.joinable())
//         {
//             thread.join();
//         }
//     }

//     for (const auto& [category, values]: results)
//     {
//         std::cout << "Category " << category << ": ";
//         for (int value: values)
//         {
//             std::cout << value << " ";
//         }
//         std::cout << std::endl;
//     }
// }