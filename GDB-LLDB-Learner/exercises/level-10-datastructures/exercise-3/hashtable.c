#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TABLE_SIZE 10

typedef struct Entry {
    char *key;
    int value;
    struct Entry *next;
} Entry;

typedef struct HashTable {
    Entry **buckets;
    int size;
} HashTable;

unsigned int hash(const char *key) {
    unsigned int hash = 0;
    while (*key) {
        hash = (hash << 5) + *key++;
    }
    return hash % TABLE_SIZE;
}

HashTable* create_table() {
    HashTable *table = malloc(sizeof(HashTable));
    table->size = TABLE_SIZE;
    table->buckets = calloc(TABLE_SIZE, sizeof(Entry*));
    return table;
}

void insert(HashTable *table, const char *key, int value) {
    unsigned int index = hash(key);
    Entry *entry = malloc(sizeof(Entry));
    entry->key = strdup(key);
    entry->value = value;
    
    // 链地址法处理冲突
    entry->next = table->buckets[index];
    table->buckets[index] = entry;
}

int main() {
    printf("=== 哈希表调试 ===\n\n");
    
    HashTable *table = create_table();
    
    // 插入数据（故意制造冲突）
    insert(table, "apple", 100);
    insert(table, "banana", 200);
    insert(table, "cherry", 300);
    insert(table, "date", 400);
    insert(table, "elderberry", 500);
    
    // 打印哈希分布
    printf("Hash distribution:\n");
    for (int i = 0; i < TABLE_SIZE; i++) {
        int count = 0;
        Entry *e = table->buckets[i];
        while (e) {
            count++;
            e = e->next;
        }
        if (count > 0) {
            printf("Bucket[%d]: %d entries\n", i, count);
        }
    }
    
    printf("\n任务:\n");
    printf("1. 检查每个桶的链表\n");
    printf("2. 验证哈希函数分布\n");
    printf("3. 查找特定 key 的存储位置\n");
    
    return 0;
}
