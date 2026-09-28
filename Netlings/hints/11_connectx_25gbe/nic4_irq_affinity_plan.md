## 提示 1
先看真机器上的原始数据：`ls /sys/class/net/IFACE/device/msi_irqs`、
`grep mlx5 /proc/interrupts`、`cat /sys/class/net/IFACE/device/local_cpulist`。
cpulist 的格式是逗号分隔的 "N" 或 "LO-HI"。

## 提示 2
`parse_cpulist` 的骨架：
```c
while (*p && *p != '\n') {
    long lo = strtol(p, &end, 10);  if (end == p) return -1;
    long hi = lo;  p = end;
    if (*p == '-') { hi = strtol(p + 1, &end, 10); if (end == p + 1 || hi < lo) return -1; p = end; }
    for (long c = lo; c <= hi; c++) { if (n >= cap) return -1; out[n++] = (int)c; }
    if (*p == ',') p++; else if (*p && *p != '\n') return -1;
}
```

## 提示 3
`queue_index_from_name`：`const char *m = strstr(name, "mlx5_comp");` 找到后
`isdigit(m[9])` 再 `strtol(m + 9, nullptr, 10)`；"-TxRx-" 同理。
`build_plan`：`plan[i] = local[i % nlocal]`。真机器上 `--apply` 之后用
`grep mlx5_comp /proc/interrupts` 看每个中断的计数是不是只在对应那一列 CPU 上增长。
