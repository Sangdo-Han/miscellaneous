#pragma once

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

using Point3 = Vec3;

#endif