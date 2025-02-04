#ifndef PROMPT_MAEKER_H
#define PROMPT_MAEKER_H
#include <cstring>

class prompt {
public:
    void set_prompt_template(char* prompt_template) {
        this->prompt_template = prompt_template;
    }

    void fill_prompt_template(char* input_keyword, char* input_argv) {
        int template_len = strlen(this->prompt_template);
        int keyword_len = strlen(input_keyword);
        int argv_len = strlen(input_argv);

        for (int i = 0; i < template_len; i++) {
            if (this->prompt_template[i] == input_keyword[0]) {
                bool is_keyword = true;

                for (int j = 0; j < keyword_len; j++) {
                    if (i + j >= template_len || this->prompt_template[i + j] != input_keyword[j]) {
                        is_keyword = false;
                        break;
                    }
                }

                if (is_keyword) {
                    for (int k = 0; k < argv_len; k++) {
                        this->prompt_template[i + k] = input_argv[k];
                    }

                    if (argv_len < keyword_len) {
                        for (int k = i + keyword_len; k < template_len; k++) {
                            this->prompt_template[k - (keyword_len - argv_len)] = this->prompt_template[k];
                        }
                        this->prompt_template[template_len - (keyword_len - argv_len)] = '\0';
                    } else if (argv_len > keyword_len) {
                        for (int k = template_len - 1; k >= i + keyword_len; k--) {
                            this->prompt_template[k + (argv_len - keyword_len)] = this->prompt_template[k];
                        }
                        this->prompt_template[template_len + (argv_len - keyword_len)] = '\0';
                    }
                    i += keyword_len - 1;
                }
            }
        }
    }

private:
    char* prompt_template;
};

#endif
