// EXERCISE: prep4_errno — 错误处理的两种约定：-1 + errno 与 -errno
// TOPIC: errno / strerror / strtol 的正确用法
// DIFFICULTY: ★★☆☆☆
// BOOK: APUE §1.7；man 3 errno、man 3 strtol
//
// 说明：
//   POSIX 函数失败时通常返回 -1 并设置全局（实为线程局部）变量 errno；
//   Linux 内核、io_uring 的 cqe->res、很多现代 C 库则直接返回 -errno（负的错误码）。
//   Rust 的 std::io::Error::from_raw_os_error、Go 的 syscall.Errno 都是在包装这两种约定。
//   1. parse_long：把字符串解析为 [min, max] 内的 long。atoi/atol 无法报告错误，必须用 strtol：
//        - 空串、没有数字、数字后面有多余字符（"12abc"）→ 返回 -1，errno = EINVAL
//        - 溢出 long（strtol 会设置 ERANGE）或不在 [min, max] → 返回 -1，errno = ERANGE
//        - 成功返回 0 并写 *out；失败时不写 *out
//      注意：strtol 成功时不会把 errno 清零，调用前要自己 errno = 0。
//   2. open_ro：打开文件只读，成功返回 fd，失败返回 -errno（内核风格）。

#include "sl.h"

#include <fcntl.h>
#include <limits.h>
#include <unistd.h>

// TODO: 用 strtol 实现带完整错误检查的解析
static int parse_long(const char *s, long min, long max, long *out) {
    char *end;
    errno = 0;
    long v = strtol(s, &end, 10);
    if (end == s || *end != '\0') { // 没有消费任何数字，或数字后面还有东西
        errno = EINVAL;
        return -1;
    }
    if (errno == ERANGE || v < min || v > max) {
        errno = ERANGE;
        return -1;
    }
    *out = v;
    return 0;
}

// TODO: 失败时返回 -errno
static int open_ro(const char *path) {
    int fd = open(path, O_RDONLY | O_CLOEXEC);
    return fd < 0 ? -errno : fd;
}

// ---- 以下为自测，不要修改 ----
int main(void) {
    long v = -1;
    SL_CHECK_EQ(parse_long("8080", 1, 65535, &v), 0);
    SL_CHECK_EQ(v, 8080);
    SL_CHECK_EQ(parse_long("  -42", -100, 100, &v), 0); // strtol 允许前导空白和符号
    SL_CHECK_EQ(v, -42);

    const char *bad[] = {"", "abc", "12abc", "0x", " "};
    for (size_t i = 0; i < sizeof bad / sizeof bad[0]; i++) {
        v = 777;
        errno = 0;
        SL_CHECK_EQ(parse_long(bad[i], LONG_MIN, LONG_MAX, &v), -1);
        SL_CHECK_EQ(errno, EINVAL);
        SL_CHECK_EQ(v, 777);
    }
    errno = 0;
    SL_CHECK_EQ(parse_long("99999999999999999999999", LONG_MIN, LONG_MAX, &v), -1);
    SL_CHECK_EQ(errno, ERANGE);
    errno = 0;
    SL_CHECK_EQ(parse_long("70000", 1, 65535, &v), -1);
    SL_CHECK_EQ(errno, ERANGE);

    SL_CHECK_EQ(open_ro("/definitely/not/here"), -ENOENT);
    SL_CHECK_EQ(open_ro("/proc/self/stat/child"), -ENOTDIR);
    int fd = open_ro("/proc/self/stat");
    SL_CHECK(fd >= 0);
    if (fd >= 0)
        close(fd);
    printf("strerror(ENOENT) = \"%s\"\n", strerror(ENOENT));
    return sl_report();
}
