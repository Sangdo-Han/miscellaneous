#pragma once

#include "RayTracingPCH.h"
#ifndef RAY_H
#define RAY_H


class Ray
{
public:
	Ray()
	{
	}
	Ray(const Point3& origin, const Vec3& direction)
		: mOrigin(origin)
		, mDirection(direction)
	{
	}
	const Point3& GetOrigin() const { return mOrigin; }
	const Vec3& GetDirection() const { return mDirection; }
	Point3 At(double t) const {
		return mOrigin + t * mDirection;
	}
private:
	Point3 mOrigin;
	Vec3 mDirection;
};

#endif
