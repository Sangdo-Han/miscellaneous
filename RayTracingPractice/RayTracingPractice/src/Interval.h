#pragma once
#include "RayTracingPCH.h"
#ifndef INTERVAL_H
#define INTERVAL_H


class Interval
{
public:
    Interval()
    : min(+infinity)
    , max(+infinity)
    {
    }
    Interval(double min, double max)
    : min(min)
    , max(max)
    {
    }
    Interval(const Interval& a, const Interval& b)
    {
        min = a.min < b.min ? a.min : b.min;
        max = a.max > b.max ? a.max : b.max;
    }
    double Size() const
    {
        return max - min;
    }
    bool Contains(double x) const
    {
        return min <= x && x <= max;
    }
    bool Surrounds(double x) const
    {
        return min < x && x < max;
    }
    double Clamp(double x) const
    {
        if (x < min)
            return min;
        if (x >= max)
            return max;
        return x;
    }
    Interval expand(double delta) const
    {
        auto padding = delta / 2;
        return Interval(min - padding, max + padding);
    }
    static const Interval empty;
    static const Interval universe;

public:
    double min;
    double max;
};

inline const Interval Interval::empty = Interval(+infinity, -infinity);
inline const Interval Interval::universe = Interval(-infinity, +infinity);
#endif