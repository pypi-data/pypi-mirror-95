#include <math.h>
#include <Python.h>
#include <stdio.h>

/*
This is VirxERLU-CLib!

Finding if a shot is viable is extremely expensive, and is unrealistic to do in Python.
Therfore, it's done in C!
Using C drastically improves run times, but it also takes a lot more time to develop.
Hence, I've tried my best to strike a nice balance.
Finding viable shot isn't the only thing VirxERLU-CLib does, although it is the main thing.
VirxERLU-CLib also runs some small physics simulations.
For example, it can find the time needed in order to jump a certain height.
It can also find if the car will land on the floor, ceiling, or a wall.

All of the things that VirxERLU-CLib does is very math-intensive, making C the perfect canidate as a language.
Combine this with the fact that you can call C functions inside your Python script, and you have a VERY speedy function!

GitHub repository: https://github.com/VirxEC/VirxERLU
Questions or comments? Join my Discord server! https://discord.gg/5ARzYRD2Na
Want to be notified of VirxERLU updates? You can get notifications by either Watching the github repo, or subscribe to VirxERLU updates on my Discord server!
*/

// Constants

static const double simulation_dt = 1. / 60.;
static const double physics_dt = 1. / 120.;

static const double min_shot_time = 0;
static const double max_shot_time = 6;
static const double max_shot_slope = 3;
static const double max_shot_0_slope = 10;
static const double ground_shot_min_slope = 0.4;
static const double jump_shot_min_slope = 0.75;
static const double double_jump_shot_min_slope = 1;
static const double aerial_shot_min_slope = 2;

static const double jump_max_duration = 0.2;
static const double jump_speed = 291. + (2. / 3.);
static const double jump_acc = 1458. + (1. / 3.);

static const double aerial_throttle_accel = 100. * (2. / 3.);
static const double boost_consumption = 100. * (1. / 3.);

static const double brake_force = 3500.;
static const double max_speed = 2300.;
static const double max_speed_no_boost = 1410.;
static const double max_boost = 100.;

static const double throttle_accel_division = 1400;
static const double start_throttle_accel_m = -36. / 35.;
static const double start_throttle_accel_b = 1600.;
static const double end_throttle_accel_m = -16.;
static const double end_throttle_accel_b = 160.;

static const double curvature_m_0_500 = 5.84e-6;
static const double curvature_b_0_500 = 0.0069;
static const double curvature_m_500_1000 = 3.26e-6;
static const double curvature_b_500_1000 = 0.00561;
static const double curvature_m_1000_1500 = 1.95e-6;
static const double curvature_b_1000_1500 = 0.0043;
static const double curvature_m_1500_1750 = 1.1e-6;
static const double curvature_b_1500_1750 = 0.003025;
static const double curvature_m_1750_2300 = 4e-7;
static const double curvature_b_1750_2300 = 0.0018;

static const double max_jump_height = 220;
static const double min_double_jump_height = 300;
static const double max_double_jump_height = 450;

static const double PI = 3.14159265358979323846;

static const double side_wall = 4080;
static const double goal_line = 5120;
static const double back_wall = 5110;
static const double ceiling = 2030;
static const double flooring = 20;

static const double legacy_default_gravity = 650;

static const char direction_forwards = 1;
static const char direction_backwards = -1;

static const unsigned char no_boost = 0;

// see further down for some global vector variables

enum ShotType
{
	GROUND_SHOT,
	JUMP_SHOT,
	DOUBLE_JUMP_SHOT,
	AERIAL_SHOT
};

// simple math stuff

static inline double cap(double value, double min_v, double max_v)
{
    return max(min(value, max_v), min_v);
}

static inline signed char sign(int value)
{
    return (value > 0) - (value < 0);
}

// Vector stuff

typedef struct vector
{
    double x;
    double y;
    double z;
} Vector;

Vector legacy_default_gravity_vector = {0, 0, 650};

static inline Vector add(Vector vec1, Vector vec2)
{
    return (Vector){vec1.x + vec2.x, vec1.y + vec2.y, vec1.z + vec2.z};
}

static inline Vector sub(Vector vec1, Vector vec2)
{
    return (Vector){vec1.x - vec2.x, vec1.y - vec2.y, vec1.z - vec2.z};
}

static inline Vector multiply(Vector vec1, Vector vec2)
{
    return (Vector){vec1.x * vec2.x, vec1.y * vec2.y, vec1.z * vec2.z};
}

static inline Vector divide(Vector vec1, Vector vec2)
{
    return (Vector){vec1.x / vec2.x, vec1.y / vec2.y, vec1.z / vec2.z};
}

static inline double dot(Vector vec1, Vector vec2)
{
    return vec1.x * vec2.x + vec1.y * vec2.y + vec1.z * vec2.z;
}

static inline double magnitude(Vector vec)
{
    return sqrt(dot(vec, vec));
}

static inline Vector double_to_vector(double num)
{
    return (Vector){num, num, num};
}

static inline Vector flatten(Vector vec)
{
    return (Vector){vec.x, vec.y, 0};
}

static inline Vector cross(Vector vec1, Vector vec2)
{
    return (Vector){(vec1.y * vec2.z) - (vec1.z * vec2.y), (vec1.z * vec2.x) - (vec1.x * vec2.z), (vec1.x * vec2.y) - (vec1.y * vec2.x)};
}

static inline double dist(Vector vec1, Vector vec2)
{
    return magnitude(sub(vec1, vec2));
}

static inline double flat_dist(Vector vec1, Vector vec2)
{
    return dist(flatten(vec1), flatten(vec2));
}

Vector normalize(Vector vec)
{
    double mag = magnitude(vec);

    if (mag != 0)
        return (Vector){vec.x / mag, vec.y / mag, vec.z / mag};

    return (Vector){0, 0, 0};
}

static inline double angle(Vector vec1, Vector vec2)
{
    return acos(cap(dot(normalize(vec1), normalize(vec2)), -1, 1));
}

static inline double angle2D(Vector vec1, Vector vec2)
{
    return angle(flatten(vec1), flatten(vec2));
}

Vector clamp2D(Vector vec, Vector start, Vector end)
{
    Vector s = normalize(vec);
    _Bool right = dot(s, cross(end, (Vector){0, 0, -1})) < 0;
    _Bool left = dot(s, cross(start, (Vector){0, 0, -1})) > 0;

    if ((dot(end, cross(start, (Vector){0, 0, -1})) > 0) ? (right && left) : (right || left))
        return vec;

    if (dot(start, s) < dot(end, s))
        return end;

    return start;
}

Vector clamp(Vector vec, Vector start, Vector end)
{
    Vector s = clamp2D(vec, start, end);
    double start_z = fmin(start.z, end.z);
    double end_z = fmax(start.z, end.z);

    if (s.z < start_z)
        s.z = start_z;
    else if (s.z > end_z)
        s.z = end_z;

    return s;
}

// orientation

typedef struct orientation
{
    Vector forward;
    Vector left;
    Vector up;
} Orientation;

static inline Vector localize(Orientation or_mat, Vector vec)
{
    return (Vector){dot(or_mat.forward, vec), dot(or_mat.left, vec), dot(or_mat.up, vec)};
}

// hitboxes

typedef struct hitbox
{
    double length;
    double width;
    double height;
    Vector offset;
} HitBox;

// other definitions

typedef struct target_vectors
{
    Vector left;
    Vector right;
} Target;

typedef struct post_correction
{
    Target targets;
    _Bool fits;
} PostCorrection;

PostCorrection default_post_correction = {{{0, 0, 0}, {0, 0, 0}}, 1};

typedef struct generic_shot
{
	_Bool found;
	_Bool fast;
	enum ShotType shot_type;
	Target targets;
} Shot;

Shot default_generic_shot = {0, 0, 0, {{0, 0, 0}, {0, 0, 0}}};

typedef struct car
{
    Vector location;
    Vector velocity;
    Orientation orientation;
    Vector angular_velocity;
    _Bool demolished;
    _Bool airborne;
    _Bool supersonic;
    _Bool jumped;
    _Bool doublejumped;
    unsigned char boost;
    unsigned char index;
    HitBox hitbox;
} Car;

Car default_car = {{0, 0, 0}, {0, 0, 0}, {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}}, {0, 0, 0}, 0, 0, 0, 0, 0, 0, 0, {0, 0, 0, {0, 0, 0}}};

typedef struct ball
{
    Vector location;
    Vector velocity;
} Ball;

Ball default_ball = {{0, 0, 0}, {0, 0, 0}};

typedef struct jump_time
{
    double press;
    double time;
} JumpTime;

JumpTime default_jump_time = {0, 0};

// legacy definitions

typedef struct legacy_jump_shot
{
    _Bool found;
    Vector best_shot_vector;
    Target targets;
} LegacyJumpShot;

LegacyJumpShot default_legacy_jump_shot = {0, {0, 0, 0}, {{0, 0, 0}, {0, 0, 0}}};

typedef struct legacy_aerial_shot
{
    _Bool found;
    _Bool fast;
    Vector ball_intercept;
    Vector best_shot_vector;
    Target targets;
} LegacyAerialShot;

LegacyAerialShot default_legacy_aerial_shot = {0, 0, {0, 0, 0}, {0, 0, 0}, {{0, 0, 0}, {0, 0, 0}}};

// extra math functions

PostCorrection correct_for_posts(Vector ball_location, Target *targets)
{
    int ball_radius = 95;
    Vector goal_line_perp = cross(sub(targets->right, targets->left), (Vector){0, 0, 1});

    Vector left_adjusted = add(targets->left, cross(normalize(sub(targets->left, ball_location)), (Vector){0, 0, -ball_radius}));
    Vector right_adjusted = add(targets->right, cross(normalize(sub(targets->right, ball_location)), (Vector){0, 0, ball_radius}));
    Vector left_corrected = (dot(sub(left_adjusted, targets->left), goal_line_perp) > 0.0) ? targets->left : left_adjusted;
    Vector right_corrected = (dot(sub(right_adjusted, targets->right), goal_line_perp) > 0.0) ? targets->right : right_adjusted;

    Vector left_to_right = sub(right_corrected, left_corrected);
    Vector new_goal_line = normalize(left_to_right);
    double new_goal_width = magnitude(left_to_right);

    Vector new_goal_perp = cross(new_goal_line, (Vector){0, 0, 1});
    Vector goal_center = add(left_corrected, multiply(multiply(new_goal_line, double_to_vector(new_goal_width)), double_to_vector(0.5)));
    Vector ball_to_goal = normalize(sub(goal_center, ball_location));

    return (PostCorrection){
        left_corrected,
        right_corrected,
        new_goal_width * fabs(dot(new_goal_perp, ball_to_goal)) > ball_radius * 2};
}

static inline _Bool in_2d_quarter_field(double point_x, double point_y, HitBox *car_hitbox)
{
    return point_x <= 4096 - car_hitbox->length / 2 && ((point_x >= 893 - car_hitbox->width && point_y <= 5120 - car_hitbox->length / 2) || point_x <= 893);
}

static inline _Bool in_2d_field(Vector *point_location, HitBox *car_hitbox)
{
    return in_2d_quarter_field(fabs(point_location->x), fabs(point_location->y), car_hitbox);
}

