"""SeqSleepNet-class PyTorch adaptation for protocol-v2 scaffolding.

Input is log-power spectrogram [B, L, 2, 129, 29]. This module is not
scientific execution; it supports synthetic shape and configuration tests.
"""
from __future__ import annotations
import numpy as np
import torch
from torch import Tensor, nn

def linear_tri_filterbank(freq_bins=129, filters=32, samplerate=100, nfft=256, lowfreq=0, highfreq=50):
    hz=np.linspace(lowfreq,highfreq,filters+2); bins=np.floor((nfft+1)*hz/samplerate)
    fb=np.zeros((filters,nfft//2+1),dtype=np.float32)
    for j in range(filters):
        for i in range(int(bins[j]),int(bins[j+1])): fb[j,i]=(i-bins[j])/(bins[j+1]-bins[j])
        for i in range(int(bins[j+1]),int(bins[j+2])): fb[j,i]=(bins[j+2]-i)/(bins[j+2]-bins[j+1])
    return fb.T

class SeqSleepNetClass(nn.Module):
    model_id='SEQSLEEPNET_CLASS_L20_V1'
    def __init__(self, sequence_length=20, channels=2, freq_bins=129, frames=29, filters=32, classes=5, dropout=0.25):
        super().__init__(); self.sequence_length=sequence_length; self.channels=channels; self.freq_bins=freq_bins; self.frames=frames
        self.register_buffer('triangular_support',torch.from_numpy(linear_tri_filterbank(freq_bins,filters)))
        self.filterbank=nn.Parameter(torch.zeros(channels,freq_bins,filters))
        self.epoch_gru=nn.GRU(filters*channels,64,batch_first=True,bidirectional=True)
        self.epoch_projection=nn.Linear(128,64)
        self.epoch_attention=nn.Linear(64,1)
        self.sequence_gru=nn.GRU(64,64,batch_first=True,bidirectional=True)
        self.dropout=nn.Dropout(dropout); self.classifier=nn.Linear(128,classes)
        nn.init.normal_(self.filterbank,mean=0.,std=0.02)
    def forward(self, x:Tensor, modality_mask:Tensor):
        if x.ndim!=5 or x.shape[2:]!=(2,129,29): raise ValueError('x must have shape [B,20,2,129,29]')
        if x.shape[1]!=self.sequence_length: raise ValueError('unexpected sequence length')
        mask=torch.as_tensor(modality_mask,device=x.device,dtype=x.dtype)
        if mask.ndim==1: mask=mask.unsqueeze(0).expand(x.shape[0],-1)
        if mask.shape!=(x.shape[0],2) or torch.any((mask<0)|(mask>1)) or torch.any(mask.sum(1)==0): raise ValueError('invalid modality mask')
        support=self.triangular_support.to(dtype=x.dtype)
        eff=torch.sigmoid(self.filterbank)*support.unsqueeze(0)
        # B,L,C,F,T -> B,L,C,M,T
        z=torch.einsum('blcft,cfm->blcmt',x,eff)*mask[:,None,:,None,None]
        z=z.permute(0,1,4,2,3).reshape(x.shape[0]*x.shape[1],29,64)
        h,_=self.epoch_gru(self.dropout(z)); h=self.dropout(torch.relu(self.epoch_projection(h)))
        a=torch.softmax(self.epoch_attention(h).squeeze(-1),dim=1).unsqueeze(-1); epoch=(a*h).sum(1)
        seq=epoch.reshape(x.shape[0],x.shape[1],64); out,_=self.sequence_gru(self.dropout(seq)); return self.classifier(self.dropout(out))

def count_trainable_parameters(model): return sum(p.numel() for p in model.parameters() if p.requires_grad)
