#ifndef vectormath
#define vectormath
#include "vector_math.h"
#endif

typedef unsigned short int coordinate;

const float GRAVITY = 9.81f;

struct Transform
{
    vector *position;
    vector *rotation;    
    vector *velocity;
    vector *gravity;
};

struct PhysicsBody
{
    float *mass;
    float *slip;        // Coefficient of slip for kinetic friction
    float *friction; // Coefficient for static friction
    struct Transform *transform;
    // Additional properties can be added here
};

struct Transform *create_transform(vector *position, vector *rotation, vector *velocity, vector *gravity);
struct PhysicsBody *create_physics_body(float *mass, float *friction, float *slip, struct Transform *transform);

vector *move(float *dtime, vector *velocity, struct PhysicsBody *body);
vector *rotate(float *dtime, float *rot_mag, vector *rotations, struct PhysicsBody *body);
vector *force(float *dtime, vector *acceleration, struct PhysicsBody *body);
vector *normal_force(struct PhysicsBody *body);
vector *friction_force(struct PhysicsBody *body);
void apply_force_ptr_update(float *dtime, vector *acceleration, struct PhysicsBody *body);