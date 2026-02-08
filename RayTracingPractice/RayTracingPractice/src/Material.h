#pragma once
#include "RayTracingPCH.h"
#ifndef MATERIAL_H
#define MATERIAL_H
#include "Hittable.h"

class Material
{
public:
	virtual ~Material() = default;
	virtual bool Scatter(
		const Ray& rIn,
		const HitRecord& rec,
		Color& attenuation,
		Ray& scattered
	) const
	{
		return false;
	}
};

class Lambertian : public Material
{
public:
	Lambertian(const Color& albedo)
		:mAlbedo(albedo)
	{
	}
	bool Scatter(
		const Ray& rIn,
		const HitRecord& rec,
		Color& attenuation,
		Ray& scattered
	) const override
	{
		Vec3 scatterDirection = rec.normal + RandomUnitVector();
	

		// Catch degenerate scatter direction
		if (scatterDirection.IsNearZero())
			scatterDirection = rec.normal;

		scattered = Ray(rec.p, scatterDirection);
		attenuation = mAlbedo;
		return true;
	}

private:
	Color mAlbedo;
};

class Metal : public Material
{
public:
	Metal(const Color& albedo, double fuzz = 0.0)
	: mAlbedo(albedo)
	, mFuzz(fuzz < 1 ? fuzz : 1)
	{}
	bool Scatter(
		const Ray& rIn,
		const HitRecord& rec,
		Color& attenuation,
		Ray& scattered
	) const override
	{
		Vec3 reflected = Reflect(rIn.GetDirection(), rec.normal);
		
		reflected = UnitVector(reflected) + (mFuzz * RandomUnitVector());
		scattered = Ray(rec.p, reflected);
		attenuation = mAlbedo;
		return true;
	}
private:
	Color mAlbedo;
	double mFuzz;
};

class Dielectric : public Material
{
public:
	Dielectric(double refractionIndex)
		: mRefractionIndex(refractionIndex)
	{
	}
	bool Scatter(
		const Ray& rIn,
		const HitRecord& rec,
		Color& attenuation,
		Ray& scattered
	) const override
	{
		attenuation = Color(1.0, 1.0, 1.0);
		double ri = rec.frontFace ? (1.0 / mRefractionIndex) : mRefractionIndex;

		Vec3 unitDirection = UnitVector(rIn.GetDirection());
		double cosTheta = std::fmin(Dot(-unitDirection, rec.normal), 1.0);
		double sinTheta = std::sqrt(1.0 - cosTheta * cosTheta);

		bool cannotRefract = ri * sinTheta > 1.0;
		Vec3 direction;

		if (cannotRefract || sCalcReflectance(cosTheta, ri) > RandomDouble())
			direction = Reflect(unitDirection, rec.normal);
		else
			direction = Refract(unitDirection, rec.normal, ri);

		scattered = Ray(rec.p, direction);
		return true;
	}
private:
	static double sCalcReflectance(double cos, double refractIndex)
	{
		double r0 = (1 - refractIndex) / (1 + refractIndex);
		r0 = r0 * r0;
		return r0 + (1 - r0) * std::pow((1 - cos), 5);
	}

private:
	// Refraction index in vacuum or air, or the ratio of the material's refractive index over
	// the refractive inde3x of the enclosing media
	double mRefractionIndex;
};
#endif