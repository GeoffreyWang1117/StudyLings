// EXERCISE: prep3_strings — C 字符串：有界拷贝、原地切分、去空白
// TOPIC: '\0' 结尾 / 缓冲区大小 / 原地修改
// DIFFICULTY: ★★☆☆☆
// BOOK: 预备章 —— 解析 /proc、HTTP 头、配置文件、命令行时天天用到；缓冲区溢出是 C 最经典的漏洞
// I AM NOT DONE
//
// 说明：
//   1. bounded_copy：类似 BSD/glibc 2.38 的 strlcpy —— 最多写 size 字节（含 '\0'），size > 0 时结果
//      总是以 '\0' 结尾；返回 strlen(src)，调用者用 "返回值 >= size" 判断是否被截断。
//      现在的实现直接 strcpy，会写越界 —— AddressSanitizer 会当场抓住它。
//   2. split_inplace：像 strsep 一样按分隔符原地切分："a,,b" → "a" "" "b"（连续分隔符产生空字段）。
//      把分隔符改写成 '\0'，fields[i] 指向各段开头；最多 max 段，返回段数。
//   3. trim：去掉首尾空白（isspace），返回指向第一个非空白字符的指针，尾部原地写 '\0'。
//      用它解析 "Host:   example.com  \r\n" 这类 HTTP 头。

#include "sl.h"

#include <ctype.h>
#include <string.h>

// TODO: 有界拷贝，永不越界
static size_t bounded_copy(char *dst, const char *src, size_t size) {
    strcpy(dst, src);
    return strlen(src);
}

// TODO: 原地切分，返回字段数（最多 max 个）
static size_t split_inplace(char *s, char delim, char **fields, size_t max) {
    return 0;
}

// TODO: 去掉首尾空白
static char *trim(char *s) {
    return s;
}

// ---- 以下为自测，不要修改 ----
int main(void) {
    char small[8];
    SL_CHECK_EQ(bounded_copy(small, "hi", sizeof small), 2);
    SL_CHECK(strcmp(small, "hi") == 0);
    SL_CHECK_EQ(bounded_copy(small, "0123456789abcdef", sizeof small), 16); // 返回值 >= size → 截断了
    SL_CHECK(strcmp(small, "0123456") == 0);
    char untouched = 'X';
    SL_CHECK_EQ(bounded_copy(&untouched, "abc", 0), 3); // size == 0：一个字节也不许写
    SL_CHECK(untouched == 'X');

    char line[] = "GET,/index.html,,HTTP/1.1";
    char *f[8];
    size_t n = split_inplace(line, ',', f, 8);
    SL_CHECK_EQ(n, 4);
    if (n == 4) {
        SL_CHECK(strcmp(f[0], "GET") == 0);
        SL_CHECK(strcmp(f[1], "/index.html") == 0);
        SL_CHECK(strcmp(f[2], "") == 0);
        SL_CHECK(strcmp(f[3], "HTTP/1.1") == 0);
    }
    char two[] = "a:b:c";
    SL_CHECK_EQ(split_inplace(two, ':', f, 2), 2); // 超过 max 的部分不再切分，也不越界写 fields

    char hdr[] = "   example.com  \r\n";
    SL_CHECK(strcmp(trim(hdr), "example.com") == 0);
    char blank[] = " \t\r\n";
    SL_CHECK(strcmp(trim(blank), "") == 0);
    return sl_report();
}
