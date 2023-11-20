from __future__ import annotations
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None):
        """
        This class represents a node in a singly-linked list. It has a value and a pointer to the next node.
        :param val: The value of the node.
        :param next: The next node in the list.
        """
        self.val = val
        self.next = next

    def __str__(self):
        """
        This function returns a string representation of the list.
        :return: A string representation of the list.
        """
        return str(self.val) + " -> " + str(self.next)

    def equals(self, other: Optional[ListNode], as_obj: bool = False) -> bool:
        """
        This function compares two lists, either as objects or as values. (Default is as objects.)
        As objects means that the two lists are the same object in memory.
        As values means that the two lists have the same values in the same order.
        :param other: The other ListNode to compare to.
        :param as_obj: If True, compares the two lists as objects. If False, compares the two lists as values.
        :return: True if the two lists are equal, False otherwise.
        """
        if (self and not other) or (not self and other):
            return False
        if as_obj:
            return self == other
        else:
            h1, h2 = self, other
            while h1 and h2:
                if h1.val != h2.val:
                    return False
                h1, h2 = h1.next, h2.next
            if h1 or h2:
                return False
            return True

    @staticmethod
    def add_two_numbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> ListNode:
        """
        Ref: Leetcode 2. Add Two Numbers
        This function adds two numbers represented by two lists, in reverse order.
        Example: 342 + 465 = 807
        l1 = 2 -> 4 -> 3
        l2 = 5 -> 6 -> 4
        l1 + l2 = 7 -> 0 -> 8
        :param l1: The first list.
        :param l2: The second list.
        :return: The sum of the two lists.
        """
        dummy = ListNode()
        tail, carry = dummy, 0
        while l1 or l2 or carry:
            val = carry
            if l1: val, l1 = val + l1.val, l1.next
            if l2: val, l2 = val + l2.val, l2.next
            tail.next = ListNode(val % 10)
            tail = tail.next
            carry = val // 10
        return dummy.next

    @staticmethod
    def remove_nth_from_end(head: Optional[ListNode], n: int) -> ListNode:
        """
        Ref: Leetcode 19. Remove Nth Node From End of List
        This function removes the nth node from the end of the list.
        :param head: The head of the list.
        :param n: The nth node from the end of the list.
        :return: The head of the list.
        """
        dummy = ListNode(0, head)
        left, right = dummy, head

        while n > 0:
            right = right.next
            n -= 1

        while right:
            left, right = left.next, right.next

        left.next = left.next.next

        return dummy.next

    @staticmethod
    def remove_nth_from_start(head: Optional[ListNode], n: int) -> ListNode:
        """
        This function removes the nth node from the start of the list.
        :param head: The head of the list.
        :param n: The nth node from the end of the list.
        :return: The head of the list.
        """
        dummy = ListNode(0, head)

        tail = dummy

        for _ in range(n-1):
            tail = tail.next

        tail.next = tail.next.next

        return dummy.next

    @staticmethod
    def merge_two_sorted_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> ListNode:
        """
        Ref: Leetcode 21. Merge Two Sorted Lists
        This function merges two sorted lists.
        :param l1: The first sorted list.
        :param l2: The second sorted list.
        :return: The merged sorted list.
        """
        dummy = ListNode()
        tail = dummy

        while l1 and l2:
            if l1.val < l2.val:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next

        tail.next = l1 or l2

        return dummy.next

    @staticmethod
    def reverse_list(head: Optional[ListNode]) -> ListNode:
        """
        Ref: Leetcode 206. Reverse Linked List
        This function reverses a linked list.
        :param head: The head of the list.
        :return: The head of the reversed list.
        """
        prev, tail = None, head
        while tail:
            frwd = tail.next
            tail.next = prev
            prev = tail
            tail = frwd
        return prev