_Bool in_field(Vector *point_location, HitBox *car_hitbox)
{
    double point_z = fabs(point_location->z);
    return in_2d_quarter_field(fabs(point_location->x), fabs(point_location->y), car_hitbox) && point_z >= 0 + (car_hitbox->height / 2) && point_z <= 2044 - car_hitbox->height;
}

double find_slope(Vector shot_vector, Vector car_to_target)
{
    double d = dot(shot_vector, car_to_target);
    double e = fabs(dot(cross(shot_vector, (Vector){0, 0, 1}), car_to_target));

    if (e == 0)
        return 10 * sign((int)d);

    return max(min(d / e, 3), -3);
}

double throttle_acceleration(double car_velocity_x)
{
    double x = fabs(car_velocity_x);
    if (x >= max_speed_no_boost)
        return 0;

    // use y = mx + b to find the throttle acceleration
    if (x < throttle_accel_division)
        return start_throttle_accel_m * x + start_throttle_accel_b;

    x -= throttle_accel_division;
    return end_throttle_accel_m * x + end_throttle_accel_b;
}

static inline Vector get_shot_vector_2d(Vector *direction, Ball *ball_slice, Target *targets)
{
    return clamp2D(*direction, normalize(sub(targets->left, ball_slice->location)), normalize(sub(targets->right, ball_slice->location)));
}

static inline Vector get_shot_vector_3d(Vector *direction, Ball *ball_slice, Target *targets)
{
    return clamp(*direction, normalize(sub(targets->left, ball_slice->location)), normalize(sub(targets->right, ball_slice->location)));
}

static inline Vector get_ball_offset(Ball *ball_slice, Vector *shot_vector, double *ball_radius)
{
    return sub(ball_slice->location, multiply(*shot_vector, double_to_vector(*ball_radius)));
}

Vector get_final_target(Vector *ball_offset, Vector *shot_vector, Vector *car_to_ball, Car *me, double *T, double lower_cap)
{
    signed char side_of_shot = sign((int)dot(cross(*shot_vector, (Vector){0, 0, 1}), *car_to_ball));

    Vector car_to_offset_target = sub(*ball_offset, me->location);
    Vector car_to_offset_perp = cross(car_to_offset_target, (Vector){0, 0, side_of_shot});

    double adjustment = angle2D(car_to_offset_target, *shot_vector) * cap(*T, lower_cap, 3) * 750;
    return add(*ball_offset, multiply(normalize(car_to_offset_perp), double_to_vector(adjustment)));
}

double min_non_neg(double x, double y)
{
    return ((x < y && x >= 0) || (y < 0 && x >= 0)) ? x : y;
}

int smallest_element_index_no_negative(double work_array[], int work_array_length)
{
    int index = 0;
    for(int i = 1; i < work_array_length; i++)
    {
        if((work_array[i] > 0 && work_array[i] < work_array[index]) || (work_array[index] < 0 && work_array[i] > work_array[index]))
            index = i;
    }

    return index;
}

// solve for x
// y = a(x - h)^2 + k
// y - k = a(x - h)^2
// (y - k) / a = (x - h)^2
// sqrt((y - k) / a) = x - h
// sqrt((y - k) / a) + h = x
double vertex_quadratic_solve_for_x_min_non_neg(double a, double h, double k, double y)
{
    double v_sqrt = sqrt((y - k) / a);
    return min_non_neg(v_sqrt + h, -v_sqrt + h);
}

static inline double get_landing_time(double fall_distance, double falling_time_until_terminal_velocity, double falling_distance_until_terminal_velocity, double terminal_velocity, double k, double h, double g)
{
    return (fall_distance * sign((int)-g) <= falling_distance_until_terminal_velocity * sign((int)-g)) ? vertex_quadratic_solve_for_x_min_non_neg(g, h, k, fall_distance) : falling_time_until_terminal_velocity + ((fall_distance - falling_distance_until_terminal_velocity) / terminal_velocity);
}

int find_landing_plane(Vector l, Vector v, double g)
{
    if (fabs(l.y) >= goal_line || (v.x == 0 && v.y == 0 && g == 0))
        return 5;

    double times[] = { -1, -1, -1, -1, -1, -1 }; // { side_wall_pos, side_wall_neg, back_wall_pos, back_wall_neg, ceiling, floor }

    if (v.x != 0)
    {
        times[0] = (side_wall - l.x) / v.x;
        times[1] = (-side_wall - l.x) / v.x;
    }

    if (v.y != 0)
    {
        times[2] = (back_wall - l.y) / v.y;
        times[3] = (-back_wall - l.y) / v.y;
    }

    if (g != 0)
    {
        // this is the vertex of the equation, which also happens to be the apex of the trajectory
        double h = v.z / -g; // time to apex
        double k = v.z * v.z / -g; // vertical height at apex

        // a is the current gravity... because reasons
        // double a = g;

        double climb_dist = -l.z;

        // if the gravity is inverted, the the ceiling becomes the floor and the floor becomes the ceiling...
        if (g < 0)
        {
            climb_dist += ceiling;
            if (k >= climb_dist)
                times[4] = vertex_quadratic_solve_for_x_min_non_neg(g, h, k, climb_dist);
        }
        else if (g > 0)
        {
            climb_dist += flooring;
            if (k <= climb_dist)
                times[5] = vertex_quadratic_solve_for_x_min_non_neg(g, h, k, climb_dist);
        }

        // this is necessary because after we reach our terminal velocity, the equation becomes linear (distance_remaining / terminal_velocity)
        double terminal_velocity = (max_speed - magnitude(flatten(v))) * sign((int)g);
        double falling_time_until_terminal_velocity = (terminal_velocity - v.z) / g;
        double falling_distance_until_terminal_velocity = v.z * falling_time_until_terminal_velocity + -g * (falling_time_until_terminal_velocity * falling_time_until_terminal_velocity) / 2;

        double fall_distance = -l.z;
        if (g < 0)
            times[5] = get_landing_time(fall_distance + flooring, falling_time_until_terminal_velocity, falling_distance_until_terminal_velocity, terminal_velocity, k, h, g);
        else
            times[4] = get_landing_time(fall_distance + ceiling, falling_time_until_terminal_velocity, falling_distance_until_terminal_velocity, terminal_velocity, k, h, g);
    }

    return smallest_element_index_no_negative(times, 6);
}

// v is the magnitude of the velocity in the car's forward direction
double curvature(double v)
{
    if (0 <= v && v < 500)
        return curvature_b_0_500 - curvature_m_0_500 * v;

    if (500 <= v && v < 1000)
        return curvature_b_500_1000 - curvature_m_500_1000 * v;

    if (1000 <= v && v < 1500)
        return curvature_b_1000_1500 - curvature_m_1000_1500 * v;

    if (1500 <= v && v < 1750)
        return curvature_b_1500_1750 - curvature_m_1500_1750 * v;

    if (1750 <= v && v < 2500)
        return curvature_b_1750_2300 - curvature_m_1750_2300 * v;

    return 0;
}

static inline double turn_radius(double v)
{
    return 1. / curvature(v);
}

// use y=mx+b to linearly scale the minimum shot slope
double get_adjusted_min_slope(double *T, double *jump_time, const double *min_shot_slope)
{
    double m = (*min_shot_slope - (max_shot_slope + *jump_time / 2)) / (max_shot_time - *jump_time);
    double b = *min_shot_slope - m * max_shot_time;
    
    return m * *T + b;
}

// physics simulations

JumpTime get_jump_time(double car_to_target_z, double car_z_velocity, double gravity_z)
{
    JumpTime r = default_jump_time;
    double l = 0;
    double v = car_z_velocity;
    double g = gravity_z * simulation_dt;
    double g2 = 2 * gravity_z;
    double ja = jump_acc * simulation_dt;

    v += jump_speed;
    v += gravity_z * physics_dt;
    l += v * physics_dt;
    r.time += physics_dt;

    // we can only hold the jump button for max 0.2 seconds
    while (car_to_target_z - l > 0)
    {
        if (r.time <= jump_max_duration && car_to_target_z - l > (v * v) / g2)
            r.press += simulation_dt;
            v += ja;

        v += g;

        if (v <= 0)
            return r;

        l += v * simulation_dt;
        r.time += simulation_dt;
    }

    return r;
}

JumpTime get_double_jump_time(double car_to_target_z, double car_z_velocity, double gravity_z)
{
    JumpTime r = default_jump_time;
    double l = 0;
    double v = car_z_velocity;
    double g = gravity_z * simulation_dt;
    double g2 = 2 * gravity_z;
    double ja = jump_acc * simulation_dt;
    int c = 0;

    _Bool jump_done = 0;

    v += jump_speed;
    v += gravity_z * physics_dt;
    l += v * physics_dt;
    r.time += physics_dt;

    // we can only hold the jump button for max 0.2 seconds
    while (car_to_target_z - l > 0)
    {
        if (c == 1)
            v += jump_speed;

        if (!jump_done)
        {
            if (r.time > jump_max_duration)
                jump_done = 1;
            else
            {
                double v_inc = v + jump_speed;
                if (car_to_target_z - l > (v_inc * v_inc) / g2)
                {
                    r.press += simulation_dt;
                    v += ja;
                }
                else
                    jump_done = 1;
            }
        }
        else if (c < 2)
            c++;

        v += g;

        if (v <= 0)
            return r;

        l += v * simulation_dt;
        r.time += simulation_dt;
    }

    return r;
}


double time_to_speed(double boost_accel, double velocity, unsigned char car_boost, double target_speed)
{
    double T = 0;
    double b = (double)car_boost;
    double v = velocity;
    double t = 0;
    char ts = 0;

    const double ba_dt = boost_accel * simulation_dt;
    const double bc_dt = boost_consumption * simulation_dt;
    const double bk_dt = brake_force * simulation_dt;
    const double r = target_speed;

    if (r > ((b < bc_dt && v <= max_speed_no_boost) ? max_speed_no_boost : max_speed) || (b < bc_dt && v > max_speed_no_boost && r > v))
        return -1;

    if (fabs(v - r) < 60)
        return 0;

    while (!(r > ((b < bc_dt && v <= max_speed_no_boost) ? max_speed_no_boost : max_speed) || (b < bc_dt && v > max_speed_no_boost && r > v)))
    {
        t = r - v;
        ts = sign((int)(t));

        v += (ts == -sign((int)v)) ? (bk_dt * ts) : (throttle_acceleration(v) * simulation_dt * ts);

        if (b > bc_dt && v < max_speed && v >= 0 && t >= ba_dt)
        {
            v += ba_dt;

            if (v > max_speed)
                v = max_speed;

            if (b <= max_boost)
	            b -= bc_dt;
        }

        T += simulation_dt;

        if (fabs(t) < 60)
            return T;
    }

    return -1;
}

