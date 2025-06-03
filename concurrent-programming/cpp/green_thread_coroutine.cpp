// #define _XOPEN_SOURCE

// #include <ucontext.h>
// #include <iostream>
// #include <vector>
// #include <unistd.h>
// #include <sys/time.h>
// #include <cassert>
// #include <functional>

// constexpr int STACK_SIZE = 1024 * 64;
// constexpr int MAX_THREADS = 128;

// struct GreenThread {
//     ucontext_t ctx;
//     char stack[STACK_SIZE];
//     bool finished = false;
//     uint64_t wake_time = 0;
//     std::function<void()> entry;
// };

// std::vector<GreenThread> threads;
// int current_thread = -1;

// uint64_t now_ms() {
//     timeval tv;
//     gettimeofday(&tv, nullptr);
//     return tv.tv_sec * 1000ULL + tv.tv_usec / 1000ULL;
// }

// // Yield control to the next runnable thread
// void yield() {
//     int prev = current_thread;
//     int start = (current_thread == -1) ? 0 : current_thread;
//     for (int i = 1; i <= (int)threads.size(); ++i) {
//         int next = (start + i) % threads.size();
//         if (!threads[next].finished && now_ms() >= threads[next].wake_time) {
//             current_thread = next;
//             if (prev == -1) {
//                 // First time running, no context to save
//                 setcontext(&threads[next].ctx);
//                 // setcontext does not return
//                 assert(false);
//             } else {
//                 swapcontext(&threads[prev].ctx, &threads[next].ctx);
//             }
//             return;
//         }
//     }
//     // No runnable thread found, just return
// }

// // Sleep async by setting wake_time and yielding
// void async_sleep(int ms) {
//     threads[current_thread].wake_time = now_ms() + ms;
//     yield();
// }

// // Trampoline called by makecontext with thread index
// void thread_trampoline(int idx) {
//     current_thread = idx;
//     threads[idx].entry();
//     threads[idx].finished = true;
//     yield(); // back to scheduler or other threads
//     // Should never return here
//     assert(false);
// }

// // Create a green thread running fn
// void create_green_thread(std::function<void()> fn) {
//     assert(threads.size() < MAX_THREADS);

//     GreenThread gt;
//     getcontext(&gt.ctx);
//     gt.ctx.uc_stack.ss_sp = gt.stack;
//     gt.ctx.uc_stack.ss_size = sizeof(gt.stack);
//     gt.ctx.uc_link = nullptr; // no successor context
//     gt.entry = fn;

//     threads.push_back(std::move(gt));
//     int index = (int)threads.size() - 1;

//     // Pass index as argument to trampoline
//     makecontext(&threads[index].ctx, (void (*)())thread_trampoline, 1, index);
// }

// // Run the scheduler until all threads finish
// void run_scheduler() {
//     while (true) {
//         bool any_running = false;
//         for (const auto& t : threads) {
//             if (!t.finished) {
//                 any_running = true;
//                 break;
//             }
//         }
//         if (!any_running) break;

//         yield();
//         usleep(1000); // prevent 100% CPU spinning
//     }
// }

// // Example task 1
// void task1() {
//     std::cout << "[Task 1] Start\n";
//     async_sleep(1000);
//     std::cout << "[Task 1] After 1s\n";
//     async_sleep(1000);
//     std::cout << "[Task 1] Done\n";
// }

// // Example task 2
// void task2() {
//     std::cout << "[Task 2] Start\n";
//     async_sleep(500);
//     std::cout << "[Task 2] After 0.5s\n";
//     async_sleep(1500);
//     std::cout << "[Task 2] Done\n";
// }

// int main() {
//     create_green_thread(task1);
//     create_green_thread(task2);
//     run_scheduler();
//     return 0;
// }
