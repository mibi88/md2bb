/*
 * md2bb - A small markdown to BBCode converter.
 * by mibi88
 *
 * This software is under the Unlicense
 */

#ifndef TARGET_H
#define TARGET_H

typedef struct {
    const char *name;
    const char *code_start;
    const char *code_end;
    const char *code_block_start;
    const char *code_block_end;
    const char *bold_start;
    const char *bold_end;
    const char *italic_start;
    const char *italic_end;
    const char *hr;
} Target;

#endif
