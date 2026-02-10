#pragma once

#include<chrono>
#include<iostream>

using namespace std::chrono_literals;
class Timer
{
public:
	Timer(const std::string& codeBlockName)
		: mCodeBlockName(codeBlockName)
		, mStart(std::chrono::high_resolution_clock::now())
	{
		std::clog << "Start " << mCodeBlockName << "... \n";
	}
	~Timer()
	{
		std::chrono::duration<float> elapseSec
			= std::chrono::high_resolution_clock::now() - mStart;

		std::clog << "Executed in " << std::chrono::duration_cast<std::chrono::seconds>(elapseSec).count() << " (sec)";
	}
private:
	std::string mCodeBlockName;
	std::chrono::high_resolution_clock::time_point mStart;
};