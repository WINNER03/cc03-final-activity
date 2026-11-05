# =====================================================================
# CC03 Final Activity: Barangay Cooperative Records System
# Module: CC03 - Intermediate Programming (Chapters 10 to 13)
# Rename this file to YOURLASTNAME_final_activity.py before submitting.
# =====================================================================

import os
from collections import deque

LOAN_LOG = "loan_log.txt"
REGISTRY = "registry.txt"

# Start every run from a clean state so the output is the same every time.
for _f in (LOAN_LOG, REGISTRY):
    if os.path.exists(_f):
        os.remove(_f)


def banner(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


# =====================================================================
# CHAPTER 10 - MEMBER ID DIRECTORY (Binary Search Tree)
# =====================================================================

# ---- Step 1: MemberNode and a hand-linked BST of 7 member IDs -------
class MemberNode:
    def __init__(self, member_id):
        self.member_id = member_id
        self.left = None
        self.right = None


# Tree built by linking nodes directly (no insert function):
#
#                 50
#              /      \
#            30        70
#           /  \      /  \
#         20    40  60    80
#
root = MemberNode(50)
root.left = MemberNode(30)
root.right = MemberNode(70)
root.left.left = MemberNode(20)
root.left.right = MemberNode(40)
root.right.left = MemberNode(60)
root.right.right = MemberNode(80)
# Check: every left child is smaller than its parent and every right
# child is larger, so the BST property holds at every level.


# ---- Step 2: The three traversals -----------------------------------
def preorder_members(node):
    # Visit the node first, then the left side, then the right side.
    if node is None:
        return
    print(node.member_id, end=" ")
    preorder_members(node.left)
    preorder_members(node.right)


def inorder_members(node):
    # Left side first, then the node, then the right side.
    if node is None:
        return
    inorder_members(node.left)
    print(node.member_id, end=" ")
    inorder_members(node.right)


def postorder_members(node):
    # Both children first, and the node itself is printed last.
    if node is None:
        return
    postorder_members(node.left)
    postorder_members(node.right)
    print(node.member_id, end=" ")


# ---- Step 3: The buggy print_sorted_members -------------------------
# PREDICTION: The original function prints node.member_id only AFTER it
# has gone through both the left and the right subtree. That is a
# POSTORDER traversal, not a sorted one. For my tree it prints:
#     20 40 30 60 80 70 50
# The root (50) comes out last, and 30 shows up after 40, so the list
# is clearly not smallest-to-largest.
def print_sorted_members_buggy(node):
    if node is None:
        return
    print_sorted_members_buggy(node.left)
    print_sorted_members_buggy(node.right)
    print(node.member_id, end=" ")


# CORRECTED VERSION: move the print between the two recursive calls.
# Why in-order is always sorted on a BST: everything in a node's left
# subtree is smaller than it and everything in its right subtree is
# larger. In-order finishes the whole smaller side before printing the
# node, and only then moves to the larger side. Because this rule is
# true at every node, each ID gets printed only after all smaller IDs
# and before all larger IDs, which is exactly ascending order.
def print_sorted_members(node):
    if node is None:
        return
    print_sorted_members(node.left)
    print(node.member_id, end=" ")
    print_sorted_members(node.right)


banner("CHAPTER 10: MEMBER ID DIRECTORY (BST)")
print("Preorder  : ", end=""); preorder_members(root); print()
print("Inorder   : ", end=""); inorder_members(root); print()
print("Postorder : ", end=""); postorder_members(root); print()
print("Buggy print_sorted_members (postorder): ", end="")
print_sorted_members_buggy(root); print()
print("Fixed print_sorted_members (inorder)  : ", end="")
print_sorted_members(root); print()


# =====================================================================
# CHAPTER 11 - LOAN APPLICATION LOG (File Handling)
# =====================================================================

# ---- Step 4: log_application and load_applications ------------------
def log_application(applicant, amount):
    # "a" (append) adds a new line at the end and keeps old records.
    with open(LOAN_LOG, "a") as file:
        file.write(f"Applicant: {applicant} | Amount: PHP {amount:,.2f}\n")


def load_applications():
    # Returns every record as a list of strings with the newline removed.
    # If the log has never been written, there is nothing to load yet.
    if not os.path.exists(LOAN_LOG):
        return []
    with open(LOAN_LOG, "r") as file:
        return [line.rstrip("\n") for line in file]


# ---- Step 5: The teammate's register_borrower -----------------------
# PREDICTION: registry.txt will only contain "Ben Cruz".
# RESPONSIBLE LINE:  with open("registry.txt", "w") as file:
# WHY: "w" mode empties the file the moment open() runs, before any
# write happens. The first call writes "Ana Reyes", but the second call
# opens the file in "w" mode again, wiping Ana out, then writes Ben.
# Each call erases whatever the call before it saved.
def register_borrower_buggy(name):
    with open(REGISTRY, "w") as file:
        file.write(name + "\n")


# CORRECTED VERSION: use "a" so each new name is added at the end.
def register_borrower(name):
    with open(REGISTRY, "a") as file:
        file.write(name + "\n")


def read_registry():
    with open(REGISTRY, "r") as file:
        return [line.rstrip("\n") for line in file]


banner("CHAPTER 11: LOAN APPLICATION LOG")
print("load_applications() before any log exists:", load_applications())

register_borrower_buggy("Ana Reyes")
register_borrower_buggy("Ben Cruz")
print("registry.txt with BUGGY 'w' version :", read_registry())

os.remove(REGISTRY)
register_borrower("Ana Reyes")
register_borrower("Ben Cruz")
print("registry.txt with FIXED 'a' version :", read_registry())


# =====================================================================
# CHAPTER 12 - INTEGRATED OPERATIONS (deque + hand-built linked list)
# =====================================================================
banner("CHAPTER 12: INTEGRATED OPERATIONS")

# ---- Step 6: Loan-application queue (FIFO) --------------------------
print("\n-- Step 6: Loan application queue --")
loan_queue = deque()
loan_queue.append(("Ana Reyes", 5000))     # enqueue
loan_queue.append(("Ben Cruz", 12000))
loan_queue.append(("Carla Santos", 8000))
print("Queue:", list(loan_queue))

while loan_queue:
    applicant, amount = loan_queue.popleft()  # dequeue (first in, first out)
    log_application(applicant, amount)
    print(f"Processed and logged: {applicant} (PHP {amount:,})")

# ---- Step 7: Transaction undo stack (LIFO) --------------------------
print("\n-- Step 7: Transaction undo stack --")
undo_stack = deque()
undo_stack.append("Deposit PHP 1,000 - Ana Reyes")     # push
undo_stack.append("Loan payment PHP 500 - Ben Cruz")
undo_stack.append("Withdrawal PHP 300 - Carla Santos")
print("Stack:", list(undo_stack))
print("Undo:", undo_stack.pop())                        # last in, first out
print("Undo:", undo_stack.pop())
print("Remaining:", list(undo_stack))


# ---- Step 8: Referral chain (hand-built singly linked list) ---------
class ReferralNode:
    def __init__(self, name):
        self.name = name
        self.next = None


print("\n-- Step 8: Referral chain --")
head = ReferralNode("Ana Reyes")
head.next = ReferralNode("Ben Cruz")
head.next.next = ReferralNode("Carla Santos")
head.next.next.next = ReferralNode("Dante Lim")

current = head
chain = []
while current is not None:
    chain.append(current.name)
    current = current.next
print("Referral chain:", " -> ".join(chain))

# ---- Step 9: Two simulated days -------------------------------------
print("\n-- Step 9: Two-day simulation --")
# Day 1 = the three applications already logged in Step 6.
print("Day 1 records:")
for record in load_applications():
    print("  ", record)

log_application("Dante Lim", 15000)
log_application("Elena Mendoza", 6500)
print("Day 2 records (Day 1 records are still there):")
for record in load_applications():
    print("  ", record)

# ---- Step 10: Why deque, and why the chain is built by hand ---------
# A Python list stores items in one row of memory. list.pop(0) removes
# the first item, so every remaining item has to slide one spot to the
# left to fill the gap. With n items that is about n moves per dequeue,
# so it gets slower as the queue grows (O(n)). A deque is built from
# linked blocks and keeps track of both ends, so popleft() and append()
# just adjust an end pointer and take the same small time no matter how
# long it is (O(1)). For the undo stack, a list's append/pop at the end
# would also be fast, but using deque keeps both structures consistent.
#
# The referral chain is built by hand because the point of it is the
# "who referred whom" link between members. Each ReferralNode owns its
# own next pointer, so we can see and control the links directly and
# walk the chain one member at a time. deque hides those links, and it
# also does not let us easily insert a member in the middle of a chain
# by just rewiring two pointers.


# =====================================================================
# CHAPTER 13 - TESTING AND DEBUGGING
# =====================================================================

# ---- Step 11: The counter, left buggy on purpose --------------------
transactions_undone = 0


def undo_last(stack):
    global transactions_undone
    transactions_undone += 1
    if len(stack) == 0:
        print("Nothing to undo.")
        return None
    return stack.pop()


# ---- Step 13: Fixed version -----------------------------------------
# The counter is meant to count transactions that were ACTUALLY undone.
# The buggy version adds 1 before checking if the stack is empty, so it
# also counts failed attempts. Fix: only add 1 after a real pop.
def undo_last_fixed(stack):
    global transactions_undone
    if len(stack) == 0:
        print("Nothing to undo.")
        return None
    item = stack.pop()
    transactions_undone += 1
    return item


# ---- Step 12: Test suite --------------------------------------------
# Expected results were written BEFORE running:
#  T1 typical: undo on [t1,t2,t3]          -> returns "t3", counter = 1
#  T2 typical: queue of 3, popleft once    -> returns "A"
#  T3 typical: inorder of the member BST   -> [20,30,40,50,60,70,80]
#  T4 edge   : undo on empty stack         -> returns None, counter = 0
#  T5 edge   : popleft on empty queue      -> IndexError is raised
#  T6 edge   : one-member referral chain   -> ["Solo Member"]
#  T7 edge   : single-node tree inorder    -> [99]
#  T8 edge   : load_applications, no file  -> []

def inorder_list(node, out):
    if node is not None:
        inorder_list(node.left, out)
        out.append(node.member_id)
        inorder_list(node.right, out)
    return out


def run_tests(undo_func):
    global transactions_undone
    results = []

    def record(case, condition, expected, actual):
        status = "Pass" if expected == actual else "Fail"
        results.append((case, condition, str(expected), str(actual), status))

    # T1
    transactions_undone = 0
    s = deque(["t1", "t2", "t3"])
    got = undo_func(s)
    record("T1 Undo typical", "stack [t1,t2,t3]",
           ("t3", 1), (got, transactions_undone))

    # T2
    q = deque(["A", "B", "C"])
    record("T2 Queue typical", "queue [A,B,C]", "A", q.popleft())

    # T3
    record("T3 BST inorder", "7-member tree",
           [20, 30, 40, 50, 60, 70, 80], inorder_list(root, []))

    # T4
    transactions_undone = 0
    got = undo_func(deque())
    record("T4 Empty undo stack", "stack []",
           (None, 0), (got, transactions_undone))

    # T5
    try:
        deque().popleft()
        actual = "no error"
    except IndexError:
        actual = "IndexError"
    record("T5 Empty queue", "queue []", "IndexError", actual)

    # T6
    solo = ReferralNode("Solo Member")
    names, cur = [], solo
    while cur is not None:
        names.append(cur.name)
        cur = cur.next
    record("T6 One-member chain", "1 ReferralNode", ["Solo Member"], names)

    # T7
    record("T7 Single-node tree", "tree with ID 99",
           [99], inorder_list(MemberNode(99), []))

    # T8
    os.rename(LOAN_LOG, LOAN_LOG + ".bak")
    actual = load_applications()
    os.rename(LOAN_LOG + ".bak", LOAN_LOG)
    record("T8 Log file missing", "no loan_log.txt", [], actual)

    return results


def print_table(results):
    header = ("Test Case", "Input Condition", "Expected", "Actual", "Result")
    widths = [max(len(r[i]) for r in results + [header]) for i in range(5)]
    line = " | ".join(h.ljust(w) for h, w in zip(header, widths))
    print(line)
    print("-" * len(line))
    for r in results:
        print(" | ".join(c.ljust(w) for c, w in zip(r, widths)))
    passed = sum(1 for r in results if r[4] == "Pass")
    print(f"\n{passed}/{len(results)} tests passed.")


banner("CHAPTER 13: TEST RUN 1 (original undo_last)")
print_table(run_tests(undo_last))

banner("CHAPTER 13: TEST RUN 2 (after fixing undo_last)")
print_table(run_tests(undo_last_fixed))

# ---- Step 14: Debugging log -----------------------------------------
# First I confirmed the output was wrong: in run 1, test T4 expected the
# counter to stay at 0 after undoing on an empty stack, but it read 1.
# The smallest failing input was just an empty deque passed once to
# undo_last. Tracing line by line, the counter was already 1 on the
# "transactions_undone += 1" line, which runs before the empty check, so
# that is where the value split from what I expected. I moved the
# increment to after stack.pop(), reran all 8 tests, and all passed.

banner("END OF PROGRAM")
