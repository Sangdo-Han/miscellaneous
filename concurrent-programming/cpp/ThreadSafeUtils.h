#pragma once
#include <atomic>
#include <condition_variable>
#include <deque>
#include <mutex>
#include <string>
#include <thread>

namespace tsafe
{

    class Printer
    {
    public:
        void Print(const std::string& str);
    private:
        std::mutex m_Mutex;
    };

    // RAII Pattern for safe thread join.
    class ThreadGuard
    {
    public:
        explicit ThreadGuard(std::thread& thread):
            m_Thread(thread)
        {   
        }
        ~ThreadGuard()
        {
            if(m_Thread.joinable())
            {
                m_Thread.join();;
            }
        }
        ThreadGuard(ThreadGuard const&) = delete;
        ThreadGuard& operator=(ThreadGuard const&) = delete;
    private:
        std::thread& m_Thread;
    };


    class ScopedThread
    {
    public:
        explicit ScopedThread(std::thread thread):
            m_Thread(std::move(thread))
        {
            if(!m_Thread.joinable())
            {
                throw std::logic_error("No Thread");
            }
        }
        ~ScopedThread()
        {
            m_Thread.join();
        }
        ScopedThread(ScopedThread const&)=delete;
        ScopedThread& operator=(ScopedThread const&)=delete;
    private:
        std::thread m_Thread;
    };

    template<typename T>
    class DeQueue {
    public:
        DeQueue(std::string id) : m_ID(id), m_Done(false) {}

        T PopFront() {
            std::unique_lock<std::mutex> lk(m_Mutex);
            m_CV.wait(lk, [this] { return !m_Data.empty() || m_Done.load(); });

            if (m_Data.empty() && m_Done.load()) {
                throw std::runtime_error("Queue is empty and done.");
            }

            T val = std::move(m_Data.front());
            m_Data.pop_front();
            return val;
        }

        T PopBack() {
            std::unique_lock<std::mutex> lk(m_Mutex);
            m_CV.wait(lk, [this] { return !m_Data.empty() || m_Done.load(); });

            if (m_Data.empty() && m_Done.load()) {
                throw std::runtime_error("Queue is empty and done.");
            }

            T val = std::move(m_Data.back());
            m_Data.pop_back();
            return val;
        }

        void PushFront(T val) {
            {
                std::lock_guard<std::mutex> lk(m_Mutex);
                m_Data.push_front(std::move(val));
            }
            m_CV.notify_one();
        }

        void PushBack(T val) {
            {
                std::lock_guard<std::mutex> lk(m_Mutex);
                m_Data.push_back(std::move(val));
            }
            m_CV.notify_one();
        }

        void SetDone() {
            {
                std::lock_guard<std::mutex> lk(m_Mutex);
                m_Done = true;
            }
            m_CV.notify_all();
        }


        void SendOneElement(DeQueue* other) {
            while (true) {  // Keep trying to move elements until the queue is empty and done
                T data;
                {
                    std::unique_lock<std::mutex> srcLock(this->m_Mutex);
                    this->m_CV.wait(
                        srcLock,
                        [this] { return !this->m_Data.empty() || this->m_Done.load(); }
                    );
        
                    if (this->m_Data.empty() && this->m_Done.load()) {
                        return;  // Exit thread when work is done
                    }
                    data = std::move(this->m_Data.front());
                    this->m_Data.pop_front();
                }
                other->PushBack(std::move(data));  // Transfer data to the destination queue
            }
        }
    

    private:
        std::string m_ID;
        std::deque<T> m_Data;
        std::mutex m_Mutex;
        std::condition_variable m_CV;
        std::atomic<bool> m_Done;
    };


};
