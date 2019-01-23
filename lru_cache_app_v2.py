import sys
from pypeg2 import *
import re


number = re.compile(r"\d+")
Symbol.regex = re.compile(r"[\w\.]+")


class Size:
    command = "SIZE"
    grammar = "SIZE", blank, attr("size", number), endl


class Set:
    command = "SET"
    grammar = "SET", blank, attr("key", word), blank, attr("value", Symbol), endl


class Get:
    command = "GET"
    value = None
    grammar = "GET", blank, attr("key", word), endl


class Exit:
    command = "EXIT"
    grammar = "EXIT", endl


class Instruction(List):
    grammar = some([Get, Set, Exit])


class Node:
    def __init__(self, key):
        self.key = key
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def remove(self, key):
        current = self.head
        prev = None
        # Empty list
        if current is None:
            raise KeyError
        while current is not None:
            if current.key == key:
                # Remove from middle or tail
                if prev is not None:
                    prev.next = current.next
                    if prev.next is None:
                        self.tail = prev
                # Remove from head
                else:
                    self.head = current.next
                    # If it was the only node
                    if self.head is None:
                        self.tail = None
                self.length -= 1
                return
            prev = current
            current = current.next
        else:
            # Key is not in the list
            raise KeyError

    def add_to_tail(self, key):
        new = Node(key)
        old_tail = self.tail
        if old_tail is not None:
            old_tail.next = new
        else:
            self.head = new
        self.tail = new
        self.length += 1

    def add_to_head(self, key):
        new = Node(key)
        new.next = self.head
        self.head = new
        if new.next is None:
            self.tail = new
        self.length += 1

    def remove_head(self):
        if self.head is not None:
            old_head = self.head
            self.head = old_head.next
            self.length -= 1
            if self.head is None:
                self.tail = None

    def move_to_tail(self, key):
        self.remove(key)
        self.add_to_tail(key)


class LRUCache:
    def __init__(self, size):
        self.mapping = {}
        self.ordering = LinkedList()
        self.size = size

    def size_control(self):
        while self.ordering.length > self.size:
            del self.mapping[self.ordering.head.key]
            self.ordering.remove_head()

    def set(self, key, value):
        if key not in self.mapping.keys():
            self.ordering.add_to_tail(key)
            self.mapping[key] = value
            self.size_control()
        else:
            self.mapping[key] = value
            self.ordering.move_to_tail(key)

    def get(self, key):
        self.ordering.move_to_tail(key)
        return self.mapping[key]


def lru_cache2(input=sys.stdin, output=sys.stdout):
    cache = None
    size = None
    while not size:
        size_input = input.readline()
        try:
            size_parsed = parse(size_input, Size)
            size = int(size_parsed.size)
            cache = LRUCache(size)
            output.write('SIZE OK\n')
        except SyntaxError:
            output.write('You should set size of a cache:\n')
    if cache:
        for s in input:
            try:
                instructions = parse(s, Instruction)
                for item in instructions:
                    if item.command == "EXIT":
                        return
                    if item.command == "SET":
                        cache.set(item.key, item.value)
                        output.write('SET OK\n')
                    if item.command == "GET":
                        try:
                            value = cache.get(item.key)
                            output.write('GOT {0}\n'.format(value))
                        except KeyError:
                            output.write('NOTFOUND\n')
            except SyntaxError:
                output.write('ERROR\n')

