#pragma once
#ifndef HITTABLE_H
#define HITTABLE_H
#include "RayTracingPCH.h"
#include "AABB.h"

class Material;

class HitRecord
{
public:
    void SetFaceNormal(const Ray& r, const Vec3& outwardNormal)
    {
        // Sets the hit record normal vector
        // NOTE: the parameter `outward_normal` is assumed to have unit length.
        frontFace = Dot(r.GetDirection(), outwardNormal) < 0;
        normal = frontFace ? outwardNormal : - outwardNormal;
    }

public:
    Point3 p;
    Vec3 normal;
    Material* mat;
    double t;
    // u, v : Texture coordinate
    double u;
    double v;
    bool frontFace;
};

class Hittable
{
public:
    virtual ~Hittable() = default;
    virtual bool Hit(const Ray& r, Interval rayT, HitRecord& rec) const = 0;
    virtual AABB BoundingBox() const = 0;

};

#endif