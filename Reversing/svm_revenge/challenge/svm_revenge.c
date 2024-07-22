#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef enum {
    HALT,
    MUL,
    PUSH,
    ADD,
    POP,
    PUSH_IMM,
    // TRAP
} Opcode;

#include "program.h"

typedef struct Node {
    uint8_t value;
    struct Node* next;
} Node;

typedef struct {
    Node* head;
    Node* last;
    // int length;
} Queue;

typedef struct {
    uint8_t registers[33];
    Queue queue;
} State;

void push(Queue* queue, uint8_t value) {
    Node* last = (Node*)malloc(sizeof(Node));
    last->value = value;
    last->next = NULL;
    if(queue->last != NULL) {
        queue->last->next = last;
    } else {
        queue->head = last;
    }
    queue->last = last;
    // printf("Pushed, new length: %d\n", ++queue->length);
}

int pop(Queue* queue) {
    Node* head = queue->head;
    // if(head == NULL) {
    //     exit(1);
    // }
    int value = head->value;
    queue->head = head->next;
    if(queue->head == NULL) {
        queue->last = NULL;
    }
    free(head);
    // printf("Popped, new length: %d\n", --queue->length);
    return value;
}

void perform_operation(State* state, Opcode opcode, uint8_t argument) {
    int tmp;
    int tmp2;

    // printf("%d\n", opcode);

    switch(opcode) {
        case PUSH:
            push(&state->queue, state->registers[argument]);
            break;
        case PUSH_IMM:
            push(&state->queue, argument);
            break;
        case POP:
            tmp = pop(&state->queue);
            state->registers[argument] = tmp;
            break;
        case ADD:
            tmp = pop(&state->queue);
            tmp2 = pop(&state->queue);
            push(&state->queue, tmp + tmp2);
            break;
        case MUL:
            tmp = pop(&state->queue);
            tmp2 = pop(&state->queue);
            push(&state->queue, tmp * tmp2);
            break;
        // case TRAP:
        //     printf("TRAP %d reached\n", argument);
        //     break;
        // default:
        //     printf("Unknown opcode %d!\n", opcode);
        //     exit(2);
        //     break;
    }
}

void run_program(State* state, uint8_t* program) {
    int pc = 0;

    while(1) {
        Opcode opcode = (Opcode)program[pc++];
        uint8_t argument = program[pc++];

        if(opcode == HALT) {
            break;
        }

        perform_operation(state, opcode, argument);
    }
}

void process_chunk(const char* source, uint8_t* dest) {
    State state = { {}, { NULL, NULL } };

    for(int i = 0; i < 16; i++) {
        push(&state.queue, source[i]);
    }

    run_program(&state, PROGRAM);

    for(int i = 0; i < 16; i++) {
        dest[i] = pop(&state.queue);
    }
}

int main() {
    char flag[65];
    FILE* fptr;
    fptr = fopen("flag.txt", "r");
    fgets(flag, 65, fptr);
    fclose(fptr);

    uint8_t* dest = (uint8_t*)malloc(64);

    for(int i = 0; i < 64; i += 16) {
        // printf("Processing chunk %d\n", i / 16);
        // if(i > 0) {
        //     puts("TRAP");
        // }
        process_chunk(flag + i, dest + i);
    }

    fptr = fopen("output.bin", "w");
    fwrite(dest, 1, 64, fptr);
    fclose(fptr);

    free(dest);

    return 0;
}
