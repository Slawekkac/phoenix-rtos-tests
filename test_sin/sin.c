#include <math.h>

#include "unity_fixture.h"


#define UNITY_EXCLUDE_FLOAT
#define UNITY_INCLUDE_DOUBLE
#define UNITY_DOUBLE_PRECISION


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

TEST(test_sin, sinus_1_3_pi)
{
    TEST_ASSERT_EQUAL_DOUBLE(sqrt(3) / 2, sin(M_PI / 3.0));
}

TEST(test_sin, sinus_1_2_pi)
{
    TEST_ASSERT_EQUAL_DOUBLE(1.0, sin(M_PI / 2.0));
}

TEST(test_sin, sinus_1_pi)
{
    TEST_ASSERT_EQUAL_DOUBLE(0.0, sin(M_PI));
}

TEST(test_sin, sinus_2_pi)
{
    TEST_ASSERT_EQUAL_DOUBLE(0.0, sin(2 * M_PI));
}

TEST_GROUP_RUNNER(test_sinus_with_normal_values) 
{
    RUN_TEST_CASE(test_sin, sinus_0_pi);
    RUN_TEST_CASE(test_sin, sinus_1_6_pi);
    RUN_TEST_CASE(test_sin, sinus_1_4_pi);
    RUN_TEST_CASE(test_sin, sinus_1_3_pi);
    RUN_TEST_CASE(test_sin, sinus_1_2_pi);
    RUN_TEST_CASE(test_sin, sinus_1_pi);
    RUN_TEST_CASE(test_sin, sinus_2_pi);
}

void runner(void)
{
	RUN_TEST_GROUP(test_sinus_with_normal_values);
}

int main(int argc, char *argv[])
{
	UnityMain(argc, (const char **)argv, runner);
	return 0;
}
