#define _GNU_SOURCE
#include <stdio.h>
#include <dlfcn.h>

// 劫持 malloc
void* malloc(size_t size) {
    // 获取真正的 malloc
    static void* (*real_malloc)(size_t) = NULL;
    if (!real_malloc) {
        real_malloc = dlsym(RTLD_NEXT, "malloc");
    }

    void *ptr = real_malloc(size);
    fprintf(stderr, "[HOOK] malloc(%zu) = %p\n", size, ptr);
    return ptr;
}

// 劫持 free
void free(void *ptr) {
    static void (*real_free)(void*) = NULL;
    if (!real_free) {
        real_free = dlsym(RTLD_NEXT, "free");
    }

    fprintf(stderr, "[HOOK] free(%p)\n", ptr);
    real_free(ptr);
}
