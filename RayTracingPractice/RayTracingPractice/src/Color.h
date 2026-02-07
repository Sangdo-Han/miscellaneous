#pragma once
#ifndef COLOR_H
#define COLOR_H
#include <iostream>
#include "Vec3.h"

using Color = Vec3;

void WriteColor(std::ostream& out, const Color& pixelColor)
{
	double r = pixelColor.X();
	double g = pixelColor.Y();
	double b = pixelColor.Z();

	// Translate [0, 1] component values to the byte range (0, 255)
	
	int rByte = int(255.999 * r);
	int gByte = int(255.999 * g);
	int bByte = int(255.999 * b);

	out << rByte << ' ' << gByte << ' ' << bByte << '\n';
}

#endif