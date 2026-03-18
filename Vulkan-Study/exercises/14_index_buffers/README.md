# 练习 14: 索引缓冲

## 学习目标
- 创建索引缓冲
- 使用索引绘制减少顶点重复
- 优化内存使用

## 关键概念

### 索引绘制
不使用索引绘制 6 个顶点画正方形：
```
0, 1, 2, 2, 3, 0
```

使用索引绘制只需 4 个顶点：
```
顶点: 0, 1, 2, 3
索引: 0, 1, 2, 2, 3, 0
```

### 命令
```cpp
vkCmdBindIndexBuffer(commandBuffer, indexBuffer, 0, VK_INDEX_TYPE_UINT32);
vkCmdDrawIndexed(commandBuffer, indexCount, 1, 0, 0, 0);
```

## 任务
在 main.cpp 中完成 TODO 标记的代码。
