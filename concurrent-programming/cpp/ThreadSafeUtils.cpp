#include <iostream>
#include "ThreadSafeUtils.h"

namespace tsafe
{
    void Printer::Print(const std::string& str)
    {
        std::lock_guard<std::mutex> lock(m_Mutex);
        std::cout << str ;
    }
}