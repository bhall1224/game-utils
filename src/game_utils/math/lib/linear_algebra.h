typedef unsigned int vdimension;
typedef float *vector;
typedef void (*vector_transform)(vdimension*, vector);

vector create_vector(vdimension *num_dimension_ptr);
void delete_vector(vector v);

vector zero_vector(vdimension *num_dimensions_ptr);
vector identity_vector(vdimension *num_dimensions_ptr);

void set_v_dim_value(vdimension* ptr_dim_to_set, float *ptr_value_to_set, vector v_to_set);
void map_vector(vdimension *v_size_ptr, vector v_ref_to_map, vector_transform op);
void vector_map_list(vdimension *v_size_ptr, vdimension *op_arr_size,  vector v_ref_to_map, vector_transform op[]);
void scale_vector(vdimension *v_size_ptr, vector v_ref_to_scale, float *scalar_ptr);
void add_vectors(vdimension *v_size_ptr, vector v_ref_to_set, vector v_ref_to_use);
void add_all_vectors(vdimension *v_size_ptr, vdimension *arr_size_ptr, vector v_to_set, vector vctrs_to_sum[]);
void copy_and_release_vector(vdimension *v_size_ptr, vector v_to_set, vector v_cpy_rls);

float magnitude(vdimension *v_size_ptr, vector vector);
short int compare_vectors(vdimension *v_size_ptr, vector vctr_a, vector vctr_b);
