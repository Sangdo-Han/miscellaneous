#pragma once

#ifndef CAMERA_H
#define CAMERA_H
#include <iostream>
#include "Vec3.h"

class Camera
{
public:

private:
	double mAspectRatio;
	double focalLength;
	double viewportHeight;
	double viewportWidth;
	double pos;
};

#endif