_Bool can_reach_target(double max_time, double distance_remaining, double boost_accel, double velocity, unsigned char car_boost, char direction)
{
    double d = distance_remaining;
    double T = max_time;
    double b = (double)car_boost;
    double v = velocity;
    int t = 0;
    char ts = 0;

    const double ba_dt = boost_accel * simulation_dt;
    const double bc_dt = boost_consumption * simulation_dt;
    const double bk_dt = brake_force * simulation_dt;
    const double r = max_time / d * direction;

    if (r > ((b < bc_dt && v <= max_speed_no_boost) ? max_speed_no_boost : max_speed) || (b < bc_dt && v > max_speed_no_boost && r > v))
        return 0;

    if (fabs(v - r) < 100)
        return 1;

    while (T >= -simulation_dt && !(r > ((b < bc_dt && v <= max_speed_no_boost) ? max_speed_no_boost : max_speed) || (b < bc_dt && v > max_speed_no_boost && r > v)))
    {
        t = (int)(r - v);
        ts = sign(t);

        v += (ts == -sign((int)v)) ? (bk_dt * ts) : (throttle_acceleration(v) * simulation_dt * ts);

        if (b > bc_dt && v < max_speed && v >= 0 && t >= ba_dt)
        {
            v += ba_dt;

            if (v > max_speed)
                v = max_speed;

            if (b <= max_boost)
	            b -= bc_dt;
        }

        d -= v * simulation_dt;
        T -= simulation_dt;

        if (d <= 0 || abs(t) < 100 || v * direction > r)
            return 1;
    }

    return 0;
}

// Parsing shot slices

_Bool legacy_generic_is_viable(double *T, double jump_time, double *boost_accel, Vector *car_forward, double *car_speed, unsigned char *car_boost, Vector direction, double *distance_remaining, double *total_jump_accel)
{
    if (*distance_remaining < 25 && *T > jump_time)
        return 1;

	if (*T <= 0 || *distance_remaining / *T > max_speed_no_boost)
		return 0;

	double forward_angle = fabs(angle2D(direction, *car_forward));
	double backward_angle = PI - forward_angle;

    double abs_car_speed = fabs(*car_speed);
    double turn_rad = turn_radius(abs_car_speed);

    double forward_time = *T;
    double backward_time = *T;

    if (abs_car_speed > 400)
    {
        double turn_rad = turn_radius(*car_speed);
        forward_time -= forward_angle * turn_rad / *car_speed * 0.95;
        backward_time -= backward_angle * turn_rad / *car_speed * 0.95;
    }
    else
    {
        forward_time -= 1.8 * (forward_angle / PI);
        backward_time -= 1.8 * (backward_angle / PI);
    }

    if (forward_time > 0 && can_reach_target(forward_time, *distance_remaining, *boost_accel, *car_speed, *car_boost, direction_forwards))
        return 1;

    return backward_time > 0 && forward_angle >= 1.6 && *car_speed <= 1000 && can_reach_target(backward_time, *distance_remaining, *boost_accel, *car_speed, no_boost, direction_backwards);
}

_Bool generic_is_viable(double *T, double jump_time, double *boost_accel, Car *me, Vector direction, double *distance_remaining, double *total_jump_accel)
{
    if (*distance_remaining < me->hitbox.length * 0.05 && *T > jump_time)
        return 1;

	if (*T <= 0 || *distance_remaining / *T > max_speed)
		return 0;

    double forward_angle = fabs(angle2D(direction, me->orientation.forward));
    double backward_angle = PI - forward_angle;

    double true_car_speed = dot(me->orientation.forward, me->velocity);
    double car_speed = fabs(true_car_speed);

    double time = *T - jump_time;
    double forward_time, backward_time;

    if (fabs(car_speed) > 400)
    {
        double turn_rad = turn_radius(car_speed);
        forward_time = time - (forward_angle * turn_rad / car_speed * 0.95);
        backward_time = time - (backward_angle * turn_rad / car_speed * 0.95);
    }
    else
    {
        forward_time = time - (1.8 * (forward_angle / PI));
        backward_time = time - (1.8 * (backward_angle / PI));
    }

    if (forward_time > 0 && can_reach_target(forward_time, *distance_remaining, *boost_accel, true_car_speed, me->boost, direction_forwards))
        return 1;

    return backward_time > 0 && forward_angle >= 1.6 && *distance_remaining / backward_time <= max_speed_no_boost && can_reach_target(backward_time, *distance_remaining, *boost_accel, true_car_speed, 0, direction_backwards);
}

_Bool legacy_ground_shot_is_viable(double *T, HitBox *hitbox, double *boost_accel, double *car_z, double *distance_remaining, Vector *direction, Vector *car_forward, unsigned char *car_boost, double *car_speed, double slope)
{
    double total_jump_accel = 0;
    double slope_jump_time = 0.2;

    if (multiply(*direction, double_to_vector(*distance_remaining)).z + *car_z >= 92.75 + (hitbox->height / 2) || slope < get_adjusted_min_slope(T, &slope_jump_time, &ground_shot_min_slope))
        return 0;

    Car me = default_car;
    me.location.z = *car_z;

	return legacy_generic_is_viable(T, 0, boost_accel, car_forward, car_speed, car_boost, *direction, distance_remaining, &total_jump_accel);
}

_Bool ground_shot_is_viable(double *T, double *boost_accel, Car *me, double offset_target_z, Vector *direction, double *distance_remaining, double slope)
{
    double total_jump_accel = 0;
    double slope_jump_time = 0.05;

    if (offset_target_z >= me->hitbox.height || me->airborne || slope < get_adjusted_min_slope(T, &slope_jump_time, &ground_shot_min_slope))
        return 0;

    return generic_is_viable(T, 0, boost_accel, me, *direction, distance_remaining, &total_jump_accel);
}

Shot legacy_parse_slice_for_ground_shot_with_target(double *time_remaining, double *ball_radius, double *boost_accel, Ball *ball_slice, Car *me, Target *targets)
{
    Shot r = default_generic_shot;

    Vector car_to_ball = sub(ball_slice->location, me->location);
    Vector direction = normalize(car_to_ball);

    PostCorrection post_info = correct_for_posts(ball_slice->location, targets);

    if (post_info.fits)
    {
        r.targets = post_info.targets;
        Vector shot_vector = get_shot_vector_2d(&direction, ball_slice, &r.targets);
        double slope = find_slope(flatten(shot_vector), flatten(car_to_ball));
        Vector ball_offset = get_ball_offset(ball_slice, &shot_vector, ball_radius);
        Vector final_target = get_final_target(&ball_offset, &shot_vector, &car_to_ball, me, time_remaining, 0);
        double distance_remaining = flat_dist(final_target, me->location) - (me->hitbox.length / 3);
        Vector final_direction = normalize(sub(final_target, me->location));

        r.found = legacy_ground_shot_is_viable(time_remaining, &me->hitbox, boost_accel, &me->location.z, &distance_remaining, &final_direction, &me->orientation.forward, &me->boost, &me->velocity.x, slope);
    }

    return r;
}

_Bool legacy_parse_slice_for_ground_shot(double *time_remaining, double *ball_radius, double *boost_accel, Ball *ball_slice, Car *me)
{
    Vector car_to_ball = sub(ball_slice->location, me->location);
    Vector direction = normalize(car_to_ball);
    Vector ball_offset = get_ball_offset(ball_slice, &direction, ball_radius);
    double distance_remaining = flat_dist(ball_offset, me->location) - (me->hitbox.length / 3);
    Vector offset_direction = normalize(sub(ball_offset, me->location));

    return legacy_ground_shot_is_viable(time_remaining, &me->hitbox, boost_accel, &me->location.z, &distance_remaining, &offset_direction, &me->orientation.forward, &me->boost, &me->velocity.x, max_shot_0_slope);
}

_Bool legacy_jump_shot_is_viable(double *T, double *boost_accel, double *distance_remaining, Vector *direction, Vector *car_forward, unsigned char *car_boost, double *car_speed, double slope)
{
    double offset_target_z = multiply(*direction, double_to_vector(*distance_remaining)).z + 17;
    JumpTime jump_info = get_jump_time(offset_target_z, 0, legacy_default_gravity);

    if (offset_target_z < 92.75 || offset_target_z > max_jump_height || slope < get_adjusted_min_slope(T, &jump_info.time, &jump_shot_min_slope))
        return 0;

    double speed_reduction = jump_speed + (jump_acc * jump_info.press);

    return legacy_generic_is_viable(T, jump_info.time, boost_accel, car_forward, car_speed, car_boost, *direction, distance_remaining, &speed_reduction);
}

_Bool jump_shot_is_viable(double *T, double *boost_accel, Vector *gravity, Car *me, double offset_target_z, Vector *direction, double *distance_remaining, double slope)
{
    JumpTime jump_info = get_jump_time(offset_target_z, me->velocity.z, gravity->z);

    if (*T - jump_info.time <= 0 || offset_target_z < me->hitbox.height || offset_target_z > max_jump_height + (me->hitbox.height / 2) || me->airborne || slope < get_adjusted_min_slope(T, &jump_info.time, &jump_shot_min_slope))
        return 0;

    double jump_accel = jump_speed + (jump_acc * jump_info.press);

    return generic_is_viable(T, jump_info.time, boost_accel, me, *direction, distance_remaining, &jump_accel);
}

LegacyJumpShot legacy_parse_slice_for_jump_shot_with_target(double *time_remaining, double *ball_radius, double *boost_accel, Car *me, Ball *ball_slice, Target *targets)
{
    LegacyJumpShot r = default_legacy_jump_shot;

    Vector car_to_ball = sub(ball_slice->location, me->location);
    Vector direction = normalize(car_to_ball);

    PostCorrection post_info = correct_for_posts(ball_slice->location, targets);

    if (post_info.fits)
    {
        r.targets = post_info.targets;
        Vector shot_vector = get_shot_vector_2d(&direction, ball_slice, &r.targets);
        r.best_shot_vector = shot_vector;
        double slope = find_slope(flatten(shot_vector), flatten(car_to_ball));
        Vector ball_offset = get_ball_offset(ball_slice, &shot_vector, ball_radius);
        Vector final_target = get_final_target(&ball_offset, &shot_vector, &car_to_ball, me, time_remaining, 0);
        double distance_remaining = flat_dist(final_target, me->location);
        Vector final_direction = normalize(sub(final_target, me->location));

        r.found = legacy_jump_shot_is_viable(time_remaining, boost_accel, &distance_remaining, &final_direction, &me->orientation.forward, &me->boost, &me->velocity.x, slope);
    }

    return r;
}

LegacyJumpShot legacy_parse_slice_for_jump_shot(double *time_remaining, double *ball_radius, double *boost_accel, Ball *ball_slice, Car *me)
{
    LegacyJumpShot r = default_legacy_jump_shot;

    Vector car_to_ball = sub(ball_slice->location, me->location);
    Vector direction = normalize(car_to_ball);
    Vector ball_offset = sub(ball_slice->location, multiply(direction, double_to_vector(*ball_radius)));
    double distance_remaining = flat_dist(ball_offset, me->location);
    Vector offset_direction = normalize(sub(ball_offset, me->location));

    r.best_shot_vector = direction;
    r.found = legacy_jump_shot_is_viable(time_remaining, boost_accel, &distance_remaining, &offset_direction, &me->orientation.forward, &me->boost, &me->velocity.x, max_shot_0_slope);
    return r;
}

