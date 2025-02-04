#ifndef MACHINE_H
#define MACHINE_H

#include <string>
#include <vector>

class Machine {
public:
    Machine(std::vector<std::vector<std::string>> machine_info): machine_info(machine_info);
    
    string get_info(std::vector<std::vector<std::string>> machine_info, string type_name) {
        char *name_c = type_name.c_str();
        int type_id = 0;
        
        for (int i = 0; i < sizeof &name_c / sizeof &name_c[0]; i ++) {
            type_id += (int) name_c[i];
        }

        return machine_info[type];
    }

    void set_info(std::vector<std::vector<std::string>> machine_info, string type_name, string value) {
        char *name_c = type_name.c_str();
        int type_id = 0;
        
        for (int i = 0; i < sizeof &name_c / sizeof &name_c[0]; i ++) {
            type_id += (int) name_c[i];
        }

        machine_info[type] = value;
    }

    string get_structed_info(std::vector<std::vector<std::string>> machine_info) {
        string info = "";
        for (int i = 0; i < sizeof &machine_info / sizeof &machine_info[0]; i ++) {
            info += machine_info[i][0] + ", " + machine_info[i][1] + "\n";
        }
        return info;
    }

private:
    std::vector<std::vector<std::string>> machine_info;
};

#endif