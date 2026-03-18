#include <stdio.h>
#include <stdint.h>

// Union 示例
union Data {
    int i;
    float f;
    char bytes[4];
};

// 位域示例
struct Flags {
    unsigned int flag1 : 1;
    unsigned int flag2 : 1;
    unsigned int value : 6;
    unsigned int reserved : 24;
};

// 网络数据包头（位域应用）
struct PacketHeader {
    uint8_t version : 4;
    uint8_t header_length : 4;
    uint8_t type_of_service;
    uint16_t total_length;
};

int main() {
    printf("=== Union 内存共享 ===\n");
    union Data data;
    
    data.i = 0x41424344;  // 'ABCD' in ASCII
    printf("作为 int: 0x%x\n", data.i);
    printf("作为 bytes: %c%c%c%c\n", 
           data.bytes[0], data.bytes[1], data.bytes[2], data.bytes[3]);
    
    data.f = 3.14f;
    printf("作为 float: %.2f\n", data.f);
    printf("作为 bytes (hex): %02x %02x %02x %02x\n",
           data.bytes[0], data.bytes[1], data.bytes[2], data.bytes[3]);
    
    printf("\n=== 位域 ===\n");
    struct Flags flags = {1, 0, 42, 0};
    printf("sizeof(Flags) = %lu\n", sizeof(flags));
    printf("flag1=%u, flag2=%u, value=%u\n", flags.flag1, flags.flag2, flags.value);
    
    printf("\n任务: 使用调试器查看 union 和位域的实际内存\n");
    
    return 0;
}
