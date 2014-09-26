#include <stdlib.h>
#include <stdio.h>

/* Globals */
errCount = 0;

int main()
{
	readFile();

}

int readFile()
{
	FILE *f;
	char *line = NULL;
	size_t = len = 0;
	ssize_t = read;
	char **lines = NULL;

	f = fopen("./test/commands.txt")
	if (f == NULL)
	{
		fprintf(stderr, "Error opening file.");
		exit(1);
	}

	while ((read = getline(&line, &len, f)) != -1)
	{
		printf("%s", line);
	}

	if (line)
		free(line);
	exit(0);

}