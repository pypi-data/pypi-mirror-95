<div align="center">
<img src="feat_img.png"/>
</div>

# Self-attention building blocks for computer vision applications in PyTorch

Implementation of self attention mechanisms for computer vision in PyTorch with einsum and einops

Focused on computer vision self-attention modules. 

Ongoing repository. pip package coming soon...

## Related articles: attention and transformers and einsum
- [How Attention works in Deep Learning](https://theaisummer.com/attention/)
- [How Transformers work in deep learning and NLP](https://theaisummer.com/transformer/)
- [How the Vision Transformer (ViT) works in 10 minutes: an image is worth 16x16 words](https://theaisummer.com/vision-transformer/)
- [Understanding einsum for Deep learning: implement a transformer with multi-head self-attention from scratch](https://theaisummer.com/einsum-attention/)


## Code Examples

#### Multi head attention

```python
import torch
from self_attention_cv import MultiHeadSelfAttention

model = MultiHeadSelfAttention(dim=64)
x = torch.rand(16, 10, 64)  # [batch, tokens, dim]
mask = torch.zeros(10, 10)  # tokens X tokens
mask[5:8, 5:8] = 1
y = model(x, mask)
```

#### Axial attention

```python
import torch
from self_attention_cv import AxialAttentionBlock
model = AxialAttentionBlock(in_channels=256, dim=64, heads=8)
x = torch.rand(1, 256, 64, 64)  # [batch, tokens, dim, dim]
y = model(x)
```

#### Vanilla Transformer Encoder
```python
import torch
from self_attention_cv import TransformerEncoder

model = TransformerEncoder(dim=64,blocks=6,heads=8)
x = torch.rand(16, 10, 64)  # [batch, tokens, dim]
mask = torch.zeros(10, 10)  # tokens X tokens
mask[5:8, 5:8] = 1
y = model(x,mask)
```

#### 1D Positional Embeddings 

```python
import torch
from self_attention_cv.pos_embeddings import AbsPosEmb1D,RelPosEmb1D

model = AbsPosEmb1D(tokens=20, dim_head=64)
# batch heads tokens dim_head
q = torch.rand(2, 3, 20, 64)
y1 = model(q)

model = RelPosEmb1D(tokens=20, dim_head=64, heads=3)
q = torch.rand(2, 3, 20, 64)
y2 = model(q)
```

#### 2D Positional Embeddings
```python
import torch
from self_attention_cv.pos_embeddings import RelPosEmb2D
dim = 32  # spatial dim of the feat map
model = RelPosEmb2D(
    feat_map_size=(dim, dim),
    dim_head=128)

q = torch.rand(2, 4, dim*dim, 128)
y = model(q)
```

#### Bottleneck Attention block 
```python
import torch
from self_attention_cv.bottleneck_transformer import BottleneckBlock
inp = torch.rand(1, 512, 32, 32)
bottleneck_block = BottleneckBlock(in_channels=512, fmap_size=(32, 32), heads=4, out_channels=1024, pooling=True)
y = bottleneck_block(inp)
```


## References

1. Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). Attention is all you need. arXiv preprint arXiv:1706.03762.
2. Wang, H., Zhu, Y., Green, B., Adam, H., Yuille, A., & Chen, L. C. (2020, August). Axial-deeplab: Stand-alone axial-attention for panoptic segmentation. In European Conference on Computer Vision (pp. 108-126). Springer, Cham.
3. Srinivas, A., Lin, T. Y., Parmar, N., Shlens, J., Abbeel, P., & Vaswani, A. (2021). Bottleneck Transformers for Visual Recognition. arXiv preprint arXiv:2101.11605.  
4. Dosovitskiy, A., Beyer, L., Kolesnikov, A., Weissenborn, D., Zhai, X., Unterthiner, T., ... & Houlsby, N. (2020). An image is worth 16x16 words: Transformers for image recognition at scale. arXiv preprint arXiv:2010.11929.


