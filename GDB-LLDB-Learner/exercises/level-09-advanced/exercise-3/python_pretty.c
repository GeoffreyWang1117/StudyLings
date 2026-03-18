#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

Node* create_node(int data) {
    Node *node = malloc(sizeof(Node));
    node->data = data;
    node->next = NULL;
    return node;
}

int main() {
    Node *head = create_node(1);
    head->next = create_node(2);
    head->next->next = create_node(3);

    printf("Linked list created\n");

    // Free memory
    Node *current = head;
    while (current) {
        Node *temp = current;
        current = current->next;
        free(temp);
    }

    return 0;
}
