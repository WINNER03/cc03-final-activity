# CC03 Final Activity – Written File
**Barangay Cooperative Records System**

## Test Results (Chapter 13)

Expected results were written before the program was run.

### Run 1 – original `undo_last`

| Test Case | Input Condition | Expected | Actual | Pass/Fail |
|---|---|---|---|---|
| T1 Undo (typical) | stack [t1, t2, t3] | returns "t3", counter = 1 | returns "t3", counter = 1 | Pass |
| T2 Queue (typical) | queue [A, B, C], popleft once | "A" | "A" | Pass |
| T3 BST inorder (typical) | 7-member tree | 20 30 40 50 60 70 80 | 20 30 40 50 60 70 80 | Pass |
| T4 Empty undo stack (edge) | stack [] | returns None, counter = 0 | returns None, counter = 1 | **Fail** |
| T5 Empty queue (edge) | queue [], popleft | IndexError | IndexError | Pass |
| T6 One-member referral chain (edge) | 1 ReferralNode | ["Solo Member"] | ["Solo Member"] | Pass |
| T7 Single-node tree (edge) | tree with ID 99 | [99] | [99] | Pass |
| T8 Missing log file (edge) | no loan_log.txt | [] | [] | Pass |

**Result: 7/8 passed.**

### Run 2 – after fixing `undo_last`

All 8 tests passed (T4 now shows counter = 0).

## The Bug

`transactions_undone` was supposed to count transactions that were actually undone. It actually counted every call to `undo_last`, including calls on an empty stack where nothing was undone, because `transactions_undone += 1` ran before the empty-stack check. The fix moves the increment to after `stack.pop()`, so only successful undos are counted.

## Debugging Log

First I confirmed the output was wrong: test T4 expected the counter to stay at 0 after an undo on an empty stack, but it showed 1. The smallest input that failed was a single call to `undo_last` with an empty deque. Tracing line by line, the counter already became 1 on the `transactions_undone += 1` line, which runs before the `if len(stack) == 0` check, so that is where the value went wrong. I moved the increment to after `stack.pop()`, reran the whole suite, and all 8 tests passed.
