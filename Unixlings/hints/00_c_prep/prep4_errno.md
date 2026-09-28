## 提示 1
`long v = strtol(s, &end, 10);` 之后：`end == s` 说明一个数字都没解析到；`*end != '\0'` 说明后面有垃圾。

## 提示 2
strtol 只在溢出时设置 errno = ERANGE，成功时 errno 保持原值 —— 所以调用前先 `errno = 0`。

## 提示 3
`/proc/self/stat/child`：路径中间的组件是普通文件而不是目录，内核返回 ENOTDIR。
open 失败后立即保存 errno（`return -errno;`），中间不要调用其他可能改写 errno 的函数（比如 printf）。
