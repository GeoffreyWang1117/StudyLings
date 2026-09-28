// sl.h — tiny helpers shared by Netlings exercises (the modern stand-in for APUE's apue.h).
//
//   sl_die("open")          print "open: <strerror(errno)>" to stderr and exit(1)
//   SL_CHECK(expr)          self-test assertion; failures are counted, not fatal
//   return sl_report();     at the end of main(): prints the verdict, returns exit status
#pragma once

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

[[noreturn]] static inline void sl_die(const char *what) {
    int saved = errno;
    fprintf(stderr, "%s: %s\n", what, strerror(saved));
    exit(1);
}

static int sl_failures [[maybe_unused]] = 0;

#define SL_CHECK(expr)                                                                             \
    do {                                                                                           \
        if (!(expr)) {                                                                             \
            fprintf(stderr, "✗ %s:%d: CHECK failed: %s\n", __FILE__, __LINE__, #expr);             \
            sl_failures++;                                                                         \
        }                                                                                          \
    } while (0)

#define SL_CHECK_EQ(actual, expected)                                                              \
    do {                                                                                           \
        long long a_ = (long long)(actual), e_ = (long long)(expected);                            \
        if (a_ != e_) {                                                                            \
            fprintf(stderr, "✗ %s:%d: %s == %lld, expected %lld\n", __FILE__, __LINE__, #actual,   \
                    a_, e_);                                                                       \
            sl_failures++;                                                                         \
        }                                                                                          \
    } while (0)

static inline int sl_report(void) {
    if (sl_failures) {
        fprintf(stderr, "%d check(s) failed\n", sl_failures);
        return 1;
    }
    puts("ALL CHECKS PASSED");
    return 0;
}