_Bool legacy_double_jump_shot_is_viable(double *T, double *boost_accel, double *distance_remaining, Vector *direction, Vector *car_forward, unsigned char *car_boost, double *car_speed, double slope)
{
    double offset_target_z = multiply(*direction, double_to_vector(*distance_remaining)).z + 17;
    JumpTime jump_info = get_double_jump_time(offset_target_z, 0, legacy_default_gravity);

    if (offset_target_z < min_double_jump_height || offset_target_z > max_double_jump_height || slope < get_adjusted_min_slope(T, &jump_info.time, &double_jump_shot_min_slope))
        return 0;

    double forward_angle = angle2D(*direction, *car_forward);
    double forward_time = *T - (forward_angle * 0.318);
    double jump_time = jump_info.time * 1.05;
    double total_jump_accel = (2 * jump_speed) + (jump_acc * jump_info.press);

    return forward_time > 0 && can_reach_target(forward_time, *distance_remaining, *boost_accel, *car_speed, *car_boost, direction_forwards);
}

_Bool double_jump_shot_is_viable(double *T, double *boost_accel, Vector *gravity, Car *me, double offset_target_z, Vector *direction, double *distance_remaining, double slope)
{
    JumpTime jump_info = get_double_jump_time(offset_target_z, me->velocity.z, gravity->z);

    if (*T - jump_info.time <= 0 || offset_target_z < min_double_jump_height + (me->hitbox.height / 2) || offset_target_z > max_double_jump_height + (me->hitbox.height / 2) || me->airborne || slope < get_adjusted_min_slope(T, &jump_info.time, &double_jump_shot_min_slope))
        return 0;

    double total_jump_accel = (2 * jump_speed) + (jump_acc * jump_info.press);

    return generic_is_viable(T, jump_info.time, boost_accel, me, *direction, distance_remaining, &total_jump_accel);
}

LegacyJumpShot legacy_parse_slice_for_double_jump_shot_with_target(double *time_remaining, double *ball_radius, double *boost_accel, Car *me, Ball *ball_slice, Target *targets)
{
    LegacyJumpShot r = default_legacy_jump_shot;

    Vector car_to_ball = sub(ball_slice->location, me->location);
    Vector direction = normalize(car_to_ball);

    PostCorrection post_info = correct_for_posts(ball_slice->location, targets);

    if (post_info.fits)
    {
        r.targets = post_info.targets;
        Vector shot_vector = get_shot_vector_2d(&direction, ball_slice, &r.targets);
        r.best_shot_vector = shot_vector;
        double slope = find_slope(flatten(shot_vector), flatten(car_to_ball));
        Vector ball_offset = get_ball_offset(ball_slice, &shot_vector, ball_radius);
        Vector final_target = get_final_target(&ball_offset, &shot_vector, &car_to_ball, me, time_remaining, 0);
        double distance_remaining = flat_dist(final_target, me->location);
        Vector final_direction = normalize(sub(final_target, me->location));

        r.found = legacy_double_jump_shot_is_viable(time_remaining, boost_accel, &distance_remaining, &final_direction, &me->orientation.forward, &me->boost, &me->velocity.x, slope);
    }

    return r;
}

LegacyJumpShot legacy_parse_slice_for_double_jump_shot(double *time_remaining, double *ball_radius, double *boost_accel, Ball *ball_slice, Car *me)
{
    LegacyJumpShot r = default_legacy_jump_shot;

    Vector car_to_ball = sub(ball_slice->location, me->location);
    Vector direction = normalize(car_to_ball);
    Vector ball_offset = sub(ball_slice->location, multiply(direction, double_to_vector(*ball_radius)));
    double distance_remaining = flat_dist(ball_offset, me->location);
    Vector offset_direction = normalize(sub(ball_offset, me->location));

    r.best_shot_vector = direction;
    r.found = legacy_double_jump_shot_is_viable(time_remaining, boost_accel, &distance_remaining, &offset_direction, &me->orientation.forward, &me->boost, &me->velocity.x, max_shot_0_slope);
    return r;
}

_Bool aerial_shot_is_viable(double T, double boost_accel, Vector gravity, Car *me, Vector target, _Bool *fast, _Bool safe)
{
	if (T <= 0.2)
		return 0;

    boost_accel += aerial_throttle_accel;

    Vector Tv = double_to_vector(T);
    Vector vf = add(me->velocity, multiply(gravity, Tv));
    Vector xf = add(add(me->location, multiply(me->velocity, Tv)), multiply(multiply(multiply(double_to_vector(0.5), gravity), Tv), Tv));

    _Bool ceiling = me->location.z > 2044 - (me->hitbox.height * 2) && !me->jumped;

    if (!me->airborne && !ceiling)
    {
        vf = add(vf, multiply(me->orientation.up, double_to_vector(2 * jump_speed + jump_acc * jump_max_duration)));
        xf = add(xf, multiply(me->orientation.up, double_to_vector(jump_speed * (2 * T - jump_max_duration) + jump_acc * (T * jump_max_duration - 0.5 * jump_max_duration * jump_max_duration))));
    }

    if (ceiling)
        target.z -= 92;

    Vector delta_x = sub(target, xf);
    Vector f = normalize(delta_x);

    double phi = angle(f, me->orientation.forward);
    double turn_time = 0.7 * (2 * sqrt(phi / 9));
    double tau1 = turn_time * cap(1 - 0.3 / phi, 0, 1);
    double required_acc = (2 * magnitude(delta_x) / ((T - tau1) * (T - tau1)));
    double ratio = required_acc / boost_accel;
    double tau2 = T - (T - tau1) * sqrt(1 - cap(ratio, 0, 1));
    int boost_estimate = (int)floor((tau2 - tau1) * 30);

    Vector velocity_estimate = add(vf, multiply(f, double_to_vector(boost_accel * (tau2 - tau1))));

    _Bool enough_boost = 0;
    _Bool enough_time = 0;
    _Bool enough_speed = 0;

    if (safe)
    {
        enough_boost = (me->boost == 232) ? 1 : boost_estimate < 0.95 * me->boost;
        enough_time = fabs(ratio) < 0.9;
        enough_speed = magnitude(velocity_estimate) < 0.9 * max_speed;
    }
    else
    {
        enough_boost = (me->boost == 232) ? 1 : boost_estimate < me->boost;
        enough_time = fabs(ratio) < 1;
        enough_speed = magnitude(velocity_estimate) < max_speed;
    }

    _Bool found = enough_speed && enough_boost && enough_time;
    if (found && !me->airborne)
        *fast = 1;

    if (!me->airborne && (T < 1.45 || !found))
    {
        Vector vf = add(me->velocity, multiply(gravity, Tv));
        Vector xf = add(add(me->location, multiply(me->velocity, Tv)), multiply(multiply(multiply(double_to_vector(0.5), gravity), Tv), Tv));

        vf = add(vf, multiply(me->orientation.up, double_to_vector(jump_speed + jump_acc * jump_max_duration)));
        xf = add(xf, multiply(me->orientation.up, double_to_vector(jump_speed * T + jump_acc * (T * jump_max_duration - 0.5 * jump_max_duration * jump_max_duration))));

        Vector delta_x = sub(target, xf);
        Vector f = normalize(delta_x);

        double phi = angle(f, me->orientation.forward);
        double turn_time = 0.7 * (2 * sqrt(phi / 9));
        double tau1 = turn_time * cap(1 - 0.3 / phi, 0, 1);
        double required_acc = (2 * magnitude(delta_x) / ((T - tau1) * (T - tau1)));
        double ratio = required_acc / boost_accel;
        double tau2 = T - (T - tau1) * sqrt(1 - cap(ratio, 0, 1));
        int boost_estimate = (int)floor((tau2 - tau1) * 30);

        Vector velocity_estimate = add(vf, multiply(f, double_to_vector(boost_accel * (tau2 - tau1))));

        _Bool enough_boost = 0;
        _Bool enough_time = 0;
        _Bool enough_speed = 0;

        if (safe)
        {
            enough_boost = (me->boost == 232) ? 1 : boost_estimate < 0.95 * me->boost;
            enough_time = fabs(ratio) < 0.9;
            enough_speed = magnitude(velocity_estimate) < 0.9 * max_speed;
        }
        else
        {
            enough_boost = (me->boost == 232) ? 1 : boost_estimate < me->boost;
            enough_time = fabs(ratio) < 1;
            enough_speed = magnitude(velocity_estimate) < max_speed;
        }

        if (enough_speed && enough_boost && enough_time)
        {
            found = 1;
            *fast = 0;
        }
    }

    return found;
}

LegacyAerialShot legacy_parse_slice_for_aerial_shot_with_target(double *time_remaining, double *ball_radius, double *boost_accel, Vector *gravity, Ball *ball_slice, Car *me, Target *targets)
{
    LegacyAerialShot r = default_legacy_aerial_shot;

    Vector car_to_ball = sub(ball_slice->location, me->location);
    Vector direction = normalize(car_to_ball);

    PostCorrection post_info = correct_for_posts(ball_slice->location, targets);
    if (post_info.fits)
    {
        r.targets = post_info.targets;
        r.best_shot_vector = clamp(direction, normalize(sub(r.targets.left, ball_slice->location)), normalize(sub(r.targets.right, ball_slice->location)));

        if (find_slope(r.best_shot_vector, car_to_ball) > aerial_shot_min_slope)
        {
            r.ball_intercept = get_ball_offset(ball_slice, &r.best_shot_vector, ball_radius);
            r.found = aerial_shot_is_viable(*time_remaining, *boost_accel, *gravity, me, r.ball_intercept, &r.fast, 1);
        }
    }

    return r;
}

LegacyAerialShot legacy_parse_slice_for_aerial_shot(double *time_remaining, double *ball_radius, double *boost_accel, Vector *gravity, Ball *ball_slice, Car *me)
{
    LegacyAerialShot r = default_legacy_aerial_shot;

    Vector car_to_ball = sub(ball_slice->location, me->location);
    r.best_shot_vector = normalize(car_to_ball);
    r.ball_intercept = get_ball_offset(ball_slice, &r.best_shot_vector, ball_radius);

    r.found = aerial_shot_is_viable(*time_remaining, *boost_accel, *gravity, me, r.ball_intercept, &r.fast, 1);
    return r;
}

