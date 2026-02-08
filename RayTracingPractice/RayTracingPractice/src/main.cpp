
#include "RayTracingPCH.h"

#include "Camera.h"
#include "Hittable.h"
#include "HittableList.h"
#include "Sphere.h"
#include "Material.h"

void Step1();
void Step2();
void Step3();
void Step45(); // Step 4 and 5 : Adding Sphere

// Step 6 - 11
void Sandbox();

void FinalRenderer();

int main()
{
    // Step1();
    // Step2();
    // Step3();
    // Step45();
    // Sandbox();
    FinalRenderer();
}


void Step1() {
    // DAY 1 - Hello World in Image
    // Only requires <iostream>
    // Image
    int mImageWidth = 256;
    int mImageHeight = 256;

    // Render
    std::cout << "P3\n" << mImageWidth << ' ' << mImageHeight << "\n255\n";

    for (int j = 0; j < mImageHeight; j++) {
        std::clog << "\rScanlines remaining: " << (mImageHeight - j) << ' ' << std::flush;
        for (int i = 0; i < mImageWidth; i++) {
            auto r = double(i) / (mImageWidth - 1);
            auto g = double(j) / (mImageHeight - 1);
            auto b = 0.0;

            int ir = int(255.999 * r);
            int ig = int(255.999 * g);
            int ib = int(255.999 * b);

            std::cout << ir << ' ' << ig << ' ' << ib << '\n';
        }
    }

    std::clog << "\rDone.        \n";
}

void Step2()
{
    // DAY 2 - Hello Again with the following headers.
    // Requires Vec3.h
    // Requires Color.h

    int mImageHeight = 256;
    int mImageWidth = 256;

    // Render HW

    std::cout << "P3\n" << mImageHeight << ' ' << mImageHeight << "\n255\n";

    for (int j = 0; j < mImageHeight; j++)
    {
        std::clog << "\rScanlines remaining: " << (mImageHeight - j) << ' ' << std::flush;
        for (int i = 0; i < mImageWidth; i++)
        {
            Color PixelColor = Color(double(i) / (mImageWidth - 1), double(j) / (mImageHeight - 1), 0);
            WriteColor(std::cout, PixelColor);
        }
    }
    std::clog << "\rDone.        \n";
}

void Step3()
{
    double aspect_ratio = 16.0 / 9.0;
    int mImageWidth = 400;

    int mImageHeight = int(mImageWidth / aspect_ratio);
    mImageHeight = (mImageHeight < 1) ? 1 : mImageHeight;

    double viewportHeight = 2.0;
    double viewportWidth = viewportHeight * ((double)mImageWidth / mImageHeight);

}


bool HitSphereStep45(const Point3& mCenter, double radius, const Ray& ray)
{
    Vec3 oc = mCenter - ray.GetOrigin();
    double a = Dot(ray.GetDirection(), ray.GetDirection());
    double b = -2.0 * Dot(ray.GetDirection(), oc);
    double c = Dot(oc, oc) - radius * radius;
    double discriminant = b * b - 4 * a * c;
    return (discriminant >= 0);
}

Color RayColorStep45(const Ray& r)
{
    if (HitSphereStep45(Point3(0,0, -1), 0.5, r))
        return Color(1, 0, 0);

    Vec3 unitDirection = UnitVector(r.GetDirection());
    double a = 0.5 * (unitDirection.Y() + 1.0);
    return (1.0 - a) * Color(1.0, 1.0, 1.0 ) + a * Color(0.5, 0.7, 1.0);

}

void Step45()
{

    
    double mAspectRatio = 16.0 / 9.0;
    int mImageWidth = 400;
    int mImageHeight = int(mImageWidth / mAspectRatio);

    mImageHeight = (mImageHeight < 1) ? 1 : mImageHeight;

    double focalLength = 1.0;
    double viewportHeight = 2.0;
    double viewportWidth = viewportHeight * ((double) mImageWidth / mImageHeight);
    Vec3 cameraCenter = Point3(0,0,0);

    // Calculate the vectors across the horizontal and down the vertical viewport edges

    Vec3 viewportU = Vec3(viewportWidth, 0, 0);
    Vec3 viewportV = Vec3(0, -viewportHeight, 0);


    // Calculate the horizontal and verticla delta vectors from pixel to pixel
    Vec3 mPixelDeltaU = viewportU / mImageWidth;
    Vec3 mPixelDeltaV = viewportV / mImageHeight;

    // Calculate the location of the upper left pixel 
    Vec3 viewportUpperLeft = cameraCenter - Vec3(0, 0, focalLength) - viewportU / 2 - viewportV / 2;
    Vec3 mPixel00Loc = viewportUpperLeft + 0.5 * (mPixelDeltaU + mPixelDeltaV);

    // Render

    std::cout << "P3\n" << mImageWidth << " " << mImageHeight << "\n255\n";

    for (int j = 0; j < mImageHeight; j++)
    {
        std::clog << "\rScanlines remaining: " << (mImageHeight - j) << ' ' << std::flush;
        for (int i = 0; i < mImageWidth; i++)
        {
            Vec3 pixelCenter = mPixel00Loc + (i * mPixelDeltaU) + (j * mPixelDeltaV);
            Vec3 rayDirection = pixelCenter - cameraCenter;
            Ray r(cameraCenter, rayDirection);

            Color pixelColor = RayColorStep45(r);

            WriteColor(std::cout, pixelColor);

        }

    }
    std::clog << "\rDone.              \n";

}


void Sandbox()
{

    // World
    HittableList world;

    // Material
    Lambertian materialGround = Lambertian(Color(0.8, 0.8, 0.0));
    Lambertian materialCenter = Lambertian(Color(0.1, 0.2, 0.5));
    Metal materialRight = Metal(Color(0.8, 0.8, 0.8), 0.5);
    Dielectric materialLeft = Dielectric(1.5);
    Dielectric materialBubble = Dielectric(1 / 1.5);


    // Stack allocations.
    Sphere ground = Sphere(Point3(0, -100.5, -1), 100, &materialGround);
    Sphere ballCenter = Sphere(Point3(0.0, 0.0, -1.2), 0.5, &materialCenter);
    Sphere ballRight = Sphere(Point3(1.0, 0.0, -1.0), 0.5, &materialRight);
    Sphere ballLeft = Sphere(Point3(-1.0, 0.0, -1.0), 0.5, &materialLeft);
    Sphere ballBubble = Sphere(Point3(-1.0, 0.0, -1.0), 0.45, &materialBubble);

    world.Add(&ground);
    world.Add(&ballCenter);
    world.Add(&ballRight);
    world.Add(&ballLeft);
    world.Add(&ballBubble);


    Camera cam(
        400,
        16.0/9.0,
        100,
        50,
        20
    );

    cam.LookFrom = Point3(-2, 2, 1);
    cam.LookAt = Point3(0, 0, -1);
    cam.VUp = Vec3(0, 1, 0);

    cam.defocusAngle = 10.0;
    cam.focusDist = 3.4;

    cam.Render(world);

}

void FinalRenderer()
{
    // World
    HittableList world;
    std::vector<Sphere> sphereStorage;
    sphereStorage.reserve(500);


    Lambertian groundMaterial = Lambertian(Color(0.5, 0.5, 0.5));
    Sphere ground = Sphere(Point3(0, -1000, 0), 1000, &groundMaterial);
    world.Add(&ground);

    for (int a = -11; a < 11; a++)
    {
        for (int b=-11; b< 11; b++)
        {
            double chooseMat = RandomDouble();
            Point3 center(
                a + 0.9 * RandomDouble(),
                0.2,
                b + 0.9 * RandomDouble()
            );

            if ((center - Point3(4, 0.2, 0)).Getlength() > 0.9)
            {
                if (chooseMat < 0.8)
                {
                    Color albedo = Color::Random() * Color::Random();
                    Lambertian* sphereMaterial = new Lambertian(albedo);
                    Sphere sphere = Sphere(center, 0.2, sphereMaterial);
                    sphereStorage.push_back(sphere);
                    world.Add(&sphereStorage.back());
                }
                else if (chooseMat < 0.95)
                {
                    //Metal
                    Color albedo = Color::Random(0.5, 1);
                    auto fuzz = RandomDouble(0, 0.5);
                    Metal* sphereMaterial = new Metal(albedo, fuzz);
                    Sphere sphere = Sphere(center, 0.2, sphereMaterial);
                    sphereStorage.push_back(sphere);
                    world.Add(&sphereStorage.back());
                }
                else
                {
                    Dielectric* sphereMaterial = new Dielectric(1.5);
                    Sphere sphere = Sphere(center, 0.2, sphereMaterial);
                    sphereStorage.push_back(sphere);
                    world.Add(&sphereStorage.back());
                }
            }

        }   

    }

    Dielectric material1 = Dielectric(1.5);
    Sphere sphere1 = Sphere(Point3(0, 1, 0), 1.0, &material1);
    world.Add(&sphere1);

    Lambertian material2 = Lambertian(Color(0.4, 0.2, 0.1));
    Sphere sphere2 = Sphere(Point3(-4, 1, 0), 1.0, &material2);
    world.Add(&sphere2);

    Metal material3 = Metal(Color(0.7, 0.6, 0.5), 0.0);
    Sphere sphere3 = Sphere(Point3(4, 1, 0), 1.0, &material3);
    world.Add(&sphere3);

    Camera cam(1200, 16.0 / 9.0, 400, 40, 20);
    cam.LookFrom = Point3(13, 2, 3);
    cam.LookAt = Point3(0, 0, 0);
    cam.VUp = Vec3(0, 1, 0);

    cam.defocusAngle = 0.6;
    cam.focusDist = 10.0;

    cam.Render(world);
}
