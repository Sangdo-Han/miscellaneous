#pragma once

#include "RayTracingPCH.h"
#ifndef SPHERE_H
#define SPHERE_H

#include "Hittable.h"
#include "Vec3.h"

class Sphere : public Hittable
{
public:
    // Stationary Sphere
    Sphere(const Point3& staticCenter, double radius, Material* mat)
        : mCenter(staticCenter, Vec3(0,0,0))
        , mRadius(std::fmax(0, radius))
        , mMat(mat)
    {
        Vec3 rayVec = Vec3(radius, radius, radius);
        mBbox = AABB(staticCenter - rayVec, staticCenter + rayVec);
    }
    // Moving Sphere
    Sphere(const Point3& center1, const Point3& center2, double radius, Material* mat)
        : mCenter(center1, center2 - center1)
        , mRadius(radius)
        , mMat(mat)
    {
        Vec3 rayVec = Vec3(radius, radius, radius);

        // AABB는 출발점(At(0))과 도착점(At(1))을 모두 감싸도록 생성
        AABB box1(mCenter.At(0) - rayVec, mCenter.At(0) + rayVec);
        AABB box2(mCenter.At(1) - rayVec, mCenter.At(1) + rayVec);
        mBbox = AABB(box1, box2);
    }

    bool Hit(const Ray& r, Interval rayT, HitRecord& rec) const override
    {
        Point3 currentCenter = mCenter.At(r.GetTime());
        Vec3 oc = currentCenter - r.GetOrigin();

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
        
        Vec3 outwardNormal = (rec.p - currentCenter) / mRadius;
        rec.SetFaceNormal(r, outwardNormal);
        getSphereUV(outwardNormal, rec.u, rec.v);
        rec.mat = mMat;

        return true;
    }
    AABB BoundingBox() const override { return mBbox; }

private:
    static void getSphereUV(const Point3& p, double& u, double& v)
    {
        // p: a given point on the sphere of radius one, centered at the origin.
        // u: returned value [0,1] of angle around the Y axis from X=-1.
        // v: returned value [0,1] of angle from Y=-1 to Y=+1.
        //     <1 0 0> yields <0.50 0.50>       <-1  0  0> yields <0.00 0.50>
        //     <0 1 0> yields <0.50 1.00>       < 0 -1  0> yields <0.50 0.00>
        //     <0 0 1> yields <0.25 0.50>       < 0  0 -1> yields <0.75 0.50>

        double theta = std::acos(-p.Y());
        double phi = std::atan2(-p.Z(), p.X()) + pi;
        u = phi / (2 * pi);
        v = theta / pi;
    }
private:
    Ray mCenter;
    double mRadius;
    Material* mMat;
    AABB mBbox;
};

#endif