Shot parse_slice_for_shot_with_target(_Bool do_ground_shot, _Bool do_jump_shot, _Bool do_double_jump_shot, _Bool do_aerial_shot, double *time_remaining, double *ball_radius, double *boost_accel, Vector *gravity, Ball *ball_slice, Car *me, Target *targets)
{
	Shot r = default_generic_shot;

	Vector car_to_ball = sub(ball_slice->location, me->location);
	Vector direction = normalize(car_to_ball);

	PostCorrection post_info = correct_for_posts(ball_slice->location, targets);
	if(post_info.fits)
	{
		r.targets = post_info.targets;

		if (do_ground_shot || do_jump_shot)
		{
            Vector shot_vector = get_shot_vector_2d(&direction, ball_slice, &r.targets);
            Vector ball_offset = get_ball_offset(ball_slice, &shot_vector, ball_radius);
			double slope = find_slope(flatten(shot_vector), flatten(car_to_ball));

            if (in_2d_field(&ball_offset, &me->hitbox))
            {
                double distance_remaining = flat_dist(ball_offset, me->location) - (me->hitbox.length * 0.45);
                Vector final_target = get_final_target(&ball_offset, &shot_vector, &car_to_ball, me, time_remaining, 0.5);
                Vector final_direction = normalize(sub(final_target, me->location));

                if (do_ground_shot)
                {
                    r.found = ground_shot_is_viable(time_remaining, boost_accel, me, ball_offset.z, &final_direction, &distance_remaining, slope);
                    r.shot_type = GROUND_SHOT;
                }

                if (do_jump_shot && !r.found)
                {
                    r.found = jump_shot_is_viable(time_remaining, boost_accel, gravity, me, ball_offset.z, &final_direction, &distance_remaining, slope);
                    r.shot_type = JUMP_SHOT;
                }
            }
		}

		if (!r.found && (do_double_jump_shot || do_aerial_shot))
		{
            Vector shot_vector = get_shot_vector_3d(&direction, ball_slice, &r.targets);
            Vector ball_offset = get_ball_offset(ball_slice, &shot_vector, ball_radius);

            if (do_double_jump_shot && in_2d_field(&ball_offset, &me->hitbox))
            {
                double slope = find_slope(flatten(shot_vector), flatten(car_to_ball));
                Vector final_target = get_final_target(&ball_offset, &shot_vector, &car_to_ball, me, time_remaining, 0);
                double distance_remaining = flat_dist(ball_offset, me->location) - (me->hitbox.length * 0.45);
                Vector final_direction = normalize(sub(final_target, me->location));

                r.found = double_jump_shot_is_viable(time_remaining, boost_accel, gravity, me, ball_offset.z, &final_direction, &distance_remaining, slope);
                r.shot_type = DOUBLE_JUMP_SHOT;
            }

            if (do_aerial_shot && !r.found && in_field(&ball_offset, &me->hitbox) && find_slope(shot_vector, car_to_ball) > aerial_shot_min_slope)
            {
                r.found = aerial_shot_is_viable(*time_remaining, *boost_accel, *gravity, me, ball_offset, &r.fast, 1);
                r.shot_type = AERIAL_SHOT;
            }
		}
	}

	return r;
}

Shot parse_slice_for_shot(_Bool do_ground_shot, _Bool do_jump_shot, _Bool do_double_jump_shot, _Bool do_aerial_shot, double *time_remaining, double *ball_radius, double *boost_accel, Vector *gravity, Ball *ball_slice, Car *me)
{
	Shot r = default_generic_shot;

	Vector car_to_ball = sub(ball_slice->location, me->location);
	Vector direction = normalize(car_to_ball);
	Vector ball_offset = get_ball_offset(ball_slice, &direction, ball_radius);

	if ((do_ground_shot || do_jump_shot || do_double_jump_shot) && in_2d_field(&ball_offset, &me->hitbox))
	{
        double distance_remaining = flat_dist(ball_offset, me->location) - (me->hitbox.length * 0.45);
        double dodge_distance_remaining = distance_remaining - (me->hitbox.length * 0.5);
        Vector offset_direction = normalize(sub(ball_offset, me->location));

		if (do_ground_shot)
		{
            r.found = ground_shot_is_viable(time_remaining, boost_accel, me, ball_offset.z, &offset_direction, &dodge_distance_remaining, max_shot_0_slope);
        	r.shot_type = GROUND_SHOT;
		}

		if (do_jump_shot && !r.found)
		{
            r.found = jump_shot_is_viable(time_remaining, boost_accel, gravity, me, ball_offset.z, &offset_direction, &dodge_distance_remaining, max_shot_0_slope);
        	r.shot_type = JUMP_SHOT;
		}

		if (do_double_jump_shot && !r.found)
		{
            r.found = double_jump_shot_is_viable(time_remaining, boost_accel, gravity, me, ball_offset.z, &offset_direction, &distance_remaining, max_shot_0_slope);
        	r.shot_type = DOUBLE_JUMP_SHOT;
		}
	}

	if (do_aerial_shot && !r.found && in_field(&ball_offset, &me->hitbox))
	{
	    r.found = aerial_shot_is_viable(*time_remaining, *boost_accel, *gravity, me, ball_offset, &r.fast, 1);
    	r.shot_type = AERIAL_SHOT;
	}

	return r;
}

// Linking the C functions to Python methods

static PyObject *method_ground_shot_is_viable(PyObject *self, PyObject *args)
{
    double T, boost_accel, offset_target_z, distance_remaining;
    Vector direction;
    Car me;
    _Bool shot_viable = 0;

    // args are for >= 1.11
    if (!PyArg_ParseTuple(args, "dd((ddd)(ddd)((ddd)(ddd)(ddd))(ddd)bbbbbbb(ddd)(ddd))d(ddd)d", &T, &boost_accel, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.orientation.left.x, &me.orientation.left.y, &me.orientation.left.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.angular_velocity.x, &me.angular_velocity.y, &me.angular_velocity.z, &me.demolished, &me.airborne, &me.supersonic, &me.jumped, &me.doublejumped, &me.boost, &me.index, &me.hitbox.length, &me.hitbox.width, &me.hitbox.height, &me.hitbox.offset.x, &me.hitbox.offset.y, &me.hitbox.offset.z, &offset_target_z, &direction.x, &direction.y, &direction.z, &distance_remaining))
    {
        PyErr_Clear();
		Vector car_forward;
        HitBox hitbox;
        double car_speed;
		int car_boost;

    	// legacy args & method are for < 1.10
		if (!PyArg_ParseTuple(args, "ddd(ddd)(ddd)(ddd)dd", &T, &boost_accel, &distance_remaining, &direction.x, &direction.y, &direction.z, &car_forward.x, &car_forward.y, &car_forward.z, &hitbox.length, &hitbox.width, &hitbox.height, &car_boost, &car_speed))
	        return NULL;

        unsigned char boost = (car_boost <= 100) ? (unsigned char)car_boost : 255;
        double car_z = 17;
	    shot_viable = legacy_ground_shot_is_viable(&T, &hitbox, &boost_accel, &car_z, &distance_remaining, &direction, &car_forward, &boost, &car_speed, max_shot_0_slope);
    }
    else
    {
        shot_viable = ground_shot_is_viable(&T, &boost_accel, &me, offset_target_z, &direction, &distance_remaining, max_shot_0_slope);
    }

    if (shot_viable)
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
}

static PyObject *method_parse_slice_for_ground_shot_with_target(PyObject *self, PyObject *args)
{
    double T, boost_accel, ball_radius;
    Target targets;
    Ball ball_slice;
    Car me;
    Shot shot_viable;

    // args are for >= 1.11
    if (!PyArg_ParseTuple(args, "ddd((ddd)(ddd))((ddd)(ddd)((ddd)(ddd)(ddd))(ddd)bbbbbbb(ddd)(ddd))((ddd)(ddd))", &T, &boost_accel, &ball_radius, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &ball_slice.velocity.x, &ball_slice.velocity.y, &ball_slice.velocity.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.orientation.left.x, &me.orientation.left.y, &me.orientation.left.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.angular_velocity.x, &me.angular_velocity.y, &me.angular_velocity.z, &me.demolished, &me.airborne, &me.supersonic, &me.jumped, &me.doublejumped, &me.boost, &me.index, &me.hitbox.length, &me.hitbox.width, &me.hitbox.height, &me.hitbox.offset.x, &me.hitbox.offset.y, &me.hitbox.offset.z, &targets.left.x, &targets.left.y, &targets.left.z, &targets.right.x, &targets.right.y, &targets.right.z))
    {
        int car_boost;
    	PyErr_Clear();

    	// legacy args & method are for < 1.11
    	if (!PyArg_ParseTuple(args, "ddd(ddd)((ddd)(ddd)(ddd)(ddd)(ddd)ii)(ddd)(ddd)", &T, &ball_radius, &boost_accel, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.hitbox.length, &me.hitbox.width, &me.hitbox.height, &me.airborne, &car_boost, &targets.left.x, &targets.left.y, &targets.left.z, &targets.right.x, &targets.right.y, &targets.right.z))
	        return NULL;

        me.boost = (car_boost <= 100) ? car_boost : 255;
		shot_viable = legacy_parse_slice_for_ground_shot_with_target(&T, &ball_radius, &boost_accel, &ball_slice, &me, &targets);
    }
	else
	{
    	shot_viable = parse_slice_for_shot_with_target(1, 0, 0, 0, &T, &ball_radius, &boost_accel, &legacy_default_gravity_vector, &ball_slice, &me, &targets);
	}

    return Py_BuildValue("{s:i,s:((ddd)(ddd))}", "found", shot_viable.found, "targets", shot_viable.targets.left.x, shot_viable.targets.left.y, shot_viable.targets.left.z, shot_viable.targets.right.x, shot_viable.targets.right.y, shot_viable.targets.right.z);
}

static PyObject *method_parse_slice_for_ground_shot(PyObject *self, PyObject *args)
{
    double T, boost_accel, ball_radius;
    Ball ball_slice;
    Car me;
    _Bool shot_viable = 0;

    // args are for >= 1.11
    if (!PyArg_ParseTuple(args, "ddd((ddd)(ddd))((ddd)(ddd)((ddd)(ddd)(ddd))(ddd)bbbbbbb(ddd)(ddd))", &T, &boost_accel, &ball_radius, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &ball_slice.velocity.x, &ball_slice.velocity.y, &ball_slice.velocity.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.orientation.left.x, &me.orientation.left.y, &me.orientation.left.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.angular_velocity.x, &me.angular_velocity.y, &me.angular_velocity.z, &me.demolished, &me.airborne, &me.supersonic, &me.jumped, &me.doublejumped, &me.boost, &me.index, &me.hitbox.length, &me.hitbox.width, &me.hitbox.height, &me.hitbox.offset.x, &me.hitbox.offset.y, &me.hitbox.offset.z))
    {
        int car_boost;
        PyErr_Clear();

        // legacy args & method are for < 1.11
        if (!PyArg_ParseTuple(args, "ddd(ddd)((ddd)(ddd)(ddd)(ddd)(ddd)ii)", &T, &ball_radius, &boost_accel, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.hitbox.length, &me.hitbox.width, &me.hitbox.height, &me.airborne, &car_boost))
            return NULL;

        me.boost = (car_boost <= 100) ? car_boost : 255;
        shot_viable = legacy_parse_slice_for_ground_shot(&T, &ball_radius, &boost_accel, &ball_slice, &me);
    }
    else
    {
        shot_viable = parse_slice_for_shot(1, 0, 0, 0, &T, &ball_radius, &boost_accel, &legacy_default_gravity_vector, &ball_slice, &me).found;
    }

    return Py_BuildValue("{s:i}", "found", shot_viable);
}

