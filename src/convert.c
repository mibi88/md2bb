/*
 * md2bb - A small markdown to BBCode converter.
 * by mibi88
 *
 * This software is under the Unlicense
 */

#include <convert.h>
#include <string.h>

#define LAST_MAX 256

void convert(FILE *in, FILE *out, const Target *target) {
    /* The amount of chars in last */
    size_t last_sz = 0;
    /* The last characters */
    char last[LAST_MAX];
    /* The output characters of last */
    size_t written = 0;
    /* If we are in code: we should parse nothing, we only need to check if the
     * code block ended. */
    char in_code = 0;
    /* If we are in bold, italic and/or strikethrough text */
    char in_bold = 0;
    char in_italic = 0;
    char in_strikethrough = 0;
    /* We are in a code block (i.e., a block where each line starts with an
     * indent). */
    char in_code_block = 0;
    /* How many back ticks were used to start the last code */
    size_t code_start = 0;
    /* The last read character. */
    char c;
    /* If the last written character is a backslash (i.e., the next tag is
     * escaped) */
    char escaped = 0;
    /* Used in for loops */
    size_t i;
    size_t n;
    /* freads return value. */
    int read_out;
    while((read_out = fread(&c, 1, 1, in)) || last_sz-written > 0){
        if(read_out){
            if(last_sz < LAST_MAX){
                last[last_sz] = c;
                last_sz++;
            }else{
                memmove(last, last+1, last_sz-1);
                last[last_sz-1] = c;
                if(written > 0) written--;
            }
        }
        if(last_sz >= LAST_MAX || (!read_out && last_sz-written > 0)){
            /* Convert tabs into four spaces. */
            if(last[written] == '\t'){
                fwrite("    ", 4, 1, out);
            }else{
                fwrite(last+written, 1, 1, out);
            }
            written++;
        }
        /* Handle code blocks */
        /* TODO */
        /* Handle code */
        if(last[written] == '`' && !escaped && !in_code_block){
            for(i=written;i<last_sz && last[i] == '`';i++);
            i -= written;
            if(in_code && i >= code_start){
                if(code_start < 3){
                    fwrite(target->code_end, strlen(target->code_end), 1, out);
                }else{
                    fwrite(target->code_block_end,
                           strlen(target->code_block_end), 1, out);
                }
                written += i;
                in_code = !in_code;
            }else if(!in_code){
                code_start = i;
                if(code_start < 3){
                    fwrite(target->code_start, strlen(target->code_start), 1,
                            out);
                }else{
                    fwrite(target->code_block_start,
                           strlen(target->code_block_start), 1, out);
                }
                written += i;
                in_code = !in_code;
            }
        }
        /* Handle horizontal rules */
        if(last[written] == '\n' && !escaped && !in_code && !in_code_block){
            n = 0;
            for(i=written+1;i<last_sz && (last[i] == '*' || last[i] == '-' ||
                last[i] == ' ');i++){
                if(last[i] == '*' || last[i] == '-') n++;
            }
            if(n >= 3){
                fwrite("\n", 1, 1, out);
                fputs(target->hr, out);
                written = i;
            }
        }
        /* Handle bold and italic text */
        if((last[written] == '*' || last[written] == '_') && !escaped && 
           !in_code && !in_code_block){
            for(i=written;i<last_sz && (last[i] == '*' || last[i] == '_');i++);
            i -= written;
            if(i == 2){
                /* Bold */
                if(in_bold){
                    fputs(target->bold_end, out);
                }else{
                    fputs(target->bold_start, out);
                }
                in_bold = !in_bold;
                written += 2;
            }else if(i == 1){
                /* Italic */
                if(in_italic){
                    fputs(target->italic_end, out);
                }else{
                    fputs(target->italic_start, out);
                }
                in_italic = !in_italic;
                written++;
            }
        }
        /* Handle escaping. */
        if(last[written] == '\\' && !in_code){
            escaped = 1;
        }else{
            escaped = 0;
        }
    }
}