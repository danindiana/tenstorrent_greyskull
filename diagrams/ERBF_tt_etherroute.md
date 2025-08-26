```mermaid
%% ERBF Multi-Chip Mesh (Ethernet routing view)
%% Each chip hosts one cortical node n
%% Relational edges hop through 2-D NoC + 100 GbE links
%% Green = ERBF cortical nodes, Yellow = Tensix cores, Grey = memory/routing
graph TD
    subgraph HostSystem["Host System"]
        Host[Host CPU]
        DRAM[(Host DRAM<br/>State Ring Buffer)]
    end
    
    subgraph Rack["Rack Topology (x,y coordinates)"]
        subgraph Chip00["Chip (0,0)"]
            N1[ERBF Node V1]
            T00_E8[E8: 100GbE]
            T00_E9[E9: 100GbE]
            T00_Core[72 Tensix Cores<br/>FlashAttention]
        end
        
        subgraph Chip01["Chip (0,1)"]
            N2[ERBF Node LM]
            T01_E0[E0: 100GbE]
            T01_E1[E1: 100GbE]
            T01_Core[72 Tensix Cores<br/>FlashAttention]
        end
        
        subgraph Chip10["Chip (1,0)"]
            N3[ERBF Node MT]
            T10_E6[E6: 100GbE]
            T10_E7[E7: 100GbE]
            T10_Core[72 Tensix Cores<br/>FlashAttention]
        end
        
        subgraph Chip11["Chip (1,1)"]
            N4[ERBF Node IT]
            T11_E14[E14: 100GbE]
            T11_E15[E15: 100GbE]
            T11_Core[72 Tensix Cores<br/>FlashAttention]
        end
    end
    
    %% Host to Chips (PCIe + DMA)
    Host -->|PCIe + DMA<br/>Θ,Φ,Stim| Chip00
    Host -->|Ethernet<br/>Θ,Φ,Stim| Chip01
    Host -->|Ethernet<br/>Θ,Φ,Stim| Chip10
    Host -->|Ethernet<br/>Θ,Φ,Stim| Chip11
    
    %% Inter-chip Ethernet (Relational edges E)
    T00_E8 <==>|Rel Edge<br/>State tiles| T01_E0
    T00_E9 <==>|Rel Edge<br/>State tiles| T10_E6
    T01_E1 <==>|Rel Edge<br/>State tiles| T11_E14
    T10_E7 <==>|Rel Edge<br/>State tiles| T11_E15
    
    %% Intra-chip NoC (Core to Ethernet tiles)
    T00_Core -.->|32×32 tiles<br/>NoC| T00_E8
    T00_Core -.->|32×32 tiles<br/>NoC| T00_E9
    T01_Core -.->|32×32 tiles<br/>NoC| T01_E0
    T01_Core -.->|32×32 tiles<br/>NoC| T01_E1
    T10_Core -.->|32×32 tiles<br/>NoC| T10_E6
    T10_Core -.->|32×32 tiles<br/>NoC| T10_E7
    T11_Core -.->|32×32 tiles<br/>NoC| T11_E14
    T11_Core -.->|32×32 tiles<br/>NoC| T11_E15
    
    %% State collection back to host
    Chip00 -->|State n,t+1| DRAM
    Chip01 -->|State n,t+1| DRAM
    Chip10 -->|State n,t+1| DRAM
    Chip11 -->|State n,t+1| DRAM
    
    %% Define styles
    classDef erbf fill:#c8e6c9,stroke:#333,color:#000
    classDef tensix fill:#ffeb3b,stroke:#333,color:#000
    classDef ethernet fill:#ff9800,stroke:#333,color:#fff
    classDef memory fill:#9e9e9e,stroke:#333,color:#fff
    
    %% Apply styles
    class N1,N2,N3,N4 erbf
    class T00_Core,T01_Core,T10_Core,T11_Core tensix
    class T00_E8,T00_E9,T01_E0,T01_E1,T10_E6,T10_E7,T11_E14,T11_E15 ethernet
    class Host,DRAM memory
```

Here are the key design decisions:
Physical Topology Mapping:

Each ERBF cortical node (V1, LM, MT, IT) maps to one Wormhole chip at coordinates (x,y)
Each chip has multiple Ethernet tiles (E0-E15) that can manage 100Gb ethernet Community Highlight: Tenstorrent Wormhole Series Part 1: Physicalities | Tenstorrent
Chips are connected in a 2D mesh through integrated ethernet ports Tenstorrent Wormhole Analysis – A Scale Out Architecture for Machine Learning That Could Put Nvidia On Their Back Foot

ERBF Relational Edge Routing:

Relational edges E ⊆ N × N become physical Ethernet links between chips
E8/E9 tiles on one chip connect to E0/E1 tiles on adjacent chips Community Highlight: Tenstorrent Wormhole Series Part 1: Physicalities | Tenstorrent
State tiles (32×32) flow over these 100GbE links during edge gating and recurrent updates

Data Flow:

Host injects parameters Θ, Φ and stimuli via PCIe/Ethernet
Each chip runs FlashAttention kernels on its 72 Tensix cores
Intra-chip NoC routes 32×32 tiles between cores and Ethernet tiles
State(n,t+1) flows back to host DRAM ring buffer

This mapping allows the ERBF algorithm's distributed cortical computation to leverage Tenstorrent's seamless scale-out capabilities where software sees an infinite mesh of cores without strict hierarchies
