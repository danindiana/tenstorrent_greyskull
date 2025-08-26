```mermaid
%%{init: {'theme': 'dark'}}%%
flowchart LR
    Rel["Rel(t)\nContext"] --> Attn["Φ\nAttention"]
    Attn --> Gate["σ\nEdge Gating\nW(e,t)"]
    Gate --> N["N\nCortical Net"]
    Stim["Stim(t)\nStimulus"] --> N

    subgraph Update["Recurrent Update"]
        N --> V1["V1"]
        N --> LM["LM"]
        N --> n3["n₃"]
        N --> n4["n₄"]
    end

    V1 --> Omega["Ω\nEvidence Model"]
    LM --> Omega
    n3 --> Omega
    n4 --> Omega

    Omega --> Post["B(t+1)\nBeliefs"]
    Post --> Obj["Min KL[Q_t||P(⋅)]"]
    Post --> Rel

    classDef box fill:#1e1e1e,stroke:#555,color:#fff;
    classDef comp fill:#26a69a,stroke:#fff,color:#fff;
    class Rel,Stim,Attn,Post,Obj,Omega box
    class Gate,N,V1,LM,n3,n4 comp
```
```mermaid
%%{init: {'theme': 'dark'}}%%
classDiagram
    direction LR

    class RelationalContext {
      +Rel(t)
      +update(B(t+1))
    }
    class Stimulus {
      +Stim(t)
      +broadcast()
    }
    class AttentionController {
      +Φ
      +compute_a(t)
    }
    class EdgeGating {
      +σ
      +apply_W(e,t)
    }
    class CorticalNode {
      <<Abstract>>
      +RNN_Θ
      +update()
      +get_state()
    }
    class V1 {
      +visual_features
    }
    class LM {
      +language_memory
    }
    class IntegratingNode {
      +integration
    }
    class EvidenceModel {
      +Ω
      +P(cause | S_N; Rel)
      +compute_posterior()
    }
    class BeliefUpdater {
      +B(t+1)
      +minimize_KL()
    }

    RelationalContext --> AttentionController
    Stimulus --> CorticalNode
    AttentionController --> EdgeGating
    EdgeGating --> CorticalNode
    CorticalNode <|-- V1
    CorticalNode <|-- LM
    CorticalNode <|-- IntegratingNode
    CorticalNode --> EvidenceModel
    EvidenceModel --> BeliefUpdater
    BeliefUpdater --> RelationalContext
```
```mermaid
%%{init: {'theme': 'dark'}}%%
stateDiagram-v2
    [*] --> ContextInjected
    ContextInjected --> AttentionModulated
    AttentionModulated --> EdgesGated
    EdgesGated --> NodesUpdated
    NodesUpdated --> EvidenceComputed
    EvidenceComputed --> BeliefsFormed
    BeliefsFormed --> FeedbackApplied
    FeedbackApplied --> ContextInjected

    note right of NodesUpdated
        V1, LM, n₃, n₄ update
        using Stim(t) and
        W(e,t)-gated inputs
    end note

    note right of EvidenceComputed
        Ω computes P(cause | S_N; Rel)
        from current states
    end note

    BeliefsFormed --> ObjectiveMet
    ObjectiveMet --> [*]

    %% Correct styling syntax for state diagrams
    style ContextInjected fill:#4fc3f7,stroke:#fff,color:#000
    style NodesUpdated fill:#4fc3f7,stroke:#fff,color:#000
    style EvidenceComputed fill:#4fc3f7,stroke:#fff,color:#000
    style BeliefsFormed fill:#4fc3f7,stroke:#fff,color:#000
```
```mermaid
%%{init: {'theme': 'dark', 'themeVariables': {
  'actorBgColor': '#1f2937',
  'actorBorderColor': '#38bdf8',
  'textColor': '#f1f5f9',
  'noteBorderColor': '#64748b',
  'noteTextColor': '#f1f5f9',
  'messageColor': '#f1f5f9'
}}}%%
sequenceDiagram
    participant Rel
    participant Attn as Attention Φ
    participant Gate as Gating σ
    participant N as Cortical Network N
    participant Omega as Evidence Ω
    participant Post as Beliefs B(t+1)
    participant Obj as Objective

    Note over Rel,Post: Inference Step t

    Rel->>Attn: Rel(t)
    Attn->>Gate: a(t)
    Gate->>N: W(e,t) [gated edges]
    N->>N: Stim(t) → V1, LM, n₃, n₄
    N->>N: Weighted internal updates
    N->>Omega: S_N(t) [node states]
    
    %% SIMPLIFIED LINE TO AVOID PARSER BUG
    Omega->>Post: Compute Posterior Probability
    
    %% SIMPLIFIED LINE TO AVOID PARSER BUG
    Post->>Obj: Minimize KL Divergence
    
    Post->>Rel: B(t+1) → Rel(t+1)

    Note over Rel,Post: Cycle repeats at t+1
```
```mermaid
%%{init: {'theme': 'dark'}}%%
graph TD
    subgraph " "
        direction LR
        subgraph " "
            direction TB
            subgraph " "
                Rel["Relational Context<br><span class='subtitle'>The Guiding Past</span>"]:::inputStyle
            end
            subgraph " "
                Stim["External Stimulus<br><span class='subtitle'>The Sensory Present</span>"]:::inputStyle
            end
        end

        subgraph " "
            direction TB
            subgraph "Cognitive Core"
                direction LR
                Attn["Φ<br><span class='subtitle'>Attention</span>"]:::controlStyle
                Gate["σ<br><span class='subtitle'>Gating</span>"]:::controlStyle
            end

            subgraph "Cortical Network"
                subgraph " "
                    V1["V1"]:::nodeStyle
                    LM["LM"]:::nodeStyle
                end
                subgraph " "
                    N3["n₃"]:::nodeStyle
                    N4["n₄"]:::nodeStyle
                end
            end
        end

        subgraph " "
            direction TB
            subgraph "Emergent Understanding"
                Omega["Ω<br><span class='subtitle'>Evidence & Causality</span>"]:::outputStyle
                Post["B(t+1)<br><span class='subtitle'>Formed Beliefs</span>"]:::outputStyle
            end
            subgraph " "
                Obj["<span class='obj'>Objective: Minimize Divergence</span><br><span class='subtitle'>The Drive to Learn</span>"]:::objStyle
            end
        end
    end

    %% Define connections with pathway styles
    Rel -- "Guides" --> Attn
    Stim -- "Drives" --> V1 & LM & N3 & N4
    Attn -- "Focus" --> Gate
    Gate -- "Modulates" --> V1 & LM & N3 & N4
    V1 & LM & N3 & N4 -- "Internal State" --> Omega
    Omega -- "Inference" --> Post
    Post -- "Learning Signal" --> Obj
    Post -.->|"Becomes Context"| Rel

    %% Define CSS-like styles for enhanced dark mode visibility
    classDef inputStyle fill:#075985,stroke:#38bdf8,stroke-width:2px,color:#e0f2fe,font-family:Inter,sans-serif
    classDef controlStyle fill:#581c87,stroke:#a855f7,stroke-width:2px,color:#f3e8ff,font-family:Inter,sans-serif
    classDef nodeStyle fill:#14532d,stroke:#4ade80,stroke-width:3px,color:#dcfce7,font-family:Inter,sans-serif,font-weight:bold
    classDef outputStyle fill:#881337,stroke:#f43f5e,stroke-width:2px,color:#fff1f2,font-family:Inter,sans-serif
    classDef objStyle fill:#111827,stroke:#f59e0b,stroke-width:2px,color:#fef3c7,font-family:Inter,sans-serif

    %% Style the connection lines
    linkStyle default stroke:#9ca3af,stroke-width:1.5px
    linkStyle 7 stroke:#f59e0b,stroke-width:2px,stroke-dasharray:5 5
    
    %% Subgraph styling to create invisible containers for layout
    style 0 fill:transparent,stroke:transparent
    style 1 fill:transparent,stroke:transparent
    style 2 fill:transparent,stroke:transparent
    style 3 fill:transparent,stroke:transparent
    style 4 fill:transparent,stroke:transparent
    style 5 fill:transparent,stroke:transparent
    style 6 fill:transparent,stroke:transparent
    style 7 fill:transparent,stroke:transparent
    style 8 fill:transparent,stroke:transparent
    style 9 fill:transparent,stroke:transparent
    style 10 fill:transparent,stroke:transparent
    style 11 fill:transparent,stroke:transparent
```
