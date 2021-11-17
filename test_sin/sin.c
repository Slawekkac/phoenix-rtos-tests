#include <math.h>

#include "unity_fixture.h"


#ifdef UNITY_INCLUDE_FLOAT
#define UNITY_INCLUDE_FLOAT
#endif

#ifdef UNITY_INCLUDE_DOUBLE
#define UNITY_INCLUDE_DOUBLE
#endif


TEST_GROUP(test_sin);

TEST_SETUP(test_sin)
{
}

TEST_TEAR_DOWN(test_sin)
{
}

TEST(test_sin, sinus_0_pi)
{
    TEST_ASSERT_EQUAL_DOUBLE(0.0, sin(0.0));
}

TEST(test_sin, sinus_1_6_pi)
{
    TEST_ASSERT_EQUAL_DOUBLE(0.5, sin(M_PI / 6.0));
}

TEST(test_sin, sinus_1_4_pi)
{
    TEST_ASSERT_EQUAL_DOUBLE(sqrt(2) / 2, sin(M_PI / 4.0));
}

TEST(test_sin, sinus_1_4_pi_t2)
{
    TEST_ASSERT_EQUAL_DOUBLE(0.70710678118654752440084436210485, sin(M_PI / 4.0));
}


TEST(test_sin, sinus_1_3_pi)
{
    TEST_ASSERT_EQUAL_DOUBLE(sqrt(3) / 2, sin(M_PI / 3.0));
}

TEST(test_sin, sinus_1_3_pi_t2)
{
    TEST_ASSERT_EQUAL_DOUBLE(0.86602540378443864676372317075294, sin(M_PI / 3.0));
}


TEST(test_sin, sinus_1_2_pi)
{
    TEST_ASSERT_EQUAL_DOUBLE(1.0, sin(M_PI / 2.0));
}

/*
Test function sin for radius angle = Pi
Expected value 0.0 but result is 1.2246468e-16
*/
TEST(test_sin, sinus_1_pi)
{
    TEST_ASSERT_EQUAL_DOUBLE(0.0, sin(M_PI));
}

/*
Test function sin for radius angle = 2*Pi
Expected value 0.0 but result is -2.4492936e-16
*/
TEST(test_sin, sinus_2_pi)
{
    TEST_ASSERT_EQUAL_DOUBLE(0.0, sin(2 * M_PI));
}

/*
Test function sin for radius angle = 4*Pi
Expected value 0.0 but result is -4.8985872e-16
*/
TEST(test_sin, sinus_4_pi)
{
    TEST_ASSERT_EQUAL_DOUBLE(0.0, sin(4 * M_PI));
}

/*
Test function sin for radius angle = 8*Pi
Expected value 0.0 but result is -9.79717439e-16
*/
TEST(test_sin, sinus_8_pi)
{
    TEST_ASSERT_EQUAL_DOUBLE(0.0, sin(8 * M_PI));
}

/*
Test function sin for radius angle = 8*Pi
Expected value 0.0 but result is -9.79717439e-16
Check test with delta
*/
TEST(test_sin, sinus_8_pi_delta)
{
    TEST_ASSERT_DOUBLE_WITHIN(-1.0e-15, 0.0, sin(8 * M_PI));
}

/*
Test function sin for radius angle = 16*Pi
Expected value 0.0 but result is -1.95943488e-15
*/
TEST(test_sin, sinus_16_pi)
{
    TEST_ASSERT_EQUAL_DOUBLE(0.0, sin(16 * M_PI));
}

/*
Test function sin for radius angle = 16*Pi
Expected value 0.0 but result is -1.95943488e-15
So delta should be greather than -1.0e-15
Now we check then
Double precision is set to (1e-12)
Change precision to value (1e-15)
*/
TEST(test_sin, sinus_16_pi_delta)
{
    TEST_ASSERT_DOUBLE_WITHIN(-1.0e-15, 0.0, sin(16 * M_PI));
}

/*
Test function sin for radius angle = 64*Pi
Expected value 0.0 but result is 
*/
TEST(test_sin, sinus_64_pi)
{
    TEST_ASSERT_EQUAL_DOUBLE(0.0, sin(64 * M_PI));
}

/*
Test for float
*/

TEST(test_sin, sinus_0_pi_fl)
{
    TEST_ASSERT_EQUAL_FLOAT(0.0, sin(0.0));
}

TEST(test_sin, sinus_1_6_pi_fl)
{
    TEST_ASSERT_EQUAL_FLOAT(0.5, sin(M_PI / 6.0));
}

TEST(test_sin, sinus_1_4_pi_fl)
{
    TEST_ASSERT_EQUAL_FLOAT(sqrt(2) / 2, sin(M_PI / 4.0));
}

TEST(test_sin, sinus_1_3_pi_fl)
{
    TEST_ASSERT_EQUAL_FLOAT(sqrt(3) / 2, sin(M_PI / 3.0));
}

TEST(test_sin, sinus_1_2_pi_fl)
{
    TEST_ASSERT_EQUAL_FLOAT(1.0, sin(M_PI / 2.0));
}

/*
Test function sin for radius angle = Pi
Expected value 0.0 but result is 
*/
TEST(test_sin, sinus_1_pi_fl)
{
    TEST_ASSERT_EQUAL_FLOAT(0.0, sin(M_PI));
}

TEST_GROUP_RUNNER(test_sinus_with_normal_values) 
{
    RUN_TEST_CASE(test_sin, sinus_0_pi);
    RUN_TEST_CASE(test_sin, sinus_1_6_pi);
    RUN_TEST_CASE(test_sin, sinus_1_4_pi);
    RUN_TEST_CASE(test_sin, sinus_1_4_pi_t2);
    RUN_TEST_CASE(test_sin, sinus_1_3_pi);
    RUN_TEST_CASE(test_sin, sinus_1_3_pi_t2);
    RUN_TEST_CASE(test_sin, sinus_1_2_pi);
    RUN_TEST_CASE(test_sin, sinus_1_pi);
    RUN_TEST_CASE(test_sin, sinus_2_pi);
    RUN_TEST_CASE(test_sin, sinus_4_pi);
    RUN_TEST_CASE(test_sin, sinus_8_pi);
    RUN_TEST_CASE(test_sin, sinus_8_pi_delta);
    RUN_TEST_CASE(test_sin, sinus_16_pi);
    RUN_TEST_CASE(test_sin, sinus_16_pi_delta);
    RUN_TEST_CASE(test_sin, sinus_64_pi);
}

TEST_GROUP_RUNNER(test_fl_sinus_with_normal_values) 
{
    RUN_TEST_CASE(test_sin, sinus_0_pi_fl);
    RUN_TEST_CASE(test_sin, sinus_1_6_pi_fl);
    RUN_TEST_CASE(test_sin, sinus_1_4_pi_fl);
    RUN_TEST_CASE(test_sin, sinus_1_3_pi_fl);
    RUN_TEST_CASE(test_sin, sinus_1_2_pi_fl);
    RUN_TEST_CASE(test_sin, sinus_1_pi_fl);
    
}

void runner(void)
{
	RUN_TEST_GROUP(test_sinus_with_normal_values);
    RUN_TEST_GROUP(test_fl_sinus_with_normal_values);
}

int main(int argc, char *argv[])
{
	UnityMain(argc, (const char **)argv, runner);
	return 0;
}
