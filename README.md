# CC03 Final Activity: Barangay Cooperative Records System

Final activity for **CC03 – Intermediate Programming** (Chapters 10–13: Trees, File Handling, Data Structures and Libraries, Testing and Debugging).

A Python program for a barangay cooperative's tricycle terminal and member loan desk. It uses:

- a **binary search tree** of member IDs, with preorder, inorder and postorder traversals
- **file persistence** for a loan application log (`loan_log.txt`) and a borrower registry (`registry.txt`)
- **`collections.deque`** as a loan application queue and a transaction undo stack
- a **hand-built linked list** for the member referral chain
- a **test suite** of 8 cases that finds and confirms the fix for a bug in the undo counter

## Files

| File | Description |
|---|---|
| `LASTNAME_final_activity.py` | The full program (all 14 steps) |
| `LASTNAME_written_file.md` | Test results table and debugging log |

## How to run

Requires Python 3. From the project folder:

```
python LASTNAME_final_activity.py
```

The program prints labeled output for every step and creates `loan_log.txt` and `registry.txt` in the same folder.