static PyObject *method_jump_shot_is_viable(PyObject *self, PyObject *args)
{
    double T, boost_accel, offset_target_z, distance_remaining;
    Vector gravity, direction;
    Car me;
    _Bool shot_viable = 0;

    // args are for >= 1.11
    if (!PyArg_ParseTuple(args, "dd(ddd)((ddd)(ddd)((ddd)(ddd)(ddd))(ddd)bbbbbbb(ddd)(ddd))d(ddd)d", &T, &boost_accel, &gravity.x, &gravity.y, &gravity.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.orientation.left.x, &me.orientation.left.y, &me.orientation.left.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.angular_velocity.x, &me.angular_velocity.y, &me.angular_velocity.z, &me.demolished, &me.airborne, &me.supersonic, &me.jumped, &me.doublejumped, &me.boost, &me.index, &me.hitbox.length, &me.hitbox.width, &me.hitbox.height, &me.hitbox.offset.x, &me.hitbox.offset.y, &me.hitbox.offset.z, &offset_target_z, &direction.x, &direction.y, &direction.z, &distance_remaining))
    {
        int car_boost;
        PyErr_Clear();

        // legacy args & method are for < 1.11
        if (!PyArg_ParseTuple(args, "ddd(ddd)(ddd)id", &T, &boost_accel, &distance_remaining, &direction.x, &direction.y, &direction.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &car_boost, &me.velocity.x))
            return NULL;

        unsigned char boost = (car_boost <= 100) ? car_boost : 255;
        shot_viable = legacy_jump_shot_is_viable(&T, &boost_accel, &distance_remaining, &direction, &me.orientation.forward, &boost, &me.velocity.x, max_shot_0_slope);
    }
    else
    {
        shot_viable = jump_shot_is_viable(&T, &boost_accel, &gravity, &me, offset_target_z, &direction, &distance_remaining, max_shot_0_slope);
    }

    if (shot_viable)
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
}

static PyObject *method_parse_slice_for_jump_shot_with_target(PyObject *self, PyObject *args)
{
    double T, boost_accel, ball_radius;
    Vector gravity;
    Target targets;
    Ball ball_slice;
    Car me;

    // args are for >= 1.11
    if (!PyArg_ParseTuple(args, "ddd(ddd)((ddd)(ddd))((ddd)(ddd)((ddd)(ddd)(ddd))(ddd)bbbbbbb(ddd)(ddd))((ddd)(ddd))", &T, &boost_accel, &ball_radius, &gravity.x, &gravity.y, &gravity.z, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &ball_slice.velocity.x, &ball_slice.velocity.y, &ball_slice.velocity.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.orientation.left.x, &me.orientation.left.y, &me.orientation.left.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.angular_velocity.x, &me.angular_velocity.y, &me.angular_velocity.z, &me.demolished, &me.airborne, &me.supersonic, &me.jumped, &me.doublejumped, &me.boost, &me.index, &me.hitbox.length, &me.hitbox.width, &me.hitbox.height, &me.hitbox.offset.x, &me.hitbox.offset.y, &me.hitbox.offset.z, &targets.left.x, &targets.left.y, &targets.left.z, &targets.right.x, &targets.right.y, &targets.right.z))
    {
        int car_boost;
        PyErr_Clear();

        // args are for >=1.8
        if (!PyArg_ParseTuple(args, "ddd(ddd)(ddd)(ddd)id(ddd)(ddd)", &T, &ball_radius, &boost_accel, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &me.location.x, &me.location.y, &me.location.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &car_boost, &me.velocity.x, &targets.left.x, &targets.left.y, &targets.left.z, &targets.right.x, &targets.right.y, &targets.right.z))
        {
            double cap_;
            PyErr_Clear();
            // old legacy args are for <1.8 and >=1.7
            // cap_ is no longer needed, but some instances still pass it in as an argument; this is why it's optional
            if (!PyArg_ParseTuple(args, "dd(ddd)(ddd)(ddd)i(ddd)(ddd)d", &T, &ball_radius, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &me.location.x, &me.location.y, &me.location.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &car_boost, &targets.left.x, &targets.left.y, &targets.left.z, &targets.right.x, &targets.right.y, &targets.right.z, &cap_))
                return NULL;

            boost_accel = 991. + (2. / 3.);
            me.velocity.x = 0;
        }

        me.boost = (car_boost <= 100) ? car_boost : 255;
        LegacyJumpShot shot_viable = legacy_parse_slice_for_jump_shot_with_target(&T, &ball_radius, &boost_accel, &me, &ball_slice, &targets);

        return Py_BuildValue("{s:i,s:((ddd)(ddd)),s:(ddd)}", "found", shot_viable.found, "targets", shot_viable.targets.left.x, shot_viable.targets.left.y, shot_viable.targets.left.z, shot_viable.targets.right.x, shot_viable.targets.right.y, shot_viable.targets.right.z, "best_shot_vector", shot_viable.best_shot_vector.x, shot_viable.best_shot_vector.y, shot_viable.best_shot_vector.z);
    }

    Shot shot_viable = parse_slice_for_shot_with_target(0, 1, 0, 0, &T, &ball_radius, &boost_accel, &gravity, &ball_slice, &me, &targets);

    return Py_BuildValue("{s:i,s:((ddd)(ddd))}", "found", shot_viable.found, "targets", shot_viable.targets.left.x, shot_viable.targets.left.y, shot_viable.targets.left.z, shot_viable.targets.right.x, shot_viable.targets.right.y, shot_viable.targets.right.z);
}

static PyObject *method_parse_slice_for_jump_shot(PyObject *self, PyObject *args)
{
    double T, boost_accel, ball_radius;
    Vector gravity;
    Ball ball_slice;
    Car me;

    // args are for >= 1.11
    if (!PyArg_ParseTuple(args, "ddd(ddd)((ddd)(ddd))((ddd)(ddd)((ddd)(ddd)(ddd))(ddd)bbbbbbb(ddd)(ddd))", &T, &boost_accel, &ball_radius, &gravity.x, &gravity.y, &gravity.z, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &ball_slice.velocity.x, &ball_slice.velocity.y, &ball_slice.velocity.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.orientation.left.x, &me.orientation.left.y, &me.orientation.left.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.angular_velocity.x, &me.angular_velocity.y, &me.angular_velocity.z, &me.demolished, &me.airborne, &me.supersonic, &me.jumped, &me.doublejumped, &me.boost, &me.index, &me.hitbox.length, &me.hitbox.width, &me.hitbox.height, &me.hitbox.offset.x, &me.hitbox.offset.y, &me.hitbox.offset.z))
    {
        int car_boost;
        PyErr_Clear();

        // args are for >= 1.8
        if (!PyArg_ParseTuple(args, "ddd(ddd)(ddd)(ddd)id", &T, &ball_radius, &boost_accel, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &me.location.x, &me.location.y, &me.location.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &car_boost, &me.velocity.x))
        {
            double cap_;
            PyErr_Clear();

            // old legacy args are for <1.8 and >=1.7
            // cap_ is no longer needed, but some instances still pass it in as an argument; this is why it's optional
            if (!PyArg_ParseTuple(args, "dd(ddd)(ddd)(ddd)i|d", &T, &ball_radius, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &me.location.x, &me.location.y, &me.location.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &car_boost, &cap_))
                return NULL;

            boost_accel = 991. + (2. / 3.);
            me.velocity.x = 0;
        }

        me.boost = (car_boost <= 100) ? car_boost : 255;
        LegacyJumpShot shot_viable = legacy_parse_slice_for_jump_shot(&T, &ball_radius, &boost_accel, &ball_slice, &me);

        return Py_BuildValue("{s:i,s:(ddd)}", "found", shot_viable.found, "best_shot_vector", shot_viable.best_shot_vector.x, shot_viable.best_shot_vector.y, shot_viable.best_shot_vector.z);
    }

    _Bool shot_viable = parse_slice_for_shot(0, 1, 0, 0, &T, &ball_radius, &boost_accel, &gravity, &ball_slice, &me).found;

    return Py_BuildValue("{s:i}", "found", shot_viable);
}

static PyObject *method_double_jump_shot_is_viable(PyObject *self, PyObject *args)
{
    double T, boost_accel, offset_target_z, distance_remaining;
    Vector gravity, direction;
    Car me;
    _Bool shot_viable = 0;

    // args are for >= 1.11
    if (!PyArg_ParseTuple(args, "dd(ddd)((ddd)(ddd)((ddd)(ddd)(ddd))(ddd)bbbbbbb(ddd)(ddd))d(ddd)d", &T, &boost_accel, &gravity.x, &gravity.y, &gravity.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.orientation.left.x, &me.orientation.left.y, &me.orientation.left.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.angular_velocity.x, &me.angular_velocity.y, &me.angular_velocity.z, &me.demolished, &me.airborne, &me.supersonic, &me.jumped, &me.doublejumped, &me.boost, &me.index, &me.hitbox.length, &me.hitbox.width, &me.hitbox.height, &me.hitbox.offset.x, &me.hitbox.offset.y, &me.hitbox.offset.z, &offset_target_z, &direction.x, &direction.y, &direction.z, &distance_remaining))
    {
        int car_boost;
        PyErr_Clear();

        // legacy args & method are for < 1.11
        if (!PyArg_ParseTuple(args, "ddd(ddd)(ddd)id", &T, &boost_accel, &distance_remaining, &direction.x, &direction.y, &direction.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &car_boost, &me.velocity.x))
            return NULL;

        unsigned char boost = (car_boost <= 100) ? car_boost : 255;
        shot_viable = legacy_double_jump_shot_is_viable(&T, &boost_accel, &distance_remaining, &direction, &me.orientation.forward, &boost, &me.velocity.x, max_shot_0_slope);
    }
    else
    {
        shot_viable = double_jump_shot_is_viable(&T, &boost_accel, &gravity, &me, offset_target_z, &direction, &distance_remaining, max_shot_0_slope);
    }

    if (shot_viable)
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
}

static PyObject *method_parse_slice_for_double_jump_shot_with_target(PyObject *self, PyObject *args)
{
    double T, boost_accel, ball_radius;
    Vector gravity;
    Target targets;
    Ball ball_slice;
    Car me;

    // args are for >= 1.11
    if (!PyArg_ParseTuple(args, "ddd(ddd)((ddd)(ddd))((ddd)(ddd)((ddd)(ddd)(ddd))(ddd)bbbbbbb(ddd)(ddd))((ddd)(ddd))", &T, &boost_accel, &ball_radius, &gravity.x, &gravity.y, &gravity.z, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &ball_slice.velocity.x, &ball_slice.velocity.y, &ball_slice.velocity.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.orientation.left.x, &me.orientation.left.y, &me.orientation.left.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.angular_velocity.x, &me.angular_velocity.y, &me.angular_velocity.z, &me.demolished, &me.airborne, &me.supersonic, &me.jumped, &me.doublejumped, &me.boost, &me.index, &me.hitbox.length, &me.hitbox.width, &me.hitbox.height, &me.hitbox.offset.x, &me.hitbox.offset.y, &me.hitbox.offset.z, &targets.left.x, &targets.left.y, &targets.left.z, &targets.right.x, &targets.right.y, &targets.right.z))
    {
        int car_boost;
        PyErr_Clear();

        // legacy args are for < 1.11 and >= 1.8
        // legacy method is for < 1.11
        if (!PyArg_ParseTuple(args, "ddd(ddd)(ddd)(ddd)id(ddd)(ddd)", &T, &ball_radius, &boost_accel, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &me.location.x, &me.location.y, &me.location.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &car_boost, &me.velocity.x, &targets.left.x, &targets.left.y, &targets.left.z, &targets.right.x, &targets.right.y, &targets.right.z))
        {
            double cap_;
            PyErr_Clear();
            // old legacy args are for < 1.8 and >= 1.7
            // cap_ is no longer needed, but some instances still pass it in as an argument; this is why it's optional
            if (!PyArg_ParseTuple(args, "dd(ddd)(ddd)(ddd)i(ddd)(ddd)d", &T, &ball_radius, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &me.location.x, &me.location.y, &me.location.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &car_boost, &targets.left.x, &targets.left.y, &targets.left.z, &targets.right.x, &targets.right.y, &targets.right.z, &cap_))
                return NULL;

            boost_accel = 991. + (2. / 3.);
            me.velocity.x = 0;
        }

        me.boost = (car_boost <= 100) ? car_boost : 255;
        LegacyJumpShot shot_viable = legacy_parse_slice_for_double_jump_shot_with_target(&T, &ball_radius, &boost_accel, &me, &ball_slice, &targets);

        return Py_BuildValue("{s:i,s:((ddd)(ddd)),s:(ddd)}", "found", shot_viable.found, "targets", shot_viable.targets.left.x, shot_viable.targets.left.y, shot_viable.targets.left.z, shot_viable.targets.right.x, shot_viable.targets.right.y, shot_viable.targets.right.z, "best_shot_vector", shot_viable.best_shot_vector.x, shot_viable.best_shot_vector.y, shot_viable.best_shot_vector.z);
    }

    Shot shot_viable = parse_slice_for_shot_with_target(0, 0, 1, 0, &T, &ball_radius, &boost_accel, &gravity, &ball_slice, &me, &targets);

    return Py_BuildValue("{s:i,s:((ddd)(ddd))}", "found", shot_viable.found, "targets", shot_viable.targets.left.x, shot_viable.targets.left.y, shot_viable.targets.left.z, shot_viable.targets.right.x, shot_viable.targets.right.y, shot_viable.targets.right.z);
}

