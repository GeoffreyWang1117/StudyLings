## 提示 1
bounded_copy：先 `len = strlen(src)`；要拷贝的字节数是 `min(len, size - 1)`，然后补 '\0'。
`size == 0` 要单独处理，否则 `size - 1` 在 size_t 下会变成 SIZE_MAX。

## 提示 2
split_inplace：`fields[n++] = s; char *d = strchr(s, delim); if (d) *d++ = '\0'; s = d;`，
循环条件 `s != NULL && n < max`。

## 提示 3
`isspace(c)` 的参数必须是 `unsigned char` 范围内的值或 EOF，对 `char` 先转换：`isspace((unsigned char)*s)`。
