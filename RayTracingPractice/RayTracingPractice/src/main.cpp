
#include "RayTracingPCH.h"

#include "Camera.h"
#include "Hittable.h"
#include "HittableList.h"
#include "Sphere.h"
#include "Material.h"
#include "Timer.h"

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
void FinalRendererFixed()
{
    // World - Stack Allocation 
    HittableList world;
    std::vector<Sphere> sphereStorage;

    MaterialArena materialArena;

    sphereStorage.reserve(500);


    Lambertian groundMaterial = Lambertian(Color(0.5, 0.5, 0.5));
    Sphere ground = Sphere(Point3(0, -1000, 0), 1000, &groundMaterial);
    world.Add(&ground);

    for (int a = -11; a < 11; a++)
    {
        for (int b = -11; b < 11; b++)
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
                    auto matPtr = materialArena.Create<Lambertian>(albedo);
                    Sphere sphere = Sphere(center, 0.2, matPtr);
                    sphereStorage.push_back(sphere);
                    world.Add(&sphereStorage.back());
                }
                else if (chooseMat < 0.95)
                {
                    //Metal
                    Color albedo = Color::Random(0.5, 1);
                    auto fuzz = RandomDouble(0, 0.5);
                    auto matPtr = materialArena.Create<Metal>(albedo, fuzz);

                    Sphere sphere = Sphere(center, 0.2, matPtr);
                    sphereStorage.push_back(sphere);
                    world.Add(&sphereStorage.back());
                }
                else
                {
                    auto matPtr = materialArena.Create<Dielectric>(1.5);
                    Sphere sphere = Sphere(center, 0.2,matPtr);
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

    Camera cam(300, 16.0 / 9.0, 400, 40, 20);
    cam.LookFrom = Point3(13, 2, 3);
    cam.LookAt = Point3(0, 0, 0);
    cam.VUp = Vec3(0, 1, 0);

    cam.defocusAngle = 0.6;
    cam.focusDist = 10.0;

    cam.Render(world);
}
void FinalRenderer()
{
    // World - Stack Allocation 
    HittableList world;
    std::vector<Sphere> sphereStorage;
    std::vector<Material> materialStorage;

    sphereStorage.reserve(500);
    materialStorage.reserve(500);


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
                    materialStorage.push_back(Lambertian(albedo)); // Copy Construction
                    Sphere sphere = Sphere(center, 0.2, &materialStorage.back());
                    sphereStorage.push_back(sphere);
                    world.Add(&sphereStorage.back());
                }
                else if (chooseMat < 0.95)
                {
                    //Metal
                    Color albedo = Color::Random(0.5, 1);
                    auto fuzz = RandomDouble(0, 0.5);
                    materialStorage.push_back(Metal(albedo, fuzz));
                    Sphere sphere = Sphere(center, 0.2, &materialStorage.back());
                    sphereStorage.push_back(sphere);
                    world.Add(&sphereStorage.back());
                }
                else
                {
                    materialStorage.push_back(Dielectric(1.5));
                    Sphere sphere = Sphere(center, 0.2, &materialStorage.back());
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

int main()
{
    Timer t("SandBox");
    FinalRendererFixed();

}