---------------- MODULE verify_capital_constitution ----------------
EXTENDS Integers, Sequences, FiniteSets

CONSTANTS
    TOTAL_AUM,        \* Total Assets Under Management
    MIN_RESERVE_RATE, \* 10%
    MAX_ALLOC_RATE,   \* 20%
    THRESHOLD_RATE    \* 5% (MultiSig required)

VARIABLES
    balance,          \* Current liquid balance
    invested,         \* Amount currently in investments
    pending_withdraw, \* Requested withdrawal amount
    multisig_approved \* Boolean flag for quorum

vars == <<balance, invested, pending_withdraw, multisig_approved>>

TypeOK ==
    /\ balance \in Int
    /\ invested \in Int
    /\ balance >= 0
    /\ invested >= 0
    /\ multisig_approved \in BOOLEAN

Init ==
    /\ balance = 1000
    /\ invested = 0
    /\ pending_withdraw = 0
    /\ multisig_approved = FALSE

\* Constitutional Invariants
LiquidityInvariant == balance >= (balance + invested) * MIN_RESERVE_RATE / 100
AllocationInvariant == invested <= (balance + invested) * MAX_ALLOC_RATE / 100
MultiSigInvariant == (pending_withdraw > (balance + invested) * THRESHOLD_RATE / 100) => multisig_approved

Next ==
    \/ /\ pending_withdraw = 0
       /\ \exists amt \in 1..100 :
            /\ balance >= amt
            /\ balance' = balance - amt
            /\ invested' = invested + amt
            /\ UNCHANGED <<pending_withdraw, multisig_approved>>
    \/ /\ pending_withdraw > 0
       /\ multisig_approved = TRUE
       /\ balance' = balance + pending_withdraw
       /\ pending_withdraw' = 0
       /\ multisig_approved' = FALSE
       /\ UNCHANGED <<invested>>

Spec == Init /\ [][Next]_vars

=============================================================================
