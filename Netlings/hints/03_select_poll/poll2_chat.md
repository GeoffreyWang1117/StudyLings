## 提示 1
广播时跳过发送者：`broadcast(from, ...)` 的循环里 `if (i == from) continue;`。
注意 pfds[0] 是监听 socket，客户端从下标 1 开始。

## 提示 2
从数组中删除元素最便宜的办法是"和最后一个交换"：
`nfds--; pfds[i] = pfds[nfds]; conns[i] = conns[nfds];`
pfds 和 conns 必须同步搬，否则 id 和 fd 就对不上了。

## 提示 3
为什么 serve() 里要倒序遍历？删除 i 时，原来的最后一个元素被搬到了 i；
倒序遍历时它已经处理过了，不会被漏掉或处理两次。
另一种做法是把 fd 设成 -1（poll 会忽略负的 fd），循环结束后再统一压缩。
看看空转有多严重：用 starter 版本连上再断开，然后 `top -p $(pgrep poll2_chat)`。
