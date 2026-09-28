## 提示 1
`INT_MAX - (-5)` 在 int 上溢出（而且是未定义行为，UBSan 会报错）。改用 `(x > y) - (x < y)`，结果只可能是 -1/0/1。

## 提示 2
for_each 只是一个循环：`for (size_t i = 0; i < n; i++) fn(&arr[i], ctx);`

## 提示 3
`void *` 可以隐式转换成任意对象指针：`struct stats *st = ctx;` —— pthread 线程函数拿参数也是这么写。
