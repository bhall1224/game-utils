#ifndef stdlib
#define stdlib
#include <stdlib.h>
#endif

#ifndef physicsbody
#define physicsbody
#include "physics_body.h"
#endif

struct Transform *create_transform(vector *position, vector *rotation, vector *velocity, vector *gravity)
{
    struct Transform *transform = malloc(sizeof(struct Transform));

    if (!transform) return NULL;

    transform->gravity = gravity;
    transform->velocity = velocity;
    transform->rotation = rotation;
    transform->position = position;
    return transform;
}


struct PhysicsBody *create_physics_body(float *mass, float *friction, float *slip, struct Transform *transform)
{
    struct PhysicsBody *pbody = malloc(sizeof(struct PhysicsBody));

    if (!pbody) return NULL;

    pbody->mass = mass;
    pbody->friction = friction;
    pbody->slip = slip;
    pbody->transform = transform;

    return pbody;
}

vector *normal_force(struct PhysicsBody *body)
{
    // Calculate the normal force with vector for Gravity
    return scale_vector(*(body->mass), body->transform->gravity);
}


vector *friction_force(struct PhysicsBody *body)
{
    vector *zf = zero_vector();

    if (*(body->friction) == 0.0f)
    {
        return copy_vector(zf);
    }

    // static friction from body and normal forces
    vector *friction_force = scale_vector(*(body->friction), body->transform->velocity);
    friction_force = add_vectors(friction_force, normal_force(body));

    // if the body's velocity is not 0, calculate kinetic friction
    if (compare_vectors(body->transform->velocity, zf) > 0)
    {
        // Calculate the friction force using the coefficient of slip
        friction_force = scale_vector(*(body->slip), friction_force);
    }   

    return friction_force;
}


vector *move(float *dtime, vector *velocity, struct PhysicsBody *body)
{
    return scale_vector(*(dtime), add_vectors(velocity, body->transform->velocity));
}


vector *force(float *dtime, vector *acceleration, struct PhysicsBody *body)
{
    vector* force = scale_vector(
        *(body->mass), 
        scale_vector(*dtime, acceleration)
    );

    if (compare_vectors(force, friction_force(body)) > 0)
    {
        return force;
    }
    else
    {
        return add_vectors(force, scale_vector(-1, friction_force(body)));
    }
}


vector *rotate(float *dtime, float *rot_mag, vector *rotations, struct PhysicsBody *body)
{
    return add_vectors(scale_vector(*rot_mag, rotations), body->transform->rotation);
}


void apply_force_ptr_update(float *dtime, vector *acceleration, struct PhysicsBody *body)
{
    body->transform->velocity = force(dtime, acceleration, body);
}
