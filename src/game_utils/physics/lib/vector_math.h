typedef float vector[3];
typedef vector *(*vector_transform)(vector *);

const int VECTOR_SIZE = 3;

enum Dimensions
{
    X_AXIS,
    Y_AXIS,
    Z_AXIS
};

vector *create_vector(float x, float y, float z);
vector *zero_vector();
vector *identity_vector();
vector *map_vector(vector *base_vector, vector_transform op);
vector *map_many_vectors(vector *vectors[], vector_transform op);
vector *scale_vector(float scalar, vector *v_to_scale);
vector *add_vectors(vector *va, vector *vb);
vector *add_all_vectors(vector *vectors[]);
vector *copy_vector(vector *v_to_copy);
vector *from_arr(float arr[]);
float *to_arr(vector *v);
float magnitude(vector *v);
unsigned short int compare_vectors(vector *va, vector *vb);