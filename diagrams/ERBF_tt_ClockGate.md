```mermaid
%% ERBF Clock-Gated Power States FSM
%% Finite-state machine showing how Tensix cores wake/sleep per ERBF time-step
%% Green = Active compute states, Yellow = Transition states, Red = Sleep states
stateDiagram-v2
    [*] --> PowerOn
    PowerOn --> SLEEP_DEEP : Boot complete

    SLEEP_DEEP --> WAKE_PENDING : ERBF timestep start
    WAKE_PENDING --> CONTEXT_INJECT : Clock stable 2us

    CONTEXT_INJECT --> EDGE_GATE : Context ready
    EDGE_GATE --> RECURRENT_UPDATE : Gates computed
    RECURRENT_UPDATE --> BELIEF_UPDATE : State updated
    BELIEF_UPDATE --> SLEEP_LIGHT : Timestep complete

    SLEEP_LIGHT --> SLEEP_DEEP : No pending work 10us
    SLEEP_LIGHT --> WAKE_PENDING : New timestep arriving

    SLEEP_DEEP --> CONTEXT_INJECT : Emergency wake 5us
    SLEEP_LIGHT --> CONTEXT_INJECT : Fast wake 1us
    CONTEXT_INJECT --> SLEEP_DEEP : Force sleep signal

    state SLEEP_DEEP {
        [*] --> CoreClockGated
        CoreClockGated --> L1Retained
        L1Retained --> EthernetActive
    }
    note right of SLEEP_DEEP : Core fully clock-gated\nL1 SRAM retained\nEthernet tiles active\nPower 5W per core

    state WAKE_PENDING {
        [*] --> ClockUngate
        ClockUngate --> DMAWarm
        DMAWarm --> NoCReady
    }
    note right of WAKE_PENDING : Clock ungating started\nDMA engines warming\nNoC routers active\nPower 15W per core

    state CONTEXT_INJECT {
        [*] --> AttentionComp
        AttentionComp --> AllTensixActive
    }
    note left of CONTEXT_INJECT : Attention computation\na = Attn_Phi(Rel t)\nAll Tensix active\nPower 40W per core

    state EDGE_GATE {
        [*] --> GateComp
        GateComp --> SFPUActive
    }
    note left of EDGE_GATE : Gate computation\nW(e,t) = sigma(a[e])\nSFPU + NoC active\nPower 35W per core

    state RECURRENT_UPDATE {
        [*] --> RNNComp
        RNNComp --> MatMulActive
    }
    note left of RECURRENT_UPDATE : RNN computation\nState(n,t+1) = RNN_Theta(...)\nMatMul engines active\nPower 45W per core

    state BELIEF_UPDATE {
        [*] --> PosteriorInf
        PosteriorInf --> ReducedUtil
    }
    note left of BELIEF_UPDATE : Posterior inference\nOptional on some nodes\nReduced core utilization\nPower 25W per core

    state SLEEP_LIGHT {
        [*] --> CoresIdle
        CoresIdle --> L1Preserved
        L1Preserved --> DMAReady
    }
    note right of SLEEP_LIGHT : Cores idle but clocked\nL1 data preserved\nDMA/NoC ready\nPower 10W per core
```
A finite state machine diagram showing how Tensix cores can be clock-gated during ERBF operation to save power while maintaining deterministic latency. Here are the key power states:
Sleep States (Power Saving):

SLEEP_DEEP: Full clock gating (~5W per core) - L1 SRAM retained, only Ethernet tiles active
SLEEP_LIGHT: Cores idle but clocked (~10W per core) - Ready for fast wake-up

Active States (ERBF Computation):

CONTEXT_INJECT: Attention computation (~40W) - Full Tensix utilization for Attn_Φ
EDGE_GATE: Gate computation (~35W) - SFPU active for σ(a[e])
RECURRENT_UPDATE: RNN computation (~45W) - Peak power for matrix operations
BELIEF_UPDATE: Posterior inference (~25W) - Optional, reduced utilization

Transition Management:

WAKE_PENDING: Clock ungating transition (~15W) - 2μs deterministic wake-up

Deterministic Timing:

Cores wake 2μs before each ERBF time-step to ensure zero compute latency
Emergency wake paths for asynchronous events (1-5μs)
Predictable sleep windows between time-steps for maximum power savings

This FSM ensures that ERBF's distributed cortical nodes can operate with deterministic latency while aggressively clock-gating unused cores, potentially reducing power consumption by 70-80% during sparse activation patterns typical in cortical processing.
