
#include <python2.6/Python.h>

int rdtsc(){
  __asm__ __volatile__("rdtsc");}

float pi(int n){

  double i,x,y,sum=0;

  srand(rdtsc());

  for(i=0;i<n;i++){

    x=rand();
    y=rand();

    if (x*x+y*y<(double)RAND_MAX*RAND_MAX)
      sum++; }

  return 4*(float)sum/(float)n; }


static PyObject *
pi_pi(PyObject *self, PyObject *args)
{
    const int n;

    if (!PyArg_ParseTuple(args, "i", &n)) 
      return NULL;

    return Py_BuildValue("f", pi(n));
}


static PyMethodDef PiMethods[] = {
    {"pi",  pi_pi, METH_VARARGS, "Simple Pi Approximation"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initpi(void)
{
    (void) Py_InitModule("pi", PiMethods);
}

int main() {
    printf("%f\n", pi(5000000));
    return 0;}

