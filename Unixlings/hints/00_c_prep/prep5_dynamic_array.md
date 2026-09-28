## 提示 1
扩容模板：`size_t ncap = v->cap ? v->cap * 2 : 4; int *p = realloc(v->data, ncap * sizeof *v->data); if (!p) return -1; v->data = p; v->cap = ncap;`
`realloc(NULL, n)` 等价于 `malloc(n)`，所以空数组不需要特殊处理。

## 提示 2
vec_free 之后把结构体整体清零：`*v = (struct vec){};`（C23 允许空花括号初始化）。

## 提示 3
join_ints 两遍法：第一遍用 `snprintf(nullptr, 0, ...)` 累加长度，malloc，第二遍真正写入。
LeakSanitizer 报告会指出泄漏内存是在哪一行分配的。
