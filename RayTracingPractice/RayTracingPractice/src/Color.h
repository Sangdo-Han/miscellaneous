#pragma once

#include "RayTracingPCH.h"
#ifndef COLOR_H
#define COLOR_H

#include "Vec3.h"
#include "Interval.h"
using Color = Vec3;

inline double LinearToGamma(double linearComponent)
{
	if (linearComponent > 0)
		return std::sqrt(linearComponent);
	return 0;
}

inline void WriteColor(std::ostream& out, const Color& pixelColor)
{
	double r = pixelColor.X();
	double g = pixelColor.Y();
	double b = pixelColor.Z();


	r = LinearToGamma(r);
	g = LinearToGamma(g);
	b = LinearToGamma(b);

	// Translate [0, 1] component values to the byte range (0, 255)
	
	static const Interval intensity(0.000, 0.999);

	int rByte = int(255.999 * intensity.Clamp(r));
	int gByte = int(255.999 * intensity.Clamp(g));
	int bByte = int(255.999 * intensity.Clamp(b));

	out << rByte << ' ' << gByte << ' ' << bByte << '\n';
}

#endif