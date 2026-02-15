
#include "RayTracingPCH.h"

#include "BVH.h"
#include "Camera.h"
#include "Hittable.h"
#include "HittableList.h"
#include "Sphere.h"
#include "Material.h"
#include "Texture.h"
#include "Timer.h"


void BouncingSphere()
{
    // World - Stack Allocation 
    HittableList world;
    std::vector<Sphere> sphereStorage;
    MaterialArena materialArena;

    sphereStorage.reserve(500);

    CheckerTexture checker = CheckerTexture(0.32, Color(0.1, 0.1, 0.1), Color(0.9, 0.9, 0.9));
    Lambertian groundMaterial = Lambertian(&checker);
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
                    auto center2 = center + Vec3(0, RandomDouble(0, 0.5), 0);
                    Sphere sphere = Sphere(center, center2, 0.2, matPtr);
                    sphereStorage.push_back(sphere);
                    world.Add(&sphereStorage.back());
                }
                else if (chooseMat < 0.9)
                {
                    //Metal
                    Color albedo = Color::Random(0.5, 1);
                    auto fuzz = RandomDouble(0, 0.5);
                    auto matPtr = materialArena.Create<Metal>(albedo, fuzz);
                    auto center2 = center + Vec3(RandomDouble(0, 0.5), 0, 0);
                    Sphere sphere = Sphere(center, center2, 0.2, matPtr);
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

    BVHTree tree = BVHTree(world);

    Camera cam(600, 16.0 / 9.0, 400, 40, 20);
    cam.LookFrom = Point3(13, 2, 3);
    cam.LookAt = Point3(0, 0, 0);
    cam.VUp = Vec3(0, 1, 0);

    cam.DefocusAngle = 0.6;
    cam.focusDist = 10.0;

    cam.Render(tree);
}

void CheckerSpheres()
{
    HittableList world;
    CheckerTexture checker = CheckerTexture(0.32, Color(0.1, 0.1, 0.1), Color(0.9, 0.9, 0.9));

    Lambertian lambertian1 = Lambertian(&checker);
    Lambertian lambertian2 = Lambertian(&checker);
    Sphere sphere1 = Sphere(Point3(0, -10, 0), 10, &lambertian1);
    Sphere sphere2 = Sphere(Point3(0, 10, 0), 10, &lambertian2);

    world.Add(&sphere1);
    world.Add(&sphere2);

    Camera cam(400, 16.0 / 9.0, 100, 50, 20);
    cam.LookFrom = Point3(13, 2, 3);
    cam.LookAt = Point3(0, 0, 0);
    cam.VUp = Vec3(0, 1, 0);

    cam.DefocusAngle = 0;
    cam.Render(world);

}


void Earth()
{
    ImageTexture earthTexture = ImageTexture("earthmap.jpg");
    Lambertian surface = Lambertian(&earthTexture);
    Sphere globe = Sphere(Point3(0, 0, 0), 2, &surface);

    Camera cam(400, 16.0 / 9.0, 100, 50, 20);

    cam.LookFrom = Point3(0, 0, 12);
    cam.LookAt = Point3(0, 0, 0);
    cam.VUp = Vec3(0, 1, 0);

    cam.DefocusAngle = 0;
    cam.Render(HittableList(&globe));

}

int main(int arg=1)
{
    Timer t("SandBox");
    switch (3)
    {
        case 1: BouncingSphere(); break;
        case 2: CheckerSpheres(); break;
        case 3: Earth(); break;
        default: BouncingSphere();
    }
}