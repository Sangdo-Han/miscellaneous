// #include <iostream>
// #include <thread>
// #include <vector>
// #include <queue>
// #include <functional>
// #include <mutex>
// #include <condition_variable>
// #include <chrono>
// #include <atomic>

// std::mutex coutMtx;

// using Task = std::function<void()>;

// class ThreadPool {
// public:
//     ThreadPool(size_t numThreads) : mb_Stop(false) {
//         for (size_t i = 0; i < numThreads; ++i) {
//             m_Workers.emplace_back([this] { workerThread(); });
//         }
//     }

//     ~ThreadPool() {
//         {
//             std::unique_lock<std::mutex> lock(m_queueMtx);
//             mb_Stop = true;
//         }
//         m_CV.notify_all();
//         for (auto& worker : m_Workers) {
//             worker.join();
//         }
//     }

//     template <typename Func, typename... Args>
//     void Submit(Func&& func, Args&&... args) {
//         {
//             std::unique_lock<std::mutex> lk(m_queueMtx);
//             m_Tasks.emplace(std::bind(std::forward<Func>(func), std::forward<Args>(args)...));
//         }
//         m_CV.notify_one();
//     }

//     void Wait() {
//         std::unique_lock<std::mutex> lk(m_WaitMtx);
//         m_CVWait.wait(lk, [this] { return m_Tasks.empty(); });
//     }

// private:
//     void workerThread() {
//         while (true) {
//             Task task;
//             {
//                 std::unique_lock<std::mutex> lock(m_queueMtx);
//                 m_CV.wait(lock, [this] { return mb_Stop || !m_Tasks.empty(); });
//                 if (mb_Stop && m_Tasks.empty()) {
//                     return;
//                 }
//                 task = std::move(m_Tasks.front());
//                 m_Tasks.pop();

//                 if(m_Tasks.empty()){
//                     m_CVWait.notify_one();
//                 }
//             }

//             task();
//         }
//     }

//     std::vector<std::thread> m_Workers;
//     std::queue<Task> m_Tasks;
//     std::mutex m_queueMtx;
//     std::condition_variable m_CV;
//     std::mutex m_WaitMtx;
//     std::condition_variable m_CVWait;
//     std::atomic<bool> mb_Stop;
// };

// void cpu_waster(int idx) {
//     std::this_thread::sleep_for(std::chrono::seconds(3));
//     {   
//         std::lock_guard<std::mutex> lk(coutMtx);
//         std::cout << std::this_thread::get_id() << " : doing " << idx << " work" << std::endl;
//     }
// }

// int main() {
//     int numJobs = 20;
//     int numThreads = 5;

//     ThreadPool pool(numThreads);

//     for (int idx = 0; idx < numJobs; ++idx) {
//         pool.Submit(cpu_waster, idx);
//     }
//     pool.Wait();

//     return 0;
// }