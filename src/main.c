/*
 * md2bb - A small markdown to BBCode converter.
 * by mibi88
 *
 * This software is under the Unlicense
 */

#include <stdio.h>
#include <stdlib.h>
#include <convert.h>
#include <target_list.h>

int main(int argc, char **argv) {
    if(argc > 1){
        FILE *fp = fopen(argv[1], "r");
        if(!fp){
            fprintf(stderr, "[ERROR] Cannot open \"%s\"!", argv[1]);
            return EXIT_FAILURE;
        }
        convert(fp, stdout, target_list[0]);
    }else{
        convert(stdin, stdout, target_list[0]);
    }
    return EXIT_SUCCESS;
}

