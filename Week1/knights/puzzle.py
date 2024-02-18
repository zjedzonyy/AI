from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

ASaidAKnight = Symbol("A said 'I am a knave'")
ASaidAKnave = Symbol("A said 'I am a Knave'")

# Puzzle 0
# A says "I am both a knight and a knave."
# jezeli jest rycerzem to mowi prawde, jezeli huliganem to klamie
knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# jezeli A to łotczyk to znaczy ze oboje nie są łotrzykami, czyli jeden z nich jest knights
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Or(AKnight, BKnight) )
)

# Puzzle 2
# A says "We are the same kind."
    # jezeli A to rycerz to A jest rycerz i B jest rycerz
    # jezeli A to łotrzyk to A != B
# B says "We are of different kinds."
    # jezeli B to rycerz to albo A = rycerz i B = lotrzyk LUB A = lotrzyk i B = rycerz
    # jezeli B to lotrzyk to A == B
knowledge2 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Implication(AKnight, BKnight),
    Implication(AKnave, BKnight),
    Implication(BKnight, AKnave),
    Implication(BKnave, AKnave)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),
    Or(ASaidAKnave, ASaidAKnight),
    Not(And(ASaidAKnave, ASaidAKnight)),
    Implication(ASaidAKnight, AKnight),
    Not(And(ASaidAKnight, AKnave)),
    Not(And(ASaidAKnave, AKnight)),
    Not(And(ASaidAKnave, AKnave)),
    Implication(BKnight, ASaidAKnave),
    Implication(BKnave, Not(ASaidAKnave)),
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
