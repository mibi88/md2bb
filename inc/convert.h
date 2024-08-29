/*
 * md2bb - A small markdown to BBCode converter.
 * by mibi88
 *
 * This software is under the Unlicense
 */

#ifndef CONVERT_H
#define CONVERT_H

#include <stdio.h>
#include <target.h>

void convert(FILE *in, FILE *out, const Target *target);

#endif

