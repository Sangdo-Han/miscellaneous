#pragma once
#ifndef TEXTURE_H
#define TEXTURE_H
#include "RayTracingPCH.h"
#include "ImageLoader.h"
class Texture
{
public:
	virtual ~Texture() = default;
	virtual Color Value(double u, double v, const Point3& p) const = 0;
};

class SolidColor : public Texture
{
public:
	SolidColor(const Color& albedo)
		: mAlbedo(albedo)
	{
	}
	SolidColor(double red, double green, double blue)
		:SolidColor(Color(red, green, blue))
	{
	}
	Color Value(double u, double v, const Point3& p) const override
	{
		return mAlbedo;
	}
private:
	Color mAlbedo;
};

class CheckerTexture : public Texture
{
public:
	CheckerTexture(double scale, Texture* even, Texture* odd)
		: mInvScale(1.0 / scale)
		, mEven(even)
		, mOdd(odd)
	, mOwnership(false)
	{
	}
	CheckerTexture(double scale, const Color& c1, const Color& c2)
		: CheckerTexture(scale, new SolidColor(c1), new SolidColor(c2))
	{
		mOwnership = true;
	}
	CheckerTexture(const CheckerTexture&) = delete;
	CheckerTexture operator=(const CheckerTexture&) = delete;
	virtual ~CheckerTexture()
	{
		if (mOwnership)
		{
			delete mEven;
			delete mOdd;
			mEven = nullptr;
			mOdd = nullptr;
		}
	}
	Color Value(double u, double v, const Point3& p) const override
	{
		int xInteger = int(std::floor(mInvScale * p.X()));
		int yInteger = int(std::floor(mInvScale * p.Y()));
		int zInteger = int(std::floor(mInvScale * p.Z()));

		bool isEven = (xInteger + yInteger + zInteger) % 2 == 0;
		return isEven ? mEven->Value(u, v, p) : mOdd->Value(u, v, p);
	}

private:
	double mInvScale;
	Texture* mEven = nullptr;
	Texture* mOdd = nullptr;
	bool mOwnership = false;
};

class ImageTexture : public Texture
{
public:
	ImageTexture(const char* filename)
		: mImage(filename)
	{
	}
	Color  Value(double u, double v, const Point3& p) const override 
	{
		if (mImage.GetHeight() <= 0) return Color(0, 1, 1);

		// Clamp input texture coordinates to [0,1] x [1,0]
		u = Interval(0, 1).Clamp(u);
		v = 1.0 - Interval(0, 1).Clamp(v);

		int i = int(u * mImage.GetWidth());
		int j = int(v * mImage.GetHeight());
		const unsigned char* pixel = mImage.GetPixelData(i, j);

		double colorScale = 1.0 / 255.0;
		return Color(colorScale * pixel[0], colorScale * pixel[1], colorScale * pixel[2]);

	}
private:
	ImageLoader mImage;
};

#endif // !TEXTURE_H
