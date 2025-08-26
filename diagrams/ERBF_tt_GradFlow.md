```mermaid
%% ERBF Parameter Update Pipeline
%% Gradient flow from SFPU accumulators → Ethernet multicast → parameter server shards
%% Green = Gradient computation, Orange = Communication, Blue = Parameter updates
graph TD
    subgraph LocalCompute["Local Gradient Computation (per chip)"]
        subgraph TensixCore["Tensix Core"]
            SFPU_Acc[(SFPU Gradient<br/>Accumulator<br/>∇Θ_local)]
            SFPU_Phi[(SFPU Attention<br/>Accumulator<br/>∇Φ_local)]
            L1_Grad[[L1 Gradient<br/>Buffer<br/>32x32 tiles]]
        end
        
        GradReduce[Local Gradient<br/>Reduce & Pack]
        EthTx[Ethernet TX<br/>E8/E9 tiles]
    end
    
    subgraph EthernetFabric["Ethernet Multicast Fabric"]
        subgraph MulticastTree["All-Reduce Tree"]
            Root[Parameter Server<br/>Root Chip 0,0]
            L1A[Intermediate<br/>Chip 0,1]
            L1B[Intermediate<br/>Chip 1,0]
            L2A[Leaf<br/>Chip 1,1]
            L2B[Leaf<br/>Chip 0,2]
            L2C[Leaf<br/>Chip 2,0]
        end
        
        AllReduce[All-Reduce<br/>∇Θ_global = Σ∇Θ_local]
        Broadcast[Parameter<br/>Broadcast<br/>Θ_new]
    end
    
    subgraph ParameterServer["Parameter Server Shards"]
        PS_Theta[(Θ Shard 0<br/>RNN parameters<br/>Chip 0,0)]
        PS_Phi[(Φ Shard 1<br/>Attention params<br/>Chip 0,1)]
        PS_Omega[(Ω Shard 2<br/>Evidence model<br/>Chip 1,0)]
        
        SGD_Theta[SGD Update<br/>Θ := Θ - α∇Θ]
        SGD_Phi[SGD Update<br/>Φ := Φ - α∇Φ]
        SGD_Omega[SGD Update<br/>Ω := Ω - α∇Ω]
    end
    
    subgraph UpdateDistribution["Updated Parameter Distribution"]
        EthRx[Ethernet RX<br/>E0/E1 tiles]
        L1_Param[[L1 Parameter<br/>Cache<br/>32x32 tiles]]
        CoreUpdate[Core Parameter<br/>Refresh]
    end
    
    %% Gradient flow
    SFPU_Acc --> L1_Grad
    SFPU_Phi --> L1_Grad
    L1_Grad --> GradReduce
    GradReduce --> EthTx
    
    %% Multicast gradient aggregation
    EthTx -->|100GbE<br/>∇Θ tiles| Root
    EthTx -->|100GbE<br/>∇Θ tiles| L1A
    EthTx -->|100GbE<br/>∇Θ tiles| L1B
    EthTx -->|100GbE<br/>∇Θ tiles| L2A
    EthTx -->|100GbE<br/>∇Θ tiles| L2B
    EthTx -->|100GbE<br/>∇Θ tiles| L2C
    
    %% All-reduce tree operations
    Root --> AllReduce
    L1A --> AllReduce
    L1B --> AllReduce
    AllReduce --> Root
    
    %% Parameter server updates
    Root -->|∇Θ_global| PS_Theta
    L1A -->|∇Φ_global| PS_Phi
    L1B -->|∇Ω_global| PS_Omega
    
    PS_Theta --> SGD_Theta
    PS_Phi --> SGD_Phi
    PS_Omega --> SGD_Omega
    
    %% Parameter broadcast back to cores
    SGD_Theta -->|Θ_new| Broadcast
    SGD_Phi -->|Φ_new| Broadcast
    SGD_Omega -->|Ω_new| Broadcast
    
    Broadcast -->|100GbE<br/>Θ,Φ,Ω tiles| EthRx
    EthRx --> L1_Param
    L1_Param --> CoreUpdate
    
    %% Pipeline timing flow
    CoreUpdate -.->|Next timestep| SFPU_Acc
    
    %% Define styles
    classDef gradient fill:#c8e6c9,stroke:#333,color:#000
    classDef communication fill:#ff9800,stroke:#333,color:#fff
    classDef parameter fill:#2196f3,stroke:#333,color:#fff
    classDef compute fill:#ffeb3b,stroke:#333,color:#000
    
    %% Apply styles
    class SFPU_Acc,SFPU_Phi,L1_Grad,GradReduce gradient
    class EthTx,Root,L1A,L1B,L2A,L2B,L2C,AllReduce,Broadcast,EthRx communication
    class PS_Theta,PS_Phi,PS_Omega,L1_Param parameter
    class SGD_Theta,SGD_Phi,SGD_Omega,CoreUpdate compute
```
A comprehensive parameter update pipeline diagram showing how ERBF gradients flow through Tenstorrent's multi-chip architecture. The pipeline shows:
Local Gradient Computation:

SFPU accumulators compute ∇Θ and ∇Φ locally on each Tensix core
Gradients are reduced and packed into 32×32 tiles for efficient transport

Ethernet Multicast Fabric:

All-reduce tree topology using 100GbE links between chips
Global gradient aggregation: ∇Θ_global = Σ∇Θ_local across all nodes
Hierarchical reduction minimizes communication overhead

Parameter Server Shards:

Distributed parameter storage across multiple chips:

Θ Shard: RNN core parameters on chip (0,0)
Φ Shard: Attention controller parameters on chip (0,1)
Ω Shard: Evidence model parameters on chip (1,0)


SGD updates applied locally: Θ := Θ - α∇Θ

Updated Parameter Distribution:

New parameters broadcast back through Ethernet fabric
L1 parameter cache updated on each core
Deterministic parameter refresh for next ERBF time-step

This pipeline enables distributed learning across the ERBF cortical network while leveraging Tenstorrent's native Ethernet mesh for efficient gradient aggregation and parameter synchronization.
