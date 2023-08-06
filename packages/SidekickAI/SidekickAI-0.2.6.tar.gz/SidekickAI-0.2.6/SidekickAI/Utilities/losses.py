import torch
import torch.nn.functional as F

def mask_nll_loss(output, target, mask, device):
    if len(output.shape) == 2: # Ensure there is a sequence length dimension
        output.unsqueeze_(0)
        target.unsqueeze_(0)
        mask.unsqueeze_(0)
    total_print_loss, mask_totals, loss = 0, 0, 0
    for t in range(len(output)):
        mask_total = mask[t].sum()
        cross_entropy = -torch.log(torch.gather(output[t], 1, target[t].view(-1, 1)).squeeze(1))
        if not mask[t].any(): continue
        mask_loss = cross_entropy.masked_select(mask[t]).mean().to(device)
        loss += mask_loss
        total_print_loss += mask_loss.item() * mask_total.item()
        mask_totals += mask_total.item()
        
    if mask_totals > 0: return loss, total_print_loss / mask_totals
    else: return loss, total_print_loss

def nll_loss(output, target):
    # output: (seq len, batch size, dist size)
    # target: (seq len, batch size)
    loss = 0
    for t in range(len(output)):
        loss += F.cross_entropy(output[t], target[t])
    return loss