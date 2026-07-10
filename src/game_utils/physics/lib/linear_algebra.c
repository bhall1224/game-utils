#include <stdlib.h>
#include <math.h>

#ifndef linearalgebra
#define linearalgebra
#include "linear_algebra.h"
#endif

vector create_vector(vdimension *num_dimension_ptr)
{
    vector v = calloc(*num_dimension_ptr, sizeof(float));

    return v;
}


void delete_vector(vector v)
{
    free(v);
}


vector zero_vector(vdimension *num_dimensions_ptr)
{
    // already initialized to 0's
    return create_vector(num_dimensions_ptr);
}



void set_v_dim_value(vdimension* ptr_dim_to_set, float *ptr_value_to_set, vector v_to_set)
{
    v_to_set[*ptr_dim_to_set] = *ptr_value_to_set;
}

vector identity_vector(vdimension *num_dimensions_ptr)
{
    float val = 1.0f;
    vector vi = create_vector(num_dimensions_ptr);

    // populate with 1's
    for (int i = 0; i < *num_dimensions_ptr; i++)
    {
        set_v_dim_value(num_dimensions_ptr, &val, vi);
    }

    return vi;
}

void map_vector(vdimension *v_size_ptr, vector v_ref_to_map, vector_transform op)
{
    op(v_size_ptr, v_ref_to_map);
}


void vector_map_list(vdimension *v_size_ptr, vdimension *op_arr_size,  vector v_ref_to_map, vector_transform op[])
{
    for (int i = 0; i < *op_arr_size; i++) 
    {
        op[i](v_size_ptr, v_ref_to_map);
    }
}


void scale_vector(vdimension *v_size_ptr, vector v_ref_to_scale, float *scalar_ptr)
{
    for (int i = 0; i < *v_size_ptr; i++)
    {
        v_ref_to_scale[i] *= *scalar_ptr;
    }
}


void add_vectors(vdimension *v_size_ptr, vector v_ref_to_set, vector v_ref_to_use)
{
    for (int i = 0; i < *v_size_ptr; i++)
    {
        v_ref_to_set[i] += v_ref_to_use[i];
    }
}


void add_all_vectors(vdimension *v_size_ptr, vdimension *arr_size_ptr, vector v_to_set, vector vctrs_to_sum[])
{
    for (int i = 0; i < *arr_size_ptr; i++)
    {
        add_vectors(v_size_ptr, v_to_set, vctrs_to_sum[i]);
    }
}


void copy_and_release_vector(vdimension *v_size_ptr, vector v_to_set, vector v_cpy_rls)
{
    for (int i = 0; i < *v_size_ptr; i++)
    {
        v_to_set[i] = v_cpy_rls[i];
    }

    delete_vector(v_cpy_rls);
}

float magnitude(vdimension *v_size_ptr, vector vector)
{
    // sqrt(sum(vx^2 in v))
    float mag = 0.0f;

    for (int i = 0; i < *v_size_ptr; i++)
    {
        mag += pow((double)vector[i], 2.0);
    }

    mag = (float)sqrt((double)mag);

    return mag;
}

short int compare_vectors(vdimension *v_size_ptr, vector vctr_a, vector vctr_b)
{
    float ma = magnitude(v_size_ptr, vctr_a);
    float mb = magnitude(v_size_ptr, vctr_b);

    if (ma > mb)
        return 1;
    else if (ma == mb)
        return 0;
    else
        return -1;
}