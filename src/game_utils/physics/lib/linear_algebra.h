typedef unsigned int vlen;
typedef float *vector;
typedef vector (*vector_transform)(vlen*, vector);

vector create_vector(vlen *num_dimensions, float *dimensions);
vector zero_vector(vlen *dimensions);
vector identity_vector(vlen *dimensions);
vector map_vector(vlen *v_size, vector base_vector, vector_transform op);
vector vector_map_list(vlen *v_size, vector base_vector, vector_transform op[]);
vector scale_vector(vlen *v_size, vector v_to_scale, float scalar);
vector add_vectors(vlen *v_size, vector va, vector vb);
vector add_all_vectors(vlen *v_size, vlen *arr_size, vector vectors[]);
vector copy_vector(vlen *v_size, vector v_to_copy);
float magnitude(vlen *v_size, vector v);
short int compare_vectors(vlen *v_size, vector va, vector vb);