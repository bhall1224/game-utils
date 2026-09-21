#ifndef vectormath
#define vectormath
#include "vector_math.h"
#endif

#ifndef stdlib
#define stdlib
#include <stdlib.h>
#endif

int vector_arr_length(vector *vectors[])
{
    if (vectors == NULL) return 0;

    int count = 0;
    while (vectors[count] != NULL)
    {
        count++;
    }
    return count;
}

vector *create_vector(float x, float y, float z)
{
    vector* v = malloc(sizeof(vector));

    (*v)[X_AXIS] = x;
    (*v)[Y_AXIS] = y;
    (*v)[Z_AXIS] = z;

    return v;
}


vector *zero_vector()
{
    return create_vector(0.0f, 0.0f, 0.0f);
}


vector *identity_vector()
{
    return create_vector(1.0f, 1.0f, 1.0f);
}


vector *map_vector(vector *base_vector, vector_transform op)
{
    return op(base_vector);
}


vector *map_many_vectors(vector *vectors[], vector_transform op)
{
    int v_len = vector_arr_length(vectors);

    if (v_len == 0) return NULL;

    vector *result_v;

    for (int i = 0; i < v_len; i++)
    {
        result_v = op(vectors[i]);
    }

    return result_v;
}


vector *copy_vector(vector *v_to_copy)
{
    return create_vector(*v_to_copy[X_AXIS], *v_to_copy[Y_AXIS], *v_to_copy[Z_AXIS]);
}


vector *scale_vector(float scalar, vector *v_to_scale)
{
    vector *new_v_ptr = copy_vector(v_to_scale);
    (*new_v_ptr)[X_AXIS] *= scalar;
    (*new_v_ptr)[Y_AXIS] *= scalar;
    (*new_v_ptr)[Z_AXIS] *= scalar;

    return new_v_ptr;
}


vector *add_vectors(vector *va, vector *vb)
{
    vector *new_v_ptr = copy_vector(va);
    (*new_v_ptr)[X_AXIS] += *vb[X_AXIS];
    (*new_v_ptr)[Y_AXIS] += *vb[Y_AXIS];
    (*new_v_ptr)[Z_AXIS] += *vb[Z_AXIS];

    return new_v_ptr;
}


vector *add_all_vectors(vector *vectors[])
{
    int v_len = vector_arr_length(vectors);

    vector *sum_v = copy_vector(vectors[0]);

    for (int i = 1; i < v_len; i++)
    {
        sum_v = add_vectors(sum_v, vectors[i]);
    }

    return sum_v;
}


float magnitude(vector *v);
unsigned short int compare_vectors(vector *va, vector *vb);