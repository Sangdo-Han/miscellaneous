#pragma once
#ifndef IMAGE_LOADER_H
#define IMAGE_LOADER_H


//#define STB_IMAGE_IMPLEMENTATION
#include "external/stb_image.h"

#include <cstdlib>
#include <iostream>


class ImageLoader
{
public:
	ImageLoader() {}
	ImageLoader(const char* imageFilename)
	{
		std::string filename = std::string(imageFilename);


		// char* imageDir = getenv("RTW_IMAGES");
		char* imageDir = nullptr;
		size_t len;
		errno_t err = _dupenv_s(&imageDir, &len, "RTW_IMAGES");

		if (imageDir && Load(std::string(imageDir) + "/" + imageFilename)) return;
		if (Load(filename)) return;
		if (Load("images/" + filename)) return;
		if (Load("../images/" + filename)) return;
		if (Load("../../images/" + filename)) return;
		if (Load("../../RayTracingPractice/images/" + filename)) return;
		if (Load("../../../images/" + filename)) return;
		if (Load("../../../../images/" + filename)) return;
		if (Load("../../../../../images/" + filename)) return;

		std::cerr << "Error could not load image file " << imageFilename << ".\n";
	}
	~ImageLoader()
	{
		delete[] mBData;
		free(mFData);
	}

	bool Load(const std::string& filename)
	{
		int n = mBytesPerPixel;

		mFData = stbi_loadf(filename.c_str(), &mImageWidth, &mImageHeight, &n, mBytesPerPixel);
		
		if (mFData == nullptr) return false;

		mBytesPerScanline = mImageWidth * mBytesPerPixel;
		convertToBytes();
		return true;
	}
	int GetWidth() const { return (mFData == nullptr) ? 0 : mImageWidth; }
	int GetHeight() const { return (mFData == nullptr) ? 0 : mImageHeight; }
	const unsigned char* GetPixelData(int x, int y) const
	{
		// Return the address of the three RGB bytes of the pixel at x, y, If there is no image
		// data, returns magenta.

		static unsigned char magenta[] = { 255, 0, 255 };
		if (mBData == nullptr) return magenta;
		x = clamp(x, 0, mImageWidth);
		y = clamp(y, 0, mImageHeight);
		return mBData + y * mBytesPerScanline + x * mBytesPerPixel;
	}

private:
	static int clamp(int x, int low, int high)
	{
		if (x < low) return low;
		if (x < high) return x;
		return high - 1;
	}
	static unsigned char floatToByte(float value)
	{
		if (value <= 0.0)
			return 0;
		if (1.0 <= value)
			return 255; 
		return static_cast<unsigned char>(256.0 * value);
	}
	void convertToBytes()
	{
		int totalBytes = mImageWidth * mImageHeight * mBytesPerPixel;
		mBData = new unsigned char[totalBytes];

		auto* bptr = mBData;
		auto* fptr = mFData;
		for (int i = 0; i < totalBytes; i++, fptr++, bptr++)
		{
			*bptr = floatToByte(*fptr);

		}
	}

private:
	const int mBytesPerPixel = 3;
	float* mFData = nullptr; // Linear floating point pixel data
	unsigned char* mBData = nullptr; // Linear 8-bit pixel data
	int mImageWidth = 0;
	int mImageHeight = 0;
	int mBytesPerScanline = 0;

};





// Restore MSVC compiler warnings
#ifdef _MSC_VER
	#pragma warning (pop)
#endif

#endif