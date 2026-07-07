// TODO: struct Quaternion {
//     float w;
//     float angle_of_rotation[3];
// };

typedef unsigned short int coordinate;

struct Transform
{
    float position[3];
    float rotation[3];    
    float velocity[3];
};

struct PhysicsBody
{
    float mass;
    float slip;        // Coefficient of slip for kinetic friction
    float friction; // Coefficient for static friction
    struct Transform transform;
    // Additional properties can be added here
};

float *move(float *dtime, float velocity[3], struct PhysicsBody *body);
float *rotate_by_axis(float *dtime, coordinate *axis, struct PhysicsBody *body);
float *rotate(float *dtime, float rotations[3], struct PhysicsBody *body);
float *force(float *dtime, float acceleration[3], struct PhysicsBody *body);
float *normal_force(struct PhysicsBody *body, coordinate* coord);
float *friction_force(struct PhysicsBody *body, coordinate* coord);
float friction_scalar(struct PhysicsBody *body);
float normal_scalar(struct PhysicsBody *body);