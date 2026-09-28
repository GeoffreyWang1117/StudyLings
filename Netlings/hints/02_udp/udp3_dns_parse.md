## 提示 1
先看真实报文：`dig +noedns @8.8.8.8 www.github.com A` 配合 `tcpdump -i any -X port 53`，
或者 Wireshark。找到头部 12 字节、QNAME 的长度前缀、答案里的 `c0 0c`。

## 提示 2
encode_qname：用 `strchr(p, '.')` 找下一个点，label 长度 = 点的位置 - p；
写 `out[pos++] = len; memcpy(out + pos, p, len); pos += len;`，最后写一个 0。
每写一次都检查不越过 `cap`/255；label 为 0（连续的点）或 > 63 时返回 -1。结尾正好是 '.' 时直接结束。

## 提示 3
parse_name 的指针：`if ((b & 0xC0) == 0xC0) { 检查 off + 1 < len; 检查 ++jumps <= MAX_JUMPS;
if (!jumped) *next = off + 2; jumped = true; off = ((b & 0x3F) << 8) | msg[off + 1]; continue; }`。
遇到 0 结束时，只有在从没跳转过的情况下才设置 `*next = off + 1`。
