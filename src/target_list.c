/*
 * md2bb - A small markdown to BBCode converter.
 * by mibi88
 *
 * This software is under the Unlicense
 */

#include <target_list.h>

extern const Target phpbb;
extern const Target planetcasio;

const Target *target_list[TARGET_NUM] = {
    &phpbb,
    &planetcasio
};
