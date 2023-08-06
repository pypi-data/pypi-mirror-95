/* Copyright (C) 2015 Atsushi Togo */
/* All rights reserved. */

/* This file is part of phonopy. */

/* Redistribution and use in source and binary forms, with or without */
/* modification, are permitted provided that the following conditions */
/* are met: */

/* * Redistributions of source code must retain the above copyright */
/*   notice, this list of conditions and the following disclaimer. */

/* * Redistributions in binary form must reproduce the above copyright */
/*   notice, this list of conditions and the following disclaimer in */
/*   the documentation and/or other materials provided with the */
/*   distribution. */

/* * Neither the name of the phonopy project nor the names of its */
/*   contributors may be used to endorse or promote products derived */
/*   from this software without specific prior written permission. */

/* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS */
/* "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT */
/* LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS */
/* FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE */
/* COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, */
/* INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, */
/* BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; */
/* LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER */
/* CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT */
/* LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN */
/* ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE */
/* POSSIBILITY OF SUCH DAMAGE. */

#include <Python.h>
#include <numpy/arrayobject.h>
#include "phonoc_array.h"
#include "lapack_wrapper.h"

Iarray* convert_to_iarray(const PyArrayObject* npyary)
{
  int i;
  Iarray *ary;

  ary = (Iarray*) malloc(sizeof(Iarray));
  for (i = 0; i < PyArray_NDIM(npyary); i++) {
    ary->dims[i] = PyArray_DIMS(npyary)[i];
  }
  ary->data = (int*)PyArray_DATA(npyary);
  return ary;
}

Darray* convert_to_darray(const PyArrayObject* npyary)
{
  int i;
  Darray *ary;

  ary = (Darray*) malloc(sizeof(Darray));
  for (i = 0; i < PyArray_NDIM(npyary); i++) {
    ary->dims[i] = PyArray_DIMS(npyary)[i];
  }
  ary->data = (double*)PyArray_DATA(npyary);
  return ary;
}

Carray* convert_to_carray(const PyArrayObject* npyary)
{
  int i;
  Carray *ary;

  ary = (Carray*) malloc(sizeof(Carray));
  for (i = 0; i < PyArray_NDIM(npyary); i++) {
    ary->dims[i] = PyArray_DIMS(npyary)[i];
  }
  ary->data = (lapack_complex_double*)PyArray_DATA(npyary);
  return ary;
}
