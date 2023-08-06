# Hello World!

Minimal example demonstrating the production of module with an external C library. It 
also demonstrate the automatic generation and uploading of the sdist and wheels for
unix, Windows and MacOS. 

The module contains a simple function that receive a string as argument and return a 
string containing "hello " with the argument string appended. The example uses 
`ctypes` to wrap the C library function.

