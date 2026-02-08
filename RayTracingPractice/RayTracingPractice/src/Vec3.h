#pragma once

#include "RayTracingPCH.h"
#ifndef VEC3_H
#define VEC3_H
#include <cmath>
#include <iostream>


class Vec3
{
public:
	Vec3()
	: mElement{0,0,0}
	{
	}
	Vec3(double e0, double e1, double e2)
	: mElement{e0, e1, e2}
	{
	}
	Vec3(const Vec3& other) // Copy Constructor
	: mElement{other.mElement[0], other.mElement[1], other.mElement[2]}
	{
	}
	double X() const
	{
		return mElement[0];
	}
	double Y() const
	{
		return mElement[1];
	}
	double Z() const
	{
		return mElement[2];
	}

	Vec3 operator-() const { return Vec3(-mElement[0], -mElement[1], -mElement[2]); }
	double operator[](int i) const { return mElement[i]; }
	double& operator[](int i) { return mElement[i]; }
	Vec3& operator-=(const Vec3& v)
	{
		mElement[0] -= v.mElement[0];
		mElement[1] -= v.mElement[1];
		mElement[2] -= v.mElement[2];

		return *this;
	}
	Vec3& operator+=(const Vec3& v)
	{
		mElement[0] += v.mElement[0];
		mElement[1] += v.mElement[1];
		mElement[2] += v.mElement[2];
		
		return *this;
	}
	Vec3& operator*=(const double t)
	{
		mElement[0] *= t;
		mElement[1] *= t;
		mElement[2] *= t;
		return *this;
	}
	Vec3& operator/=(const double t)
	{
		return *this *= 1 / t;
	}
	double GetSquaredLength() const
	{
		return mElement[0] * mElement[0] 
			+ mElement[1] * mElement[1] 
			+ mElement[2] * mElement[2];
	}
	double Getlength() const {
		return std::sqrt(GetSquaredLength());
	}
	bool IsNearZero() const
	{
		double s = 1e-8;
		return (std::fabs(mElement[0]) < s)
			&& (std::fabs(mElement[1]) < s)
			&& (std::fabs(mElement[2]) < s);
	}
	static Vec3 Random()
	{
		return Vec3(RandomDouble(), RandomDouble(), RandomDouble());
	}
	static Vec3 Random(double min, double max)
	{
		return Vec3(RandomDouble(min, max), RandomDouble(min, max), RandomDouble(min, max));
	}

private:
	double mElement[3];
};


// Vector Utility Functions

inline std::ostream& operator<<(std::ostream& out, const Vec3& v)
{
	return out << v[0] << ' ' << v[1] << ' ' << v[2];
}

inline Vec3 operator+(const Vec3& u, const Vec3& v)
{
	return Vec3(u[0] + v[0], u[1] + v[1], u[2] + v[2]);
}
inline Vec3 operator-(const Vec3& u, const Vec3& v)
{
	return Vec3(u[0] - v[0], u[1] - v[1], u[2] - v[2]);
}
inline Vec3 operator*(const Vec3& u, const Vec3& v)
{
	// element-wise production between vectors.
	return Vec3(u[0] * v[0], u[1] * v[1], u[2] * v[2]);
}
inline Vec3 operator*(const Vec3& u, double t)
{
	return Vec3(u[0] * t, u[1] * t, u[2] * t);
}
inline Vec3 operator*(double t, const Vec3& u)
{
	return u * t;
}
inline Vec3 operator/(const Vec3& u, double t)
{
	return (1 / t) * u;
}
inline double Dot(const Vec3& u, const Vec3& v)
{
	return u[0] * v[0]
		+ u[1] * v[1]
		+ u[2] * v[2];
}
inline Vec3 Cross(const Vec3& u, const Vec3& v)
{
	return Vec3(
		u[1] * v[2] - u[2] * v[1],
		u[2] * v[0] - u[0] * v[2],
		u[0] * v[1] - u[1] * v[0]
	);
}
inline Vec3 UnitVector(const Vec3 u)
{
	return u / u.Getlength();
}
inline Vec3 RandomInUnitDisk()
{
	while (true)
	{
		Vec3 p = Vec3(RandomDouble(-1, 1), RandomDouble(-1, 1), 0);
		if (p.GetSquaredLength() < 1)
		{
			return p;
		}
	}
}
inline Vec3 RandomUnitVector()
{
	while (true)
	{
		Vec3 p = Vec3::Random(-1, 1);
		double lensq = p.GetSquaredLength();
		if (1e-160 < lensq && lensq <= 1)
		{
			return p / sqrt(lensq);
		}
	}
}
inline Vec3 RandomOnHemisphere(const Vec3& normal)
{
	Vec3 onUnitSphere = RandomUnitVector();
	if (Dot(onUnitSphere, normal) > 0.0) // In the same hemisphere as the normal
		return onUnitSphere;
	else
		return -onUnitSphere;
}
inline Vec3 Reflect(const Vec3& v, const Vec3& n)
{
	return v - 2 * Dot(v, n) * n;
}
inline Vec3 Refract(const Vec3& uv, const Vec3& n, double etaiOverEtat)
{
	double cosTheta = std::fmin(Dot(-uv, n), 1.0);
	Vec3 rOutPrep = etaiOverEtat * (uv + cosTheta * n);
	Vec3 rOutParallel = -std::sqrt(std::fabs(1.0 - rOutPrep.GetSquaredLength())) * n;
	return rOutPrep + rOutParallel;
}

using Point3 = Vec3;

#endif