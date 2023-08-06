#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS 1
#define DllExport   __declspec( dllexport )
DllExport int PyInit_ext; // hack to compile with setuptools as Extension
DllExport char *hello(char *name);
DllExport void release(void*);
#endif

#include <stdio.h>
#include <string.h>
#include <stdlib.h>



void release(void *buf) {
	free(buf);
}

// hello return a heap allocated string containing the name appended 
// to "hello " and followed by "!".
char *hello(char *name) {
    char *buf = malloc(7+strlen(name));
    sprintf(buf, "hello %s!", name);
    return buf;
}