static PyObject *method_parse_slice_for_double_jump_shot(PyObject *self, PyObject *args)
{
    double T, boost_accel, ball_radius;
    Vector gravity;
    Ball ball_slice;
    Car me;

    // args are for >= 1.11
    if (!PyArg_ParseTuple(args, "ddd(ddd)((ddd)(ddd))((ddd)(ddd)((ddd)(ddd)(ddd))(ddd)bbbbbbb(ddd)(ddd))", &T, &boost_accel, &ball_radius, &gravity.x, &gravity.y, &gravity.z, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &ball_slice.velocity.x, &ball_slice.velocity.y, &ball_slice.velocity.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.orientation.left.x, &me.orientation.left.y, &me.orientation.left.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.angular_velocity.x, &me.angular_velocity.y, &me.angular_velocity.z, &me.demolished, &me.airborne, &me.supersonic, &me.jumped, &me.doublejumped, &me.boost, &me.index, &me.hitbox.length, &me.hitbox.width, &me.hitbox.height, &me.hitbox.offset.x, &me.hitbox.offset.y, &me.hitbox.offset.z))
    {
        int car_boost;
        PyErr_Clear();

        // legacy args are for < 1.11 and >= 1.8
        // legacy method is for < 1.11
        if (!PyArg_ParseTuple(args, "ddd(ddd)(ddd)(ddd)id", &T, &ball_radius, &boost_accel, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &me.location.x, &me.location.y, &me.location.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &car_boost, &me.velocity.x))
        {
            double cap_;
            PyErr_Clear();

            // old legacy args are for <1.8 and >=1.7
            // cap_ is no longer needed, but some instances still pass it in as an argument; this is why it's optional
            if (!PyArg_ParseTuple(args, "dd(ddd)(ddd)(ddd)i|d", &T, &ball_radius, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &me.location.x, &me.location.y, &me.location.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &car_boost, &cap_))
                return NULL;

            boost_accel = 991. + (2. / 3.);
            me.velocity.x = 0;
        }

        me.boost = (car_boost <= 100) ? car_boost : 255;
        LegacyJumpShot shot_viable = legacy_parse_slice_for_double_jump_shot(&T, &ball_radius, &boost_accel, &ball_slice, &me);

        return Py_BuildValue("{s:i,s:(ddd)}", "found", shot_viable.found, "best_shot_vector", shot_viable.best_shot_vector.x, shot_viable.best_shot_vector.y, shot_viable.best_shot_vector.z);
    }

    _Bool shot_viable = parse_slice_for_shot(0, 0, 1, 0, &T, &ball_radius, &boost_accel, &gravity, &ball_slice, &me).found;

    return Py_BuildValue("{s:i}", "found", shot_viable);
}

static PyObject *method_aerial_shot_is_viable(PyObject *self, PyObject *args)
{
    _Bool fast = 0;
    double T, boost_accel;
    Vector gravity, target_;
    Car me;

    // args are for >= 1.11
    if (!PyArg_ParseTuple(args, "dd(ddd)((ddd)(ddd)((ddd)(ddd)(ddd))(ddd)bbbbbbb(ddd)(ddd))(ddd)", &T, &boost_accel, &gravity.x, &gravity.y, &gravity.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.orientation.left.x, &me.orientation.left.y, &me.orientation.left.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.angular_velocity.x, &me.angular_velocity.y, &me.angular_velocity.z, &me.demolished, &me.airborne, &me.supersonic, &me.jumped, &me.doublejumped, &me.boost, &me.index, &me.hitbox.length, &me.hitbox.width, &me.hitbox.height, &me.hitbox.offset.x, &me.hitbox.offset.y, &me.hitbox.offset.z, &target_.x, &target_.y, &target_.z))
    {
        PyErr_Clear();

        // legacy args are for < 1.11
        if (!PyArg_ParseTuple(args, "ddd(ddd)(ddd)(ddd)(ddd)(ddd)ii(ddd)", &T, &me.hitbox.height, &boost_accel, &gravity.x, &gravity.y, &gravity.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.airborne, &me.boost, &target_.x, &target_.y, &target_.z))
            return NULL;

        me.hitbox.length = 118.01;
        me.hitbox.width = 76.71;
    }

    _Bool shot_viable = aerial_shot_is_viable(T, boost_accel, gravity, &me, target_, &fast, 0);

    if (shot_viable)
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
}

static PyObject *method_parse_slice_for_aerial_shot_with_target(PyObject *self, PyObject *args)
{
    double T, boost_accel, ball_radius;
    Vector gravity;
    Target targets;
    Ball ball_slice;
    Car me;

    // args are for >= 1.11
    if (!PyArg_ParseTuple(args, "ddd(ddd)((ddd)(ddd))((ddd)(ddd)((ddd)(ddd)(ddd))(ddd)bbbbbbb(ddd)(ddd))((ddd)(ddd))", &T, &boost_accel, &ball_radius, &gravity.x, &gravity.y, &gravity.z, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &ball_slice.velocity.x, &ball_slice.velocity.y, &ball_slice.velocity.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.orientation.left.x, &me.orientation.left.y, &me.orientation.left.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.angular_velocity.x, &me.angular_velocity.y, &me.angular_velocity.z, &me.demolished, &me.airborne, &me.supersonic, &me.jumped, &me.doublejumped, &me.boost, &me.index, &me.hitbox.length, &me.hitbox.width, &me.hitbox.height, &me.hitbox.offset.x, &me.hitbox.offset.y, &me.hitbox.offset.z, &targets.left.x, &targets.left.y, &targets.left.z, &targets.right.x, &targets.right.y, &targets.right.z))
    {
        PyErr_Clear();

        // legacy args and method are for < 1.11
        if (!PyArg_ParseTuple(args, "ddd(ddd)(ddd)((ddd)(ddd)(ddd)(ddd)(ddd)ii)(ddd)(ddd)", &T, &ball_radius, &boost_accel, &gravity.x, &gravity.y, &gravity.z, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.orientation.left.x, &me.orientation.left.y, &me.orientation.left.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.hitbox.length, &me.hitbox.width, &me.hitbox.height, &me.airborne, &me.boost, &targets.left.x, &targets.left.y, &targets.left.z, &targets.right.x, &targets.right.y, &targets.right.z))
        {
            double cap_;
            PyErr_Clear();

            // old legacy args are for < 1.10
            // cap_ is no longer needed, but a lot of instances still pass it in as an argument; this is why it's optional
            if (!PyArg_ParseTuple(args, "ddd(ddd)(ddd)((ddd)(ddd)(ddd)(ddd)ii)(ddd)(ddd)|d", &T, &ball_radius, &boost_accel, &gravity.x, &gravity.y, &gravity.z, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.orientation.left.x, &me.orientation.left.y, &me.orientation.left.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.airborne, &me.boost, &targets.left.x, &targets.left.y, &targets.left.z, &targets.right.x, &targets.right.y, &targets.right.z, &cap_))
                return NULL;

            me.hitbox.length = 118.01;
            me.hitbox.width = 76.71;
            me.hitbox.height = 30.3;
        }

        LegacyAerialShot shot_viable = legacy_parse_slice_for_aerial_shot_with_target(&T, &ball_radius, &boost_accel, &gravity, &ball_slice, &me, &targets);

        return Py_BuildValue("{s:i,s:(ddd),s:(ddd),s:((ddd)(ddd)),s:i}", "found", shot_viable.found, "ball_intercept", shot_viable.ball_intercept.x, shot_viable.ball_intercept.y, shot_viable.ball_intercept.z, "best_shot_vector", shot_viable.best_shot_vector.x, shot_viable.best_shot_vector.y, shot_viable.best_shot_vector.z, "targets", shot_viable.targets.left.x, shot_viable.targets.left.y, shot_viable.targets.left.z, shot_viable.targets.right.x, shot_viable.targets.right.y, shot_viable.targets.right.z, "fast", shot_viable.fast);
    }

    Shot shot_viable = parse_slice_for_shot_with_target(0, 0, 0, 1, &T, &ball_radius, &boost_accel, &gravity, &ball_slice, &me, &targets);

    return Py_BuildValue("{s:i,s:i,s:((ddd)(ddd))}", "found", shot_viable.found, "fast", shot_viable.fast, "targets", shot_viable.targets.left.x, shot_viable.targets.left.y, shot_viable.targets.left.z, shot_viable.targets.right.x, shot_viable.targets.right.y, shot_viable.targets.right.z);
}

