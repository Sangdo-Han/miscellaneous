// #include <iostream>
// #include <queue>
// #include <mutex>
// #include <condition_variable>
// #include <thread>
// #include <memory>
// #include <chrono>
// #include <string>

// template<typename T>
// class ThreadSafeQueue
// {
// public:
//     void Push(T item)
//     {
//         std::lock_guard<std::mutex> lock(m_Mutex);
//         m_Queue.push(std::move(item));
//         m_CV.notify_one();
//     }
    
//     bool Pop(T& item, std::chrono::milliseconds timeout)
//     {
//         std::unique_lock<std::mutex> lock(m_Mutex);
//         if (m_CV.wait_for(lock, timeout, [this] { return !m_Queue.empty(); }))
//         {
//             item = std::move(m_Queue.front());
//             m_Queue.pop();
//             return true;
//         }
//         return false;
//     }

// private:
//     std::queue<T> m_Queue;
//     mutable std::mutex m_Mutex;
//     std::condition_variable m_CV;
// };

// class SharedCounter
// {
// public:
//     SharedCounter(int initialValue = 0)
//     : m_Value(initialValue)
//     {}
//     void Increment()
//     {
//         std::lock_guard<std::mutex> lock(m_Mutex);
//         ++m_Value;
//     }
//     void Decrement()
//     {
//         std::lock_guard<std::mutex> lock(m_Mutex);
//         --m_Value;
//     }
//     int Get()
//     {
//         std::lock_guard<std::mutex> lock(m_Mutex);
//         return m_Value;
//     }
// private:
//     int m_Value;
//     std::mutex m_Mutex;

// };

// class Worker
// {
// public:
//     Worker(
//         ThreadSafeQueue<std::string>& queueIn,
//         ThreadSafeQueue<std::string>* queueOut,
//         std::string jobType,
//         std::chrono::milliseconds turnaroundTime,
//         int numProjects,
//         std::shared_ptr<SharedCounter> processCounter = nullptr
//     )
//     : m_QueueIn(queueIn)
//     , m_QueueOut(queueOut)
//     , m_JobType(std::move(jobType))
//     , m_TurnaroundTime(turnaroundTime)
//     , m_NumProjects(numProjects)
//     , m_ProcessCounter(processCounter ? processCounter : std::make_shared<SharedCounter>())
//     {}

//     void Start()
//     {
//         m_Thread = std::thread(&Worker::run, this);
//     }

//     void Join()
//     {
//         if (m_Thread.joinable())
//         {
//             m_Thread.join();
//         }
//     }

//     ~Worker()
//     {
//         Join();
//     }

// private:
//     void run()
//     {
//         while (m_ProcessCounter->Get() < m_NumProjects)
//         {
//             std::string workload;
//             bool isPopped = m_QueueIn.Pop(workload, std::chrono::seconds(1));
//             if (isPopped)
//             {
//                 std::cout << m_JobType << " .... " << workload << std::endl;
//                 std::this_thread::sleep_for(m_TurnaroundTime);
//                 m_ProcessCounter->Increment();
//                 if (m_QueueOut)
//                 {
//                     m_QueueOut->Push(workload);
//                 }
//             }
//         }
//     }
// private:
//     ThreadSafeQueue<std::string>& m_QueueIn;
//     ThreadSafeQueue<std::string>* m_QueueOut;
//     std::string m_JobType;
//     std::chrono::milliseconds m_TurnaroundTime;
//     int m_NumProjects;
//     std::shared_ptr<SharedCounter> m_ProcessCounter;
//     std::thread m_Thread;

// };

// class Pipeline
// {
// public:
//     Pipeline(int numProjects)
//     : m_NumProjects(numProjects)
//     {}

//     void RunConcurrently()
//     {
//         ThreadSafeQueue<std::string> toBePlanned;
//         for (int idx = 0; idx < m_NumProjects; ++idx)
//         {
//             toBePlanned.Push("Shoes #" + std::to_string(idx));
//         }

//         ThreadSafeQueue<std::string> toBeProgrammed;
//         ThreadSafeQueue<std::string> toBeFinalized;

//         Worker designer(toBePlanned, &toBeProgrammed, "Designer", std::chrono::milliseconds(200), m_NumProjects);

//         auto sharedCounter = std::make_shared<SharedCounter>();
//         Worker manufacturer1(toBeProgrammed, &toBeFinalized, "Manufacturer 1", std::chrono::milliseconds(400), m_NumProjects, sharedCounter);
//         Worker manufacturer2(toBeProgrammed, &toBeFinalized, "Manufacturer 2", std::chrono::milliseconds(500), m_NumProjects, sharedCounter);

//         Worker manager(toBeFinalized, nullptr, "Manager", std::chrono::milliseconds(100), m_NumProjects);

//         designer.Start();
//         manufacturer1.Start();
//         manufacturer2.Start();
//         manager.Start();

//         designer.Join();
//         manufacturer1.Join();
//         manufacturer2.Join();
//         manager.Join();
//     }
// private:
//     int m_NumProjects;
// };

// class Timer
// {    
// public:
//     Timer()
//     {
//         start = std::chrono::high_resolution_clock::now();
//     }

//     ~Timer()
//     {
//         auto end = std::chrono::high_resolution_clock::now();
//         auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
//         std::cout << "Time taken: " << duration.count() << " milliseconds" << std::endl;
//     }
// private:
//     std::chrono::time_point<std::chrono::high_resolution_clock> start;
// };

// int main() {
//     {
//         Timer timer;
//         Pipeline pipeline(100);
//         pipeline.RunConcurrently();
//     }
//     return 0;
// }