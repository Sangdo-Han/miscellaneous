#include <iostream>
#include "Timer.h"

Timer::Timer()
    : m_Start(std::chrono::high_resolution_clock::now())
{

}
Timer::~Timer()
{
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duration = end - m_Start;
    std::cout << "Process Ended in " << duration.count() << " [s].\n";
}