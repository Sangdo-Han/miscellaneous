#pragma once

#include "RayTracingPCH.h"
#ifndef CAMERA_H
#define CAMERA_H
#include "Hittable.h"
#include "Material.h"
#include "Texture.h"
#include "Sphere.h"

class Camera
{
public:
	Camera(
		int imageWidth,
		double aspectRatio,
		int samplesPerPixel = 10,
		int maxDepth = 10,
		double vfov = 90
	)
	: mImageWidth(imageWidth)
	, mAspectRatio(aspectRatio)
	, mSamplesPerPixel(samplesPerPixel)
	, mMaxDepth(maxDepth)
	, mVerticalFOV(vfov)
	{
	}
	void Render(const Hittable& world)
	{
		initialize();

		std::cout << "P3\n" << mImageWidth << ' ' << mImageHeight << "\n255\n";

		for (int j = 0; j < mImageHeight; j++)
		{
			std::clog << "\rScanlines remaining: " << (mImageHeight - j) << ' ' << std::flush;
			for (int i = 0; i < mImageWidth; i++)
			{
				Color pixelColor(0, 0, 0);
				for (int sample=0; sample < mSamplesPerPixel; sample++)
				{
					Ray r = getRay(i, j);
					pixelColor += rayColorRecursively(r, mMaxDepth, world);
				}
				WriteColor(std::cout, mPixelSamplesScale * pixelColor);

			}
		}
		std::clog << "\rDone.                \n";
	}
private:
	void initialize()
	{
		mImageHeight = int(mImageWidth / mAspectRatio);
		mImageHeight = (mImageHeight < 1) ? 1 : mImageHeight;
		mCenter = LookFrom;

		mPixelSamplesScale = 1.0 / mSamplesPerPixel;

		// Determine Viewport dimensions.
		double theta = DegreesToRadian(mVerticalFOV);
		double h = std::tan(theta / 2);
		mViewportHeight = 2 * h * focusDist;
		mViewportWidth = mViewportHeight * (double(mImageWidth) / mImageHeight);


		w = UnitVector(LookFrom - LookAt);
		u = UnitVector(Cross(VUp, w));
		v = Cross(w, u);

		// Calculate the vectors across the horizontal and down the vertical viewport edges.
		Vec3 viewportU = mViewportWidth * u;
		Vec3 viewportV = mViewportHeight * -v;

		// Calculate the horizontal and vertical delta vectors from pixel to pixel
		mPixelDeltaU = viewportU / mImageWidth;
		mPixelDeltaV = viewportV / mImageHeight;

		Vec3 viewportUpperLeft = mCenter
								- (focusDist * w)
								- viewportU / 2
								- viewportV / 2;

		mPixel00Loc = viewportUpperLeft + 0.5 * (mPixelDeltaU + mPixelDeltaV);

		double defocusRadius = focusDist * std::tan(DegreesToRadian(DefocusAngle / 2 ));
		defocusDiskU = u * defocusRadius;
		defocusDiskV = v * defocusRadius;

	}
	Ray getRay(int i, int j) const
	{
		// Construct a camera ray originating from the defocus disk and directed at a randomly
		// sampled point around the pixel location i, j

		Vec3 offset = sampleSquare();
		Vec3 pixelSample = mPixel00Loc
						+ ((i + offset.X()) * mPixelDeltaU)
						+ ((j + offset.Y()) * mPixelDeltaV);
		
		Point3 rayOrigin = (DefocusAngle <= 0) ? mCenter : defocusDiskSample();
		Point3 rayDirection = pixelSample - rayOrigin;

		double rayTime = RandomDouble();


		return Ray(rayOrigin, rayDirection, rayTime);
	}
	Point3 defocusDiskSample() const
	{
		auto p = RandomInUnitDisk();
		return mCenter + (p[0] * defocusDiskU) + (p[1] * defocusDiskV);
	}
	Vec3 sampleSquare() const
	{
		// Returns the vector to a random point in the [-.5,-.5]-[+.5,+.5] unit square.
		return Vec3(RandomDouble() - 0.5, RandomDouble() - 0.5, 0);
	}
	Color rayColorRecursively(const Ray& r, int depth, const Hittable& world) const
	{
		// exit criteria
		if (depth <= 0)
		{
			return Color(0, 0, 0);
		}

		HitRecord rec;
		if (world.Hit(r, Interval(0.001, infinity), rec))
		{
			Ray scattered;
			Color attenuation;
			if (rec.mat->Scatter(r, rec, attenuation, scattered))
				return attenuation * rayColorRecursively(scattered, depth - 1, world);
			return Color(0, 0, 0);
		}

		Vec3 unitDirection = UnitVector(r.GetDirection());
		if (mBackground != nullptr)
		{
			double u;
			double v;

			Sphere::GetSphereUV(unitDirection, u, v);
			return mBackground->Value(u, v, unitDirection);

			
		}
		double a = 0.5 * (unitDirection.Y() + 1.0);
		return (1.0 - a) * Color(1.0, 1.0, 1.0) + a * Color(0.8, 0.35, 0.9);
	}
public:
	Point3 LookFrom = Point3(0, 0, 0);
	Point3 LookAt = Point3(0, 0, -1);
	Vec3 VUp = Vec3(0, 1, 0);

	double DefocusAngle = 0; // Variation angle of rays through each pixel
	double focusDist = 10; // Distance from camera LookFrom point to plane of perfect focus

private:
	double mAspectRatio = 1.0;
	int mImageWidth = 100;
	int mImageHeight;
	
	// Render Quality
	int mSamplesPerPixel; // anti-aliasing
	int mMaxDepth; // diffusion

	// Camera
	double mFocalLength = 1.0;
	double mVerticalFOV = 90; // Vertical view angle (Field of View)
	double mViewportHeight;
	double mViewportWidth;

	double mPixelSamplesScale; // Color scale factor for a sum of pixel samples
	
	Point3 mCenter;
	Point3 mPixel00Loc;
	Vec3 mPixelDeltaU;
	Vec3 mPixelDeltaV;

	// Camera frame basis vectors
	Vec3 u;
	Vec3 v;
	Vec3 w;

	Vec3 defocusDiskU; // Defocus Disk horizontal radius
	Vec3 defocusDiskV; // Defocus Disk vertical radius

	ImageTexture* mBackground = new ImageTexture("purplesky.jpg");
};

#endif