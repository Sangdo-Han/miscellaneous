#pragma once
#ifndef INTERVAL_H
#define INTERVAL_H
#include "Constant.h"

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
    static const Interval empty;
    static const Interval universe;

public:
    double min;
    double max;
};

#endif