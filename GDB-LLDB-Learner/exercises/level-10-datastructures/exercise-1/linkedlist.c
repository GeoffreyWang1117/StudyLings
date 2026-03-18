#include <stdio.h>
#include <stdlib.h>

// 单链表节点
typedef struct Node {
    int data;
    struct Node *next;
} Node;

// 双链表节点
typedef struct DNode {
    int data;
    struct DNode *prev;
    struct DNode *next;
} DNode;

// 创建单链表: 1 -> 2 -> 3 -> 4 -> 5
Node* create_list() {
    Node *head = malloc(sizeof(Node));
    head->data = 1;

    Node *current = head;
    for (int i = 2; i <= 5; i++) {
        current->next = malloc(sizeof(Node));
        current = current->next;
        current->data = i;
        current->next = NULL;
    }

    return head;
}

// 创建循环链表 (有 BUG!)
Node* create_circular() {
    Node *head = malloc(sizeof(Node));
    head->data = 10;

    Node *current = head;
    for (int i = 20; i <= 50; i += 10) {
        current->next = malloc(sizeof(Node));
        current = current->next;
        current->data = i;
    }

    // BUG: 忘记让最后一个节点指向 head
    current->next = NULL;  // 应该是 current->next = head;

    return head;
}

// 创建双链表 (有 BUG!)
DNode* create_doubly() {
    DNode *head = malloc(sizeof(DNode));
    head->data = 100;
    head->prev = NULL;
    head->next = NULL;

    DNode *current = head;
    for (int i = 200; i <= 500; i += 100) {
        DNode *new_node = malloc(sizeof(DNode));
        new_node->data = i;
        new_node->next = NULL;

        // BUG: 第三个节点的 prev 指针设置错误
        if (i == 300) {
            new_node->prev = head;  // 应该是 current
        } else {
            new_node->prev = current;
        }

        current->next = new_node;
        current = new_node;
    }

    return head;
}

// 打印链表（可能死循环）
void print_list(Node *head, int max_nodes) {
    printf("List contents: ");
    Node *current = head;
    int count = 0;

    while (current != NULL && count < max_nodes) {
        printf("%d ", current->data);
        current = current->next;
        count++;
    }

    if (current != NULL) {
        printf("... (stopped at max_nodes=%d, possible cycle)", max_nodes);
    }
    printf("\n");
}

// 释放链表（可能泄漏）
void free_list(Node *head) {
    Node *current = head;
    Node *temp;
    int count = 0;

    // BUG: 没有检测环，会无限循环
    while (current != NULL && count < 100) {  // 简单的保护
        temp = current;
        current = current->next;
        free(temp);
        count++;
    }

    if (count >= 100) {
        printf("Warning: Stopped freeing after %d nodes (possible cycle)\n", count);
    }
}

int main() {
    printf("=== 链表调试练习 ===\n\n");

    // 1. 单链表
    printf("1. Creating regular linked list...\n");
    Node *list = create_list();
    print_list(list, 20);
    printf("   List head address: %p\n", (void*)list);
    printf("   First node: data=%d, next=%p\n\n", list->data, (void*)list->next);

    // 2. 循环链表（有 bug）
    printf("2. Creating circular linked list...\n");
    Node *circular = create_circular();
    print_list(circular, 20);  // 应该检测到环
    printf("   Circular head address: %p\n\n", (void*)circular);

    // 3. 双链表（有 bug）
    printf("3. Creating doubly linked list...\n");
    DNode *doubly = create_doubly();

    printf("   Doubly list (forward): ");
    DNode *d = doubly;
    int count = 0;
    while (d != NULL && count < 20) {
        printf("%d ", d->data);
        d = d->next;
        count++;
    }
    printf("\n");

    printf("   Doubly head address: %p\n", (void*)doubly);
    printf("   Second node: data=%d, prev=%p (should be %p)\n",
           doubly->next->data,
           (void*)doubly->next->prev,
           (void*)doubly);

    // 检查第三个节点的 prev 指针（有 bug）
    if (doubly->next->next) {
        printf("   Third node: data=%d, prev=%p (should be %p)\n",
               doubly->next->next->data,
               (void*)doubly->next->next->prev,
               (void*)doubly->next);
    }

    printf("\n=== 任务 ===\n");
    printf("1. 使用调试器遍历单链表\n");
    printf("2. 检测循环链表是否真的形成了环\n");
    printf("3. 找出双链表 prev 指针的错误\n");
    printf("4. 查看各个节点的内存布局\n");
    printf("5. 尝试释放链表，观察是否有内存泄漏\n");

    // 注意：实际使用时需要释放内存
    // free_list(list);
    // free_list(circular);  // 这会有问题，因为是环
    // free_doubly(doubly);

    return 0;
}
