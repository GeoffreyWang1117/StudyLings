## 提示 1
`*a` 读写的是 a 指向的那个 int。交换需要一个临时变量：`int t = *a; *a = *b; *b = t;`

## 提示 2
max_index 的关键是"失败时不写输出参数"：先判断 `n == 0` 就 `return false`，
只有找到结果后才 `*out = best;`。waitpid、getaddrinfo 等 API 都遵守这个约定。

## 提示 3
reverse 只需要循环 `n / 2` 次，交换 `a[i]` 和 `a[n - 1 - i]`。
注意 `n == 0` 时 `n - 1` 在 size_t 下会变成一个巨大的数 —— 这就是为什么循环条件用 `i < n / 2`。
