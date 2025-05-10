#include <algorithm>
#include <iostream>
#include <mutex>
#include <thread>
#include <vector>
#include <unordered_map>
#include <condition_variable>
#include <queue>
#include <random>

using Summary = std::unordered_map<int, int>;

class ThreadPool {
public:
    ThreadPool(size_t numThreads) : m_Stop(false) {
        for (size_t i = 0; i < numThreads; ++i) {
            m_Workers.emplace_back([this] {
                while (true) {
                    std::function<void()> task;
                    {
                        std::unique_lock<std::mutex> lk(m_QueueMutex);
                        m_CV.wait(lk, [this] { return m_Stop || !m_Tasks.empty(); });
                        if (m_Stop && m_Tasks.empty()) {
                            return;
                        }
                        task = std::move(m_Tasks.front());
                        m_Tasks.pop();
                    }
                    task();
                }
            });
        }
    }

    ~ThreadPool() {
        {
            std::unique_lock<std::mutex> lk(m_QueueMutex);
            m_Stop = true;
        }
        m_CV.notify_all();
        for (std::thread& worker : m_Workers) {
            worker.join();
        }
    }

    template <class Func, class... Args>
    void Enqueue(Func&& f, Args&&... args) {
        {
            std::unique_lock<std::mutex> lk(m_QueueMutex);
            if (m_Stop) {
                throw std::runtime_error("Enqueue stopped");
            }
            m_Tasks.emplace(std::bind(std::forward<Func>(f), std::forward<Args>(args)...));
        }
        m_CV.notify_one();
    }

private:
    std::vector<std::thread> m_Workers;
    std::queue<std::function<void()>> m_Tasks;
    std::mutex m_QueueMutex;
    std::condition_variable m_CV;
    bool m_Stop;
};

Summary ProcessPile(const std::vector<int>& pile) {
    Summary summary;
    for (int vote : pile) {
        summary[vote]++;
    }
    return summary;
}

Summary VoteUp(const std::vector<int>& pile, int numWorkers = 4) {
    int voteCount = pile.size();
    int unitWorkload = voteCount / numWorkers;
    std::vector<std::vector<int>> votePiles(numWorkers);
    for (int i = 0; i < numWorkers; ++i) {
        int start = i * unitWorkload;
        int end = (i == numWorkers - 1) ? voteCount : (i + 1) * unitWorkload;
        votePiles[i] = std::vector<int>(pile.begin() + start, pile.begin() + end);
    }

    ThreadPool pool(numWorkers);
    std::vector<Summary> workerSummaries(numWorkers);
    std::mutex summaryMutex;
    std::vector<std::pair<Summary, int>> results;

    std::mutex tasksMutex;
    std::condition_variable tasksCV;
    int tasksCompleted = 0;

    for (int i = 0; i < numWorkers; ++i) {
        pool.Enqueue([&, i]() {
            Summary localSummary = ProcessPile(votePiles[i]);
            {
                std::lock_guard<std::mutex> lk(summaryMutex);
                results.emplace_back(localSummary, i);
            }
            {
                std::lock_guard<std::mutex> lk(tasksMutex);
                tasksCompleted++;
            }
            tasksCV.notify_one();
        });
    }

    {
        std::unique_lock<std::mutex> lk(tasksMutex);
        tasksCV.wait(lk, [&] { return tasksCompleted == numWorkers; });
    }

    std::sort(results.begin(), results.end(), [](const auto& a, const auto& b) { return a.second < b.second; });

    for (int i = 0; i < numWorkers; ++i) {
        workerSummaries[i] = results[i].first;
        std::cout << "Votes from worker " << i << ": {";
        for (auto const& [key, val] : workerSummaries[i]) {
            std::cout << key << " : " << val << ", ";
        }
        std::cout << "}\n";
    }

    Summary totSummary;
    for (const auto& workerSummary : workerSummaries) {
        for (const auto& [key, val] : workerSummary) {
            totSummary[key] += val;
        }
    }
    std::cout << "Total number of votes: {";
    for (auto const& [key, val] : totSummary) {
        std::cout << key << ":" << val << ", ";
    }
    std::cout << "}" << std::endl;
    return totSummary;
}

int main() {
    int numCandidates = 3;
    int numVoters = 1000000;
    std::vector<int> pile(numVoters);

    std::random_device randDevice;
    std::mt19937 gen(randDevice());
    std::uniform_int_distribution<> uniformDist(1, numCandidates);

    std::generate(pile.begin(), pile.end(), [&]() { return uniformDist(gen); });

    Summary counts = VoteUp(pile);

    return 0;
}