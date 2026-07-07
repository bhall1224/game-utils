typedef float vector[3];
typedef vector *(*vector_transform)(vector *);

enum Dimensions
{
    X,
    Y,
    Z
};

const vector ZERO_VECTOR = {0.0f, 0.0f, 0.0f};
const vector IDENTITY_VECTOR = {1.0f, 1.0f, 1.0f};

vector *create_vector();
vector *create_vector_from_dim(const float *x, const float *y, const float *z);
vector *map_vector(vector *base_vector, vector_transform op);
vector *map_many_vectors(vector *vectors[], vector_transform op);
vector *scale_vector(float *scalar, vector *v_to_scale);
vector *add_vectors(vector *va, vector *vb);
vector *add_all_vectors(vector *vectors[]);
vector *from_arr(float arr[]);
vector *copy_vector(vector *v_to_copy);
float *to_arr(vector *v);
float magnitude(vector *v);
float get_from_vector(vector *v, coordinate *coord);
unsigned short int compare_vectors(vector *va, vector *vb);