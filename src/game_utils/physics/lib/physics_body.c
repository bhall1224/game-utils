#ifndef physicsbody
#define physicsbody
#include "physics_body.h"
#endif

#ifndef vectormath
#define vectormath
#include "vector_math.h"
#endif

const float GRAVITY = 9.81f;


float *normal_force(struct PhysicsBody *body, coordinate *coord)
{
    // Calculate the normal force with coord given for gravity
    vector* normal_axis = create_vector();
    *normal_axis[*coord] = body->mass * GRAVITY;
    return normal_axis; 
}


float *friction_force(struct PhysicsBody *body, coordinate *coord)
{
    if (body->friction == 0.0f)
    {
        return to_arr(
            copy_vector(IDENTITY_VECTOR)
        );
    }
    vector *vbody = from_arr(body->transform.velocity);

    // static friction from body and normal forces
    vector *friction_force = scale_vector(&body->friction, vbody);
    friction_force = add_vectors(friction_force, normal_force(body, coord));

    // if the body's velocity is not 0, calculate kinetic friction
    if (compare_vectors(vbody, ZERO_VECTOR) > 0)
    {
        // Calculate the friction force using the coefficient of slip
        friction_force = scale_vector(&body->slip, friction_force);
    }   

    return friction_force;
}

float normal_scalar(struct PhysicsBody *body)
{
    return GRAVITY * body->mass;
}

float friction_scalar(struct PhysicsBody *body)
{
    float fforce = normal_scalar(body) * body->friction;
};



float *move(float *dtime, float velocity[3], struct PhysicsBody *body)
{
    vector* v0 = from_arr(velocity);
    vector* v1 = scale_vector(dtime, add_vectors(v0, body->transform.velocity));

    return to_arr(v1);
}


float *force(float *dtime, float acceleration[3], struct PhysicsBody *body, coordinate *gravity_axis)
{
    vector* vnew = scale_vector(dtime, acceleration);
    vnew = scale_vector(&body->mass, vnew);
    vnew = add_vectors(vnew, body->transform.velocity);

    // if (magnitude(vnew)  magnitude(friction_force(body, gravity_axis)))
    // {
    // }
    // else
    // {
        
    // }
    return to_arr(vnew);
}


float *rotate(float *dtime, float rotations[3], struct PhysicsBody *body);

