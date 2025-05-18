#include <atomic>
#include <iostream>
#include <thread>

#include "Timer.h"
// 아래 CompareAndSwap 과 TestAndSet은 실제 구현체는 아토믹 연산을 수행하나,
// C / C++ 에선 OS / Hardware 함수가 아니면 실제 아토믹이 아니라 아래 처럼 사용해야 한다.
#include <iostream>
#include <thread>
#include <atomic>

class Mutex {
public:
    void Lock() {
        while (m_IsLocked.exchange(true)) {} // 원자적 교체
    }
    void Unlock() {
        m_IsLocked.store(false);
    }
private:
    std::atomic<bool> m_IsLocked = false;
};
// // CAS
// // *p 와 val 이 다르면 false 를 반환해 버리고, 같으면 *p에 새 값을 쓰고 true 반환.
// template<typename T>
// bool CompareAndSwap(T *p, T val, T newVal)
// {
//     if (*p!=val)
//     {
//         return false;
//     }
//     *p = newVal;
//     return true;
// }

// TAS
// 입력된 포인터의 값이 true 면 true, 아닐 경우 pointer 의 값은 true 로 설정하지만 false를 발환.
std::atomic<bool> TestAndSet(std::atomic<bool> *p)
{
    if (*p)
    {
        return true;
    }
    else
    {
        *p = true;
        return false;
    }

}

class Mutex
{    
public:
    void Lock() {
        while (TestAndSet(&m_IsLocked)) {
            // TAS 에 의해, false 로 시작 되었다면, false 를 반환하면서 while을 빠져나가게 되고,
            // 즉시 멤버 변수 (m_IsLocked)는 true : 잠긴 상태가 된다.

        }
        // Lock을 수행한 곳에서 Unlock 하지 않는다면, 
        // 다른 곳에 Lock을 접근하려는 경우, 포인터에 의해 m_IsLocked 는 true 인 상태를 유지하기 때문에, 접근 무한 대기가 된다.
    }
    void Unlock() {
        // 단, 이 코드는 다른 곳에서 Unlock 을 먼저 선언해 버리는 순간 조진다. 항상 Lock() -> Unlock() 순서를 유지한다.
        m_IsLocked = false;
    }

private:
    std::atomic<bool> m_IsLocked = false; // false: unlocked, true: locked
    // 풀려있는 상태 : 즉, false 로 시작한다.
};

void IncreaseA(const int numIter, int* shared_ptr, Mutex& mtx)
{
    int i = 0;
    using namespace std::chrono_literals;
    for (int i = 0; i < numIter; ++i)
    {
        mtx.Lock();
        ++(*shared_ptr);
        mtx.Unlock();
        std::this_thread::sleep_for(10us); // 자원 획득 이외의 임의 대기는 굳이 lock 구간에서 수행 할 필요 없다.
    }
}

int main()
{
    
    Timer timer;
    Mutex mtx;
    
    constexpr int NUM_THREADS = 4;
    constexpr int NUM_ITERATIONS = 10'000;

    int shared_value = 0;
    
    std::array<std::thread, NUM_THREADS> threads;

    for(int i=0; i<NUM_THREADS; ++i)
    {
        threads[i] = std::thread(IncreaseA, NUM_ITERATIONS, &shared_value, std::ref(mtx));
    }

    for(int i=0; i<NUM_THREADS; ++i)
    {
        threads[i].join();
    }
    std::cout << shared_value << "\n";
}