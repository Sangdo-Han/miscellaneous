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

    static const Interval empty;
    static const Interval universe;

public:
    double min;
    double max;
};

#endif