static PyObject *method_parse_slice_for_aerial_shot(PyObject *self, PyObject *args)
{
    double T, boost_accel, ball_radius;
    Vector gravity;
    Ball ball_slice;
    Car me;

    // args are for >= 1.11
    if (!PyArg_ParseTuple(args, "ddd(ddd)((ddd)(ddd))((ddd)(ddd)((ddd)(ddd)(ddd))(ddd)bbbbbbb(ddd)(ddd))", &T, &boost_accel, &ball_radius, &gravity.x, &gravity.y, &gravity.z, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &ball_slice.velocity.x, &ball_slice.velocity.y, &ball_slice.velocity.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.orientation.left.x, &me.orientation.left.y, &me.orientation.left.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.angular_velocity.x, &me.angular_velocity.y, &me.angular_velocity.z, &me.demolished, &me.airborne, &me.supersonic, &me.jumped, &me.doublejumped, &me.boost, &me.index, &me.hitbox.length, &me.hitbox.width, &me.hitbox.height, &me.hitbox.offset.x, &me.hitbox.offset.y, &me.hitbox.offset.z))
    {
        PyErr_Clear();

        // legacy args and method are for < 1.11
        if (!PyArg_ParseTuple(args, "ddd(ddd)(ddd)((ddd)(ddd)(ddd)(ddd)(ddd)ii)", &T, &ball_radius, &boost_accel, &gravity.x, &gravity.y, &gravity.z, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.orientation.left.x, &me.orientation.left.y, &me.orientation.left.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.hitbox.length, &me.hitbox.width, &me.hitbox.height, &me.airborne, &me.boost))
        {
            double cap_;
            PyErr_Clear();

            // old legacy args are for < 1.10
            // cap_ is no longer needed, but a lot of instances still pass it in as an argument; this is why it's optional
            if (!PyArg_ParseTuple(args, "ddd(ddd)(ddd)((ddd)(ddd)(ddd)(ddd)ii)|d", &T, &ball_radius, &boost_accel, &gravity.x, &gravity.y, &gravity.z, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.orientation.left.x, &me.orientation.left.y, &me.orientation.left.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.airborne, &me.boost, &cap_))
                return NULL;

            me.hitbox.length = 118.01;
            me.hitbox.width = 76.71;
            me.hitbox.height = 30.3;
        }

        LegacyAerialShot shot_viable = legacy_parse_slice_for_aerial_shot(&T, &ball_radius, &boost_accel, &gravity, &ball_slice, &me);

        return Py_BuildValue("{s:i,s:(ddd),s:(ddd),s:((ddd)(ddd)),s:i}", "found", shot_viable.found, "ball_intercept", shot_viable.ball_intercept.x, shot_viable.ball_intercept.y, shot_viable.ball_intercept.z, "best_shot_vector", shot_viable.best_shot_vector.x, shot_viable.best_shot_vector.y, shot_viable.best_shot_vector.z, "targets", shot_viable.targets.left.x, shot_viable.targets.left.y, shot_viable.targets.left.z, shot_viable.targets.right.x, shot_viable.targets.right.y, shot_viable.targets.right.z, "fast", shot_viable.fast);
    }

    Shot shot_viable = parse_slice_for_shot(0, 0, 0, 1, &T, &ball_radius, &boost_accel, &gravity, &ball_slice, &me);

    return Py_BuildValue("{s:i,s:i}", "found", shot_viable.found, "fast", shot_viable.fast);
}

static PyObject *method_parse_slice_for_shot_with_target(PyObject *self, PyObject *args)
{
	_Bool do_ground_shot, do_jump_shot, do_double_jump_shot, do_aerial_shot;
    double T, boost_accel, ball_radius;
    Vector gravity;
    Target targets;
    Ball ball_slice;
    Car me;
    Shot shot_viable;

    // args are for >= 1.12
    if (!PyArg_ParseTuple(args, "bbbbddd(ddd)((ddd)(ddd))((ddd)(ddd)((ddd)(ddd)(ddd))(ddd)bbbbbbb(ddd)(ddd))((ddd)(ddd))", &do_ground_shot, &do_jump_shot, &do_double_jump_shot, &do_aerial_shot, &T, &boost_accel, &ball_radius, &gravity.x, &gravity.y, &gravity.z, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &ball_slice.velocity.x, &ball_slice.velocity.y, &ball_slice.velocity.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.orientation.left.x, &me.orientation.left.y, &me.orientation.left.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.angular_velocity.x, &me.angular_velocity.y, &me.angular_velocity.z, &me.demolished, &me.airborne, &me.supersonic, &me.jumped, &me.doublejumped, &me.boost, &me.index, &me.hitbox.length, &me.hitbox.width, &me.hitbox.height, &me.hitbox.offset.x, &me.hitbox.offset.y, &me.hitbox.offset.z, &targets.left.x, &targets.left.y, &targets.left.z, &targets.right.x, &targets.right.y, &targets.right.z))
        return NULL;

	shot_viable = parse_slice_for_shot_with_target(do_ground_shot, do_jump_shot, do_double_jump_shot, do_aerial_shot, &T, &ball_radius, &boost_accel, &gravity, &ball_slice, &me, &targets);

    return Py_BuildValue("{s:i,s:i,s:i,s:((ddd)(ddd))}", "found", shot_viable.found, "fast", shot_viable.fast, "shot_type", shot_viable.shot_type, "targets", shot_viable.targets.left.x, shot_viable.targets.left.y, shot_viable.targets.left.z, shot_viable.targets.right.x, shot_viable.targets.right.y, shot_viable.targets.right.z);
}

static PyObject *method_parse_slice_for_shot(PyObject *self, PyObject *args)
{
	_Bool do_ground_shot, do_jump_shot, do_double_jump_shot, do_aerial_shot;
    double T, boost_accel, ball_radius;
    Vector gravity;
    Ball ball_slice;
    Car me;
    Shot shot_viable;

    // args are for >= 1.12
    if (!PyArg_ParseTuple(args, "bbbbddd(ddd)((ddd)(ddd))((ddd)(ddd)((ddd)(ddd)(ddd))(ddd)bbbbbbb(ddd)(ddd))", &do_ground_shot, &do_jump_shot, &do_double_jump_shot, &do_aerial_shot, &T, &boost_accel, &ball_radius, &gravity.x, &gravity.y, &gravity.z, &ball_slice.location.x, &ball_slice.location.y, &ball_slice.location.z, &ball_slice.velocity.x, &ball_slice.velocity.y, &ball_slice.velocity.z, &me.location.x, &me.location.y, &me.location.z, &me.velocity.x, &me.velocity.y, &me.velocity.z, &me.orientation.forward.x, &me.orientation.forward.y, &me.orientation.forward.z, &me.orientation.left.x, &me.orientation.left.y, &me.orientation.left.z, &me.orientation.up.x, &me.orientation.up.y, &me.orientation.up.z, &me.angular_velocity.x, &me.angular_velocity.y, &me.angular_velocity.z, &me.demolished, &me.airborne, &me.supersonic, &me.jumped, &me.doublejumped, &me.boost, &me.index, &me.hitbox.length, &me.hitbox.width, &me.hitbox.height, &me.hitbox.offset.x, &me.hitbox.offset.y, &me.hitbox.offset.z))
        return NULL;

	shot_viable = parse_slice_for_shot(do_ground_shot, do_jump_shot, do_double_jump_shot, do_aerial_shot, &T, &ball_radius, &boost_accel, &gravity, &ball_slice, &me);

    return Py_BuildValue("{s:i,s:i,s:i}", "found", shot_viable.found, "fast", shot_viable.fast, "shot_type", shot_viable.shot_type);
}

static PyObject *method_find_landing_plane(PyObject *self, PyObject *args)
{
    Vector car_location, car_velocity;
    double gravity;

    // args are for all versions, so far
    if (!PyArg_ParseTuple(args, "(ddd)(ddd)d", &car_location.x, &car_location.y, &car_location.z, &car_velocity.x, &car_velocity.y, &car_velocity.z, &gravity))
        return NULL;

    int landing_plane = find_landing_plane(car_location, car_velocity, gravity);

    return Py_BuildValue("i", landing_plane);
}

static PyObject *method_get_jump_time(PyObject *self, PyObject *args)
{
    double car_to_target_z, car_z_velocity, gravity_z;

    // args are for all versions, so far
    if (!PyArg_ParseTuple(args, "ddd", &car_to_target_z, &car_z_velocity, &gravity_z))
        return NULL;

    JumpTime time = get_jump_time(car_to_target_z, car_z_velocity, gravity_z);

    return Py_BuildValue("d", time.time);
}

static PyObject *method_get_double_jump_time(PyObject *self, PyObject *args)
{
    double car_to_target_z, car_z_velocity, gravity_z;

    // args are for all versions, so far
    if (!PyArg_ParseTuple(args, "ddd", &car_to_target_z, &car_z_velocity, &gravity_z))
        return NULL;

    JumpTime time = get_double_jump_time(car_to_target_z, car_z_velocity, gravity_z);

    return Py_BuildValue("d", time.time);
}

static PyObject *method_time_to_speed(PyObject *self, PyObject *args)
{
    double boost_accel, velocity, boost, target_speed;

    // args are for all versions, so far
    if (!PyArg_ParseTuple(args, "dddd", &boost_accel, &velocity, &boost, &target_speed))
        return NULL;

    double time = time_to_speed(boost_accel, velocity, (unsigned char)boost, target_speed);

    return Py_BuildValue("d", time);
}

static PyMethodDef methods[] = {
    {"ground_shot_is_viable", method_ground_shot_is_viable, METH_VARARGS, "Check if a ground shot is viable"},
    {"parse_slice_for_ground_shot_with_target", method_parse_slice_for_ground_shot_with_target, METH_VARARGS, "Parse slice for a ground shot with a target"},
    {"parse_slice_for_ground_shot", method_parse_slice_for_ground_shot, METH_VARARGS, "Parse slice for a ground shot"},
    {"jump_shot_is_viable", method_jump_shot_is_viable, METH_VARARGS, "Check if an jump_shot is viable"},
    {"parse_slice_for_jump_shot_with_target", method_parse_slice_for_jump_shot_with_target, METH_VARARGS, "Parse slice for a jump shot with a target"},
    {"parse_slice_for_jump_shot", method_parse_slice_for_jump_shot, METH_VARARGS, "Parse slice for a jump shot"},
    {"double_jump_shot_is_viable", method_double_jump_shot_is_viable, METH_VARARGS, "Check if an double jump is viable"},
    {"parse_slice_for_double_jump_with_target", method_parse_slice_for_double_jump_shot_with_target, METH_VARARGS, "(Legacy) Parse slice for a double jump with a target"},
    {"parse_slice_for_double_jump", method_parse_slice_for_double_jump_shot, METH_VARARGS, "(Legacy) Parse slice for a double jump"},
    {"parse_slice_for_double_jump_shot_with_target", method_parse_slice_for_double_jump_shot_with_target, METH_VARARGS, "Parse slice for a double jump with a target"},
    {"parse_slice_for_double_jump_shot", method_parse_slice_for_double_jump_shot, METH_VARARGS, "Parse slice for a double jump"},
    {"aerial_shot_is_viable", method_aerial_shot_is_viable, METH_VARARGS, "Check if an aerial is viable"},
    {"parse_slice_for_aerial_shot_with_target", method_parse_slice_for_aerial_shot_with_target, METH_VARARGS, "Parse slice for an aerial shot with a target"},
    {"parse_slice_for_aerial_shot", method_parse_slice_for_aerial_shot, METH_VARARGS, "Parse slice for an aerial shot"},
    {"parse_slice_for_shot_with_target", method_parse_slice_for_shot_with_target, METH_VARARGS, "Parse slice for one of the specified shots with a target"},
    {"parse_slice_for_shot", method_parse_slice_for_shot, METH_VARARGS, "Parse slice for one of the specified shots"},
    {"find_landing_plane", method_find_landing_plane, METH_VARARGS, "Find the plane (side wall, back wall, ceiling, or floor) that the car will collide with first"},
    {"get_jump_time", method_get_jump_time, METH_VARARGS, "Get the time required to jump and reach at target height"},
    {"get_double_jump_time", method_get_jump_time, METH_VARARGS, "Get the time required to double jump and reach at target height"},
    {"time_to_speed", method_time_to_speed, METH_VARARGS, "Get the time required to reach some speed"},
    {NULL, NULL, 0, NULL}};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "virxrlcu",
    "C Library for VirxERLU",
    -1,
    methods};

PyMODINIT_FUNC PyInit_virxrlcu(void)
{
    return PyModule_Create(&module);
}