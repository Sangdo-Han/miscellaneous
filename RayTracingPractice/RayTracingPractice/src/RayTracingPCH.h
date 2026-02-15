// In the RayTracing In a Weekend, It is rtweekend.h
#pragma once

#ifndef RAYTRACING_PCH_H
#define RAYTRACING_PCH_H
#include <cmath>
#include <random>
#include <iostream>
#include <limits>
#include <memory>

#include "Constant.h"

inline double DegreesToRadian(double degrees)
{
    return degrees * pi / 180.0;
}
inline double RandomDouble() // Use C++ Style Random Generator
{
    static std::uniform_real_distribution<double> distribution(0.0, 1.0);
    static std::mt19937 generator;
    return distribution(generator);
}
inline double RandomDouble(double min, double max)
{
    return min + (max - min) * RandomDouble();
}
inline double RandomInt(int min, int max)
{
    return int(RandomDouble(min, max + 1));
}
#include "Color.h"
#include "Ray.h"
#include "Vec3.h"
#include "Interval.h"

#endif