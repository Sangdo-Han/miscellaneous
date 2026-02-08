#include "RayTracingPCH.h"
#include "Hittable.h"
#include "HittableList.h"
#include "Sphere.h"

void Step1();
void Step2();
void Step3();
void Step45(); // Step 4 and 5 in the RayTracing In One Weekend
void Step6();

int main()
{
    // Step1();
    // Step2();
    // Step3();
    // Step45();
    Step6();
}


void Step1() {
    // DAY 1 - Hello World in Image
    // Only requires <iostream>
    // Image
    int imageWidth = 256;
    int imageHeight = 256;

    // Render
    std::cout << "P3\n" << imageWidth << ' ' << imageHeight << "\n255\n";

    for (int j = 0; j < imageHeight; j++) {
        std::clog << "\rScanlines remaining: " << (imageHeight - j) << ' ' << std::flush;
        for (int i = 0; i < imageWidth; i++) {
            auto r = double(i) / (imageWidth - 1);
            auto g = double(j) / (imageHeight - 1);
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

    int imageHeight = 256;
    int imageWidth = 256;

    // Render HW

    std::cout << "P3\n" << imageHeight << ' ' << imageHeight << "\n255\n";

    for (int j = 0; j < imageHeight; j++)
    {
        std::clog << "\rScanlines remaining: " << (imageHeight - j) << ' ' << std::flush;
        for (int i = 0; i < imageWidth; i++)
        {
            Color PixelColor = Color(double(i) / (imageWidth - 1), double(j) / (imageHeight - 1), 0);
            WriteColor(std::cout, PixelColor);
        }
    }
    std::clog << "\rDone.        \n";
}

void Step3()
{
    double aspect_ratio = 16.0 / 9.0;
    int imageWidth = 400;

    int imageHeight = int(imageWidth / aspect_ratio);
    imageHeight = (imageHeight < 1) ? 1 : imageHeight;

    double viewportHeight = 2.0;
    double viewportWidth = viewportHeight * ((double)imageWidth / imageHeight);

}


bool HitSphereStep45(const Point3& center, double radius, const Ray& ray)
{
    Vec3 oc = center - ray.GetOrigin();
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

    
    double aspectRatio = 16.0 / 9.0;
    int imageWidth = 400;
    int imageHeight = int(imageWidth / aspectRatio);

    imageHeight = (imageHeight < 1) ? 1 : imageHeight;

    double focalLength = 1.0;
    double viewportHeight = 2.0;
    double viewportWidth = viewportHeight * ((double) imageWidth / imageHeight);
    Vec3 cameraCenter = Point3(0,0,0);

    // Calculate the vectors across the horizontal and down the vertical viewport edges

    Vec3 viewportU = Vec3(viewportWidth, 0, 0);
    Vec3 viewportV = Vec3(0, -viewportHeight, 0);


    // Calculate the horizontal and verticla delta vectors from pixel to pixel
    Vec3 pixelDeltaU = viewportU / imageWidth;
    Vec3 pixelDeltaV = viewportV / imageHeight;

    // Calculate the location of the upper left pixel 
    Vec3 viewportUpperLeft = cameraCenter - Vec3(0, 0, focalLength) - viewportU / 2 - viewportV / 2;
    Vec3 pixel00Loc = viewportUpperLeft + 0.5 * (pixelDeltaU + pixelDeltaV);

    // Render

    std::cout << "P3\n" << imageWidth << " " << imageHeight << "\n255\n";

    for (int j = 0; j < imageHeight; j++)
    {
        std::clog << "\rScanlines remaining: " << (imageHeight - j) << ' ' << std::flush;
        for (int i = 0; i < imageWidth; i++)
        {
            Vec3 pixelCenter = pixel00Loc + (i * pixelDeltaU) + (j * pixelDeltaV);
            Vec3 rayDirection = pixelCenter - cameraCenter;
            Ray r(cameraCenter, rayDirection);

            Color pixelColor = RayColorStep45(r);

            WriteColor(std::cout, pixelColor);

        }

    }
    std::clog << "\rDone.              \n";

}


double HitSphereStep6(const Point3& center, double radius, const Ray& ray)
{
    Vec3 oc = center - ray.GetOrigin();
    double a = ray.GetDirection().GetSquaredLength();
    double h = Dot(ray.GetDirection(), oc);
    double c = oc.GetSquaredLength() - radius * radius;
    double discriminant = h * h - a * c;

    if (discriminant < 0)
    {
        return -1.0;
    }
    else
    {
        return (h - std::sqrt(discriminant)) / a;
    }
}

Color RayColorStep6(const Ray& r, const Hittable& world)
{
    HitRecord rec;
    if (world.Hit(r, Interval(0, infinity), rec))
    {
        return 0.5 * (rec.normal + Color(1, 1, 1));
    }

    Vec3 unitDirection = UnitVector(r.GetDirection());
    double a = 0.5 * (unitDirection.Y() + 1.0);
    return (1.0 - a) * Color(1.0, 1.0, 1.0) + a * Color(0.5, 0.7, 1.0);

}

void Step6()
{

    // Image
    double aspectRatio = 16.0 / 9.0;
    int imageWidth = 400;

    // Calculate the image height, and ensure that it's at least 1.
    int imageHeight = int(imageWidth / aspectRatio);
    imageHeight = (imageHeight < 1) ? 1 : imageHeight;

    // World
    HittableList world;

    // I will use stack allocation.
    Sphere ball1 = Sphere(Point3(0,0, -1), 0.5);
    Sphere ball2 = Sphere(Point3(0, -100.5, -1), 100);

    world.Add(&ball1);
    world.Add(&ball2);


    // Camera
    double focalLength = 1.0;
    double viewportHeight = 2.0;
    double viewportWidth = viewportHeight * ((double) imageWidth / imageHeight);
    Vec3 cameraCenter = Point3(0,0,0);

    // Calculate the vectors across the horizontal and down the vertical viewport edges

    Vec3 viewportU = Vec3(viewportWidth, 0, 0);
    Vec3 viewportV = Vec3(0, -viewportHeight, 0);


    // Calculate the horizontal and verticla delta vectors from pixel to pixel
    Vec3 pixelDeltaU = viewportU / imageWidth;
    Vec3 pixelDeltaV = viewportV / imageHeight;

    // Calculate the location of the upper left pixel 
    Vec3 viewportUpperLeft = cameraCenter - Vec3(0, 0, focalLength) - viewportU / 2 - viewportV / 2;
    Vec3 pixel00Loc = viewportUpperLeft + 0.5 * (pixelDeltaU + pixelDeltaV);

    // Render

    std::cout << "P3\n" << imageWidth << " " << imageHeight << "\n255\n";

    for (int j = 0; j < imageHeight; j++)
    {
        std::clog << "\rScanlines remaining: " << (imageHeight - j) << ' ' << std::flush;
        for (int i = 0; i < imageWidth; i++)
        {
            Vec3 pixelCenter = pixel00Loc + (i * pixelDeltaU) + (j * pixelDeltaV);
            Vec3 rayDirection = pixelCenter - cameraCenter;
            Ray r(cameraCenter, rayDirection);

            Color pixelColor = RayColorStep6(r, world);

            WriteColor(std::cout, pixelColor);

        }

    }

    std::clog << "\rDone.              \n";

}