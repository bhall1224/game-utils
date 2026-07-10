#include <stdlib.h>
#include <math.h>

#ifndef linearalgebra
#define linearalgebra
#include "linear_algebra.h"
#endif

vector create_vector(vlen *num_dimensions, float *dimensions)
{
    vector v = malloc(sizeof *dimensions);

    for (int i = 0; i < *num_dimensions; i++)
    {
        v[i] = dimensions[i];
    }

    return v;
}


vector zero_vector(vlen *dimensions)
{
    float vector_arr[*dimensions];

    for (int i = 0; i < *dimensions; i++)
    {
        vector_arr[i] = 0.0f;
    }
    
    return create_vector(dimensions, vector_arr);
}


vector identity_vector(vlen *dimensions)
{
    float vector_arr[*dimensions];

    for (int i = 0; i < *dimensions; i++)
    {
        vector_arr[i] = 1.0f;
    }
    return create_vector(dimensions, vector_arr);
}


vector map_vector(vlen *v_size, vector base_vector, vector_transform op)
{
    return op(v_size, base_vector);
}

vector vector_map_list(vlen *v_size, vector base_vector, vector_transform op[]);

vector copy_vector(vlen *v_size, vector v_to_copy)
{
    float v_new[*v_size];

    for (int i = 0; i < *v_size; i++)
    {
        v_new[i] = v_to_copy[i];
    }

    return create_vector(v_size, v_new);
}


vector scale_vector(vlen *v_size, vector v_to_scale, float scalar)
{
    vector new_v = copy_vector(v_size, v_to_scale);

    for (int i = 0; i < *v_size; i++)
    {
        new_v[i] *= scalar;
    }

    return new_v;
}


vector add_vectors(vlen *v_size, vector va, vector vb)
{    
    vector new_v = copy_vector(v_size, va);

    for (int i = 0; i < *v_size; i++)
    {
        new_v[i] += vb[i];
    }

    return new_v;
}


vector add_all_vectors(vlen *v_size, vlen *arr_size, vector vectors[])
{
    vector sum_v = zero_vector(v_size);

    for (int i = 0; i < *arr_size; i++)
    {
        sum_v = add_vectors(v_size, sum_v, vectors[i]);
    }

    return sum_v;
}


float magnitude(vlen *v_size, vector v)
{
    // sqrt(sum(vx^2 in v))
    float mag = 0.0f;

    for (int i = 0; i < *v_size; i++)
    {
        mag += pow((double)v[i], 2.0);
    }

    mag = (float)sqrt((double)mag);

    return mag;
}

short int compare_vectors(vlen *v_size, vector va, vector vb)
{
    float ma = magnitude(v_size, va);
    float mb = magnitude(v_size, vb);

    if (ma > mb) return 1;
    else if (ma == mb) return 0;
    else return -1;
}