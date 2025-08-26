```mermaid
%% ERBF L1 SRAM Footprint per Tensix Core
%% Block diagram showing circular buffer allocation for one ERBF node
%% Green = ERBF data buffers, Yellow = compute scratch, Grey = system reserved
graph TD
    subgraph TensixL1["Tensix Core L1 SRAM (1.5MB total)"]
        
        subgraph ERBFBuffers["ERBF Circular Buffers"]
            CB_Q[(CB_Q<br/>Recurrent State<br/>Q n,t<br/>256KB)]
            CB_K[(CB_K<br/>Relational Edges<br/>K src→n,t<br/>256KB)]
            CB_V[(CB_V<br/>Context Vector<br/>V n,t<br/>256KB)]
            CB_O[(CB_O<br/>Output State<br/>O n,t+1<br/>256KB)]
            CB_Attn[(CB_Attn<br/>Attention Gates<br/>W e,t<br/>128KB)]
        end
        
        subgraph ComputeScratch["Compute Scratch Space"]
            Scratch_MM[[MatMul Intermediate<br/>QK^T tiles<br/>128KB]]
            Scratch_SM[[Softmax Working<br/>exp & sum buffers<br/>64KB]]
            Scratch_FA[[FlashAttention<br/>Accumulator<br/>64KB]]
        end
        
        subgraph SystemReserved["System Reserved"]
            FW_Stack[[Firmware Stack<br/>32KB]]
            DMA_Desc[[DMA Descriptors<br/>16KB]]
            Router_Buf[[NoC Router Buffer<br/>16KB]]
        end
        
    end
    
    subgraph DataFlow["Data Movement"]
        DRAM_In[Host DRAM<br/>Input Tiles]
        DRAM_Out[Host DRAM<br/>Output Tiles]
        NoC_In[NoC Ingress<br/>from other cores]
        NoC_Out[NoC Egress<br/>to other cores]
        Eth_In[Ethernet Ingress<br/>from other chips]
        Eth_Out[Ethernet Egress<br/>to other chips]
    end
    
    %% Input data flow
    DRAM_In -->|DMA Q,K,V tiles| CB_Q
    DRAM_In -->|DMA Q,K,V tiles| CB_K
    DRAM_In -->|DMA Q,K,V tiles| CB_V
    Eth_In -->|Remote State tiles| CB_K
    NoC_In -->|Neighbor tiles| CB_V
    
    %% Compute flow within L1
    CB_Q -->|32x32 tiles| Scratch_MM
    CB_K -->|32x32 tiles| Scratch_MM
    Scratch_MM -->|QK^T result| Scratch_SM
    Scratch_SM -->|Attention weights| CB_Attn
    CB_Attn -->|Gated weights| Scratch_FA
    CB_V -->|Value tiles| Scratch_FA
    Scratch_FA -->|Accumulated output| CB_O
    
    %% Output data flow
    CB_O -->|DMA State n,t+1| DRAM_Out
    CB_O -->|Broadcast state| NoC_Out
    CB_O -->|Relational state| Eth_Out
    
    %% Memory allocation annotations
    CB_Q -.->|Total ERBF buffers<br/>1.16MB / 1.5MB| CB_O
    Scratch_MM -.->|Compute scratch<br/>256KB / 1.5MB| Scratch_FA
    FW_Stack -.->|System overhead<br/>64KB / 1.5MB| Router_Buf
    
    %% Define styles
    classDef erbf fill:#c8e6c9,stroke:#333,color:#000
    classDef compute fill:#ffeb3b,stroke:#333,color:#000
    classDef system fill:#9e9e9e,stroke:#333,color:#fff
    classDef flow fill:#e3f2fd,stroke:#1976d2,color:#000
    
    %% Apply styles
    class CB_Q,CB_K,CB_V,CB_O,CB_Attn erbf
    class Scratch_MM,Scratch_SM,Scratch_FA compute
    class FW_Stack,DMA_Desc,Router_Buf system
    class DRAM_In,DRAM_Out,NoC_In,NoC_Out,Eth_In,Eth_Out flow
```
ERBF Circular Buffers (1.16MB):

CB_Q: Recurrent state Q(n,t) - 256KB for current node state
CB_K: Relational edges K(src→n,t) - 256KB for incoming edge data
CB_V: Context vector V(n,t) - 256KB for local context
CB_O: Output state O(n,t+1) - 256KB for next state computation
CB_Attn: Attention gates W(e,t) - 128KB for edge gating weights

Compute Scratch Space (256KB):

MatMul Intermediate: For QK^T computations in attention
Softmax Working: Exp and sum buffers for attention normalization
FlashAttention Accumulator: For efficient attention computation

System Reserved (64KB):

Firmware stack, DMA descriptors, and NoC router buffers

The diagram maps directly to your ERBF operational semantics:

Context injection uses CB_Attn for attention weights
Edge gating applies σ(a[e]) using the attention buffers
Recurrent update flows through CB_Q → compute scratch → CB_O
Belief update aggregates states from CB_O back to host

This efficiently utilizes the 1.5MB L1 SRAM per Tensix core while supporting the distributed cortical computation pattern of ERBF.
