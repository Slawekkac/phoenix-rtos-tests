#include <stdio.h>
#include <unistd.h>

int main(int argc, char** argv)
{
	char c = '\0';

	printf("[Start test-1 example]\n");

	while (c != '\n') {
		read(STDIN_FILENO, &c, 1);
		putchar(c);
	}

	printf("[Success!]\n");
	return 0;
}
