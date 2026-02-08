#pragma once

#include "RayTracingPCH.h"
#ifndef HITTABLE_LIST_H
#define HITTABLE_LIST_H

#include <vector>

#include "Hittable.h"

class HittableList: public Hittable
{
public:
    HittableList() {
        objects.reserve(100);
    }
    HittableList(const HittableList&) = delete;
    HittableList& operator=(const HittableList&) = delete;
    ~HittableList(){
        Clear();
    }
    HittableList(Hittable* object)
    {
        Add(object);
    }
    void Clear()
    {
        objects.clear();
    }
    void Add(Hittable* object)
    {
        objects.push_back(object);
    }
    bool Hit(const Ray& r, Interval rayT, HitRecord& rec) const override
    {
        HitRecord tempRec;
        bool bHitAnything = false;
        double closestSoFar = rayT.max;

        for (const Hittable* object: objects)
        {
            if (object->Hit(r, Interval(rayT.min, closestSoFar), tempRec))
            {
                bHitAnything = true;
                closestSoFar = tempRec.t;
                rec = tempRec;
            }
        }
        return bHitAnything;

    }
public:
    std::vector<Hittable*> objects;
};

#endif