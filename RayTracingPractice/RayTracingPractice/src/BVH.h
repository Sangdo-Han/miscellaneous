#pragma once
#ifndef BVH_H
#define BVH_H

#include <algorithm>
#include <vector>

#include "AABB.h"
#include "Hittable.h"
#include "HittableList.h"

// -----------------------------------------------------------
// 1. Define BVHNode FIRST
//    (std::vector<BVHNode> in the Tree class needs the full definition)
// -----------------------------------------------------------
class BVHNode : public Hittable
{
public:
	// Constructor: Just stores pointers, doesn't manage memory
	BVHNode(Hittable* left, Hittable* right, const AABB& bbox)
		: mLeft(left)
		, mRight(right)
		, mBbox(bbox)
	{
	}

	bool Hit(const Ray& r, Interval rayT, HitRecord& rec) const override
	{
		if (!mBbox.Hit(r, rayT))
		{
			return false;
		}

		bool hitLeft = mLeft->Hit(r, rayT, rec);
		bool hitRight = mRight->Hit(r, Interval(rayT.min, hitLeft ? rec.t : rayT.max), rec);

		return hitLeft || hitRight;
	}

	AABB BoundingBox() const override
	{
		return mBbox;
	}

private:
	Hittable* mLeft;
	Hittable* mRight;
	AABB mBbox;
};

class BVHTree : public Hittable
{
public:
	BVHTree(HittableList& list)
	{
		if (list.objects.empty()) return;

		size_t maxNodes = 2 * list.objects.size();
		mNodeArena.reserve(maxNodes);

		mRoot = buildRecursive(list.objects, 0, list.objects.size());
	}

	bool Hit(const Ray& r, Interval rayT, HitRecord& rec) const override
	{
		if (!mRoot)
		{
			return false;
		}
		return mRoot->Hit(r, rayT, rec);
	}

	AABB BoundingBox() const override
	{
		return mRoot ? mRoot->BoundingBox() : AABB();
	}

	inline BVHNode* AllocateNode(Hittable* left, Hittable* right, const AABB& bbox)
	{
		mNodeArena.emplace_back(left, right, bbox);
		return &mNodeArena.back();
	}

private:
	static bool sbBoxCompare(const Hittable* a, const Hittable* b, int axisIndex)
	{
		const Interval aAxisInterval = a->BoundingBox().AxisInterval(axisIndex);
		const Interval bAxisInterval = b->BoundingBox().AxisInterval(axisIndex);
		return aAxisInterval.min < bAxisInterval.min;
	}
	static bool sbBoxXCompare(const Hittable* a, const Hittable* b) { return sbBoxCompare(a, b, 0); }
	static bool sbBoxYCompare(const Hittable* a, const Hittable* b) { return sbBoxCompare(a, b, 1); }
	static bool sbBoxZCompare(const Hittable* a, const Hittable* b) { return sbBoxCompare(a, b, 2); }

	Hittable* buildRecursive(std::vector<Hittable*>& objects, size_t start, size_t end)
	{
		AABB box = AABB::empty;
		for (size_t objectIndex = start; objectIndex < end; objectIndex++)
		{
			box = AABB(box, objects[objectIndex]->BoundingBox());
		}
		int axis = box.LongestAxis();

		auto comparator = (axis == 0) ? sbBoxXCompare
			: (axis == 1) ? sbBoxYCompare
			: sbBoxZCompare;

		size_t objectSpan = end - start;

		Hittable* leftChild;
		Hittable* rightChild;

		if (objectSpan == 1) {
			return objects[start]; // Returns Sphere* (valid conversion to Hittable*)
		}
		else if (objectSpan == 2) {
			if (comparator(objects[start], objects[start + 1])) {
				leftChild = objects[start];
				rightChild = objects[start + 1];
			}
			else {
				leftChild = objects[start + 1];
				rightChild = objects[start];
			}
		}
		else {
			std::sort(objects.begin() + start, objects.begin() + end, comparator);
			size_t mid = start + objectSpan / 2;

			leftChild = buildRecursive(objects, start, mid);
			rightChild = buildRecursive(objects, mid, end);
		}

		//AABB box = AABB(leftChild->BoundingBox(), rightChild->BoundingBox());

		return AllocateNode(leftChild, rightChild, box);
	}

private:
	std::vector<BVHNode> mNodeArena;
	Hittable* mRoot = nullptr;
};

#endif