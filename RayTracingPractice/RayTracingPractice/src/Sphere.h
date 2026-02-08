#pragma once

#include "RayTracingPCH.h"
#ifndef SPHERE_H
#define SPHERE_H

#include "Hittable.h"
#include "Vec3.h"

class Sphere : public Hittable
{
public:
    Sphere(
        const Point3& mCenter,
        double radius,
        Material* mat
    )
    : mCenter(mCenter)
    , mRadius(std::fmax(0, radius))
    , mMat(mat)
    {
    }
    bool Hit(const Ray& r, Interval rayT, HitRecord& rec) const override
    {
        Vec3 oc = mCenter - r.GetOrigin();
        double a = r.GetDirection().GetSquaredLength();
        double h = Dot(r.GetDirection(), oc);
        double c = oc.GetSquaredLength() - mRadius * mRadius;

        double discriminant = h * h - a * c;
        if (discriminant < 0)
        {
            return false;
        }
        
        double sqrtDiscriment = std::sqrt(discriminant);
        // Find the nearest root that lies in the acceptable range
        double root = (h - sqrtDiscriment) / a;
        if (!rayT.Surrounds(root))
        {
            root = (h+sqrtDiscriment) / a;
            if (!rayT.Surrounds(root))
            {
                return false;
            }
        }

        rec.t = root;
        rec.p = r.At(rec.t);
        rec.mat = mMat;


        Vec3 outwardNormal = (rec.p - mCenter) / mRadius;
        rec.SetFaceNormal(r, outwardNormal);

        return true;
    }

private:
    Point3 mCenter;
    double mRadius;
    Material* mMat;
};

#endif