from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import torch
import torch.nn as nn

import torch.nn.functional as F
import random, math
from SidekickAI.Modules.Attention import ContentAttention

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# CONTAINS ALL RNN BASED SEQUENCE MODELS (RNN ENCODERS, RNN DECODERS, SEQ2SEQ, etc.)

# A basic wrapper around the RNN module to allow for stacked biRNN modules
class SeperatedBiRNNModule(nn.Module):
    def __init__(self, input_size, hidden_size, rnn_type, n_layers, dropout=0.):
        super().__init__()
        assert (rnn_type == nn.RNN or rnn_type == nn.LSTM or rnn_type == nn.GRU), "rnn_type must be a valid RNN type (torch.RNN, torch.LSTM, or torch.GRU)"
        self.n_layers = n_layers
        self.forward_rnn = rnn_type(input_size, hidden_size, num_layers=n_layers, dropout=0 if n_layers == 1 else dropout)
        self.backward_rnn = rnn_type(input_size, hidden_size, num_layers=n_layers, dropout=0 if n_layers == 1 else dropout)

    def forward(self, x, hidden=None):
        #X: (seq len, batch size, features) or (num directions, seq len, batch size, features)
        if len(x.shape) == 4 and x.shape[0] == 1: x.squeeze_(0)
        # Pack
        lengths = torch.IntTensor([x.shape[-3] for i in range(x.shape[-2])])
        if len(x.data.shape) == 4:
            forward_out, forward_hidden = self.forward_rnn(nn.utils.rnn.pack_padded_sequence(x[0], lengths, enforce_sorted=False))
            backward_out, backward_hidden = self.backward_rnn(nn.utils.rnn.pack_padded_sequence(x[1], lengths, enforce_sorted=False))
        else:
            forward_out, forward_hidden = self.forward_rnn(nn.utils.rnn.pack_padded_sequence(x, lengths, enforce_sorted=False))
            backward_out, backward_hidden = self.backward_rnn(nn.utils.rnn.pack_padded_sequence(torch.flip(x, dims=[0]), lengths, enforce_sorted=False))
        # Unpack
        forward_out, _ = nn.utils.rnn.pad_packed_sequence(forward_out)
        #forward_hidden, _ = nn.utils.rnn.pad_packed_sequence(forward_hidden)
        backward_out, _ = nn.utils.rnn.pad_packed_sequence(backward_out)
        #backward_hidden, _ = nn.utils.rnn.pad_packed_sequence(backward_hidden)
        return torch.stack((forward_out, backward_out), dim=0), torch.stack((forward_hidden, backward_hidden), dim=0)

class ResidualRNN(nn.Module):
    def __init__(self, hidden_size, n_layers, rnn_type, bidirectional, dropout=0, activation=F.gelu, normalization=False):
        super().__init__()
        self.n_layers = n_layers
        self.hidden_size = hidden_size
        self.dropout = dropout
        self.activation = activation
        self.normalization = normalization
        assert rnn_type == nn.LSTM or rnn_type == nn.GRU or rnn_type == nn.RNN, "RNN type not recognized! Must be either nn.RNN, nn.GRU or nn.LSTM"
        self.rnns = nn.ModuleList()
        for i in range(n_layers):
            self.rnns.append(rnn_type(input_size=hidden_size, hidden_size=hidden_size, num_layers=1, dropout=0., bidirectional=bidirectional))

    def forward(self, x, hidden=None):
        '''x: (seq len, batch size, input_size)'''
        hiddens = []
        for i in range(self.n_layers):
            x_n, current_hidden = self.rnns[i](x, hidden[i] if hidden is not None else None)
            print(x.shape)
            print(x_n.shape)
            x_n = F.dropout(x_n, self.dropout)
            x_n = self.activation(x_n)
            hiddens.append(current_hidden)
            if i == 0:
                x = torch.cat((x + x_n[:, :, :self.hidden_size], x + x_n[:, :, self.hidden_size:]), dim=-1)
            else:
                x += x_n
            if self.normalization: x = F.layer_norm(x, x.shape)
        return x, torch.stack(hiddens)

# RNN implementing adaptive computation time
class ACTRNN(nn.Module):
    def __init__(self, input_size, hidden_size, n_layers, rnn_type, max_ponder_steps, dropout=0., epsilon=0.01):
        self.max_ponder_steps = max_ponder_steps
        self.hidden_size = hidden_size
        self.epsilon = epsilon

        self.rnn = rnn_type(input_size + 1, hidden_size, n_layers)
        self.halting_gate = nn.Sequential(nn.Linear(hidden_size, hidden_size), nn.GELU(), nn.Linear(hidden_size, 1), nn.Sigmoid())

    def forward(self, x):
        # A full forward pass through the sequence
        # x: (seq len, batch size, input size)
        seq_len, batch_size, _ = x.shape

        hidden = None
        outputs = torch.zeros((seq_len, batch_size, self.hidden_size), device=device)
        for t in range(x.shape[0]):
            output, hidden = self.step(x[t], hidden)
            outputs[t] = output
        return outputs

    def step(self, timestep_x, hidden):
        # A single timestep
        # timestep_x: (batch size, input size)
        batch_size = timestep_x.shape[0]

        # Define variables
        accum_output = torch.zeros((batch_size, self.hidden_size), device=device)
        accum_hidden = torch.zeros((batch_size, self.hidden_size), device=device) if not isinstance(self.rnn, nn.LSTM) else (torch.zeros((batch_size, self.hidden_size), device=device), torch.zeros((batch_size, self.hidden_size), device=device))
        halting_total = torch.zeros(tuple([batch_size]), device=device)
        ponder_cost = torch.zeros(tuple([batch_size]), device=device)

        # Run through ponder loop
        for n in range(self.max_ponder_steps):
            running_examples = halting_total < 1 - self.epsilon # Bool tensor determining the examples still running
            ponder_cost[running_examples] = -halting_total[running_examples]

            # Run through network
            rnn_input = torch.cat([timestep_x[running_examples], torch.full((batch_size, 1), fill_value=int(n > 0), device=device)], dim=-1) # 1 for repeat inputs, 0 for novel input
            output, hidden[running_examples] = self.rnn(rnn_input, hidden[running_examples])
            halt_prob = self.halting_gate(hidden)
            p = halt_prob if n < self.max_ponder_steps - 1 else (1 - halting_total[running_examples]).unsqueeze(-1) # Multiplier in mean-field vectors
            
            # Accumulate output and hidden
            accum_output[running_examples] += output * p
            if isinstance(self.rnn, nn.LSTM):
                accum_hidden[0][running_examples] += hidden[running_examples][0] * p
                accum_hidden[1][running_examples] += hidden[running_examples][1] * p
            else: accum_hidden[running_examples] += hidden[running_examples] * p
            # Accumulate halting total
            halting_total[running_examples] += p

            # Break if no examples are still running
            if not (halting_total < 1 - self.epsilon).any(): break
        
        return accum_output, accum_hidden, ponder_cost

# RNN-Based bidirectional encoder that takes entire sequence at once and returns output sequence along with final hidden state
class EncoderRNN(nn.Module):
    def __init__(self, input_size, hidden_size, n_layers, rnn_type, bidirectional=True, layernorm=True, dropout=0.):
        super().__init__()
        assert (rnn_type == nn.RNN or rnn_type == nn.LSTM or rnn_type == nn.GRU), "rnn_type must be a valid RNN type (torch.RNN, torch.LSTM, or torch.GRU)"
        self.n_layers = n_layers
        self.hidden_size = hidden_size
        self.rnn_type = rnn_type
        self.bidirectional = bidirectional
        self.input_transform = nn.Linear(input_size, hidden_size) if input_size != hidden_size else None

        # Construct the RNN
        #self.rnn = ResidualRNN(hidden_size=hidden_size, n_layers=n_layers, dropout=(0 if n_layers == 1 else dropout), bidirectional=bidirectional, rnn_type=rnn_type, normalization=layernorm)
        self.rnn = rnn_type(input_size=hidden_size, hidden_size=hidden_size, num_layers=n_layers, dropout=(0 if n_layers == 1 else dropout), bidirectional=bidirectional)

    def forward(self, inputs, lengths=None, hidden=None): # Takes the entire input sequence at once
        # inputs: (seq_len, batch_size, input_size)
        batch_size = inputs.shape[1]
        seq_len = inputs.shape[0]

        if self.input_transform is not None: inputs = self.input_transform(inputs)

        # Pack and use lengths if provided
        if lengths is not None:
            inputs = nn.utils.rnn.pack_padded_sequence(inputs, lengths, enforce_sorted=False)
        else:
            inputs = nn.utils.rnn.pack_padded_sequence(inputs, torch.LongTensor([seq_len for i in range(batch_size)]), enforce_sorted=False)
        # Push through RNN layer
        outputs, hidden = self.rnn(inputs, hidden) # the hidden state defaults to zero when not provided
        # Unpack
        outputs, _ =  nn.utils.rnn.pad_packed_sequence(outputs)

        # Select hidden state if using LSTM
        if self.rnn_type == nn.LSTM: hidden = hidden[0]
        if self.bidirectional:
            # Concat bidirectional hidden states
            hidden = hidden.view(self.n_layers, 2, batch_size, self.hidden_size)
            hidden = torch.cat((hidden[:, 0], hidden[:, 1]), dim=-1)
            # Concat bidirectional outputs
            outputs = outputs.view(seq_len, batch_size, 2, self.hidden_size)
            outputs = torch.cat((outputs[:, :, 0], outputs[:, :, 1]), dim=-1)

        return outputs, hidden

class PyramidEncoderRNN(nn.Module): # MAY NEED TO FIX SHAPES
    def __init__(self, input_size, n_layers, rnn_type, dropout=0.):
        super().__init__()
        assert (rnn_type == nn.RNN or rnn_type == nn.LSTM or rnn_type == nn.GRU), "rnn_type must be a valid RNN type (torch.RNN, torch.LSTM, or torch.GRU)"
        self.input_size = input_size
        self.n_layers = n_layers
        self.dropout = dropout
        self.rnn_type = rnn_type
        self.pad_vector = torch.nn.Parameter(torch.randn((1, 1, input_size), requires_grad=True))

        self.rnns = nn.ModuleList([SeperatedBiRNNModule(input_size=int(input_size * math.pow(2., float(i))), hidden_size=int(input_size * math.pow(2., float(i))), n_layers=1, rnn_type=rnn_type) for i in range(1, n_layers + 1)])

    def forward(self, input_seq, lengths=None, hidden=None):
        '''inputs: \n
            input_seq: (seq_len, batch_size, input_dim)
            lengths: (batch size)
            hidden: 
        outputs:
            seq: (seq_len / 2 ^ n_layers + 1, batch size, input_dim * 2 ^ n_layers + 1)
            hidden: None'''
        seq_len, batch_size, features = input_seq.shape
        
        # Pack if lengths are provided
        if lengths is not None: input_seq = nn.utils.rnn.pack_padded_sequence(input_seq, lengths, enforce_sorted=False)

        # Pad to ensure input_seq.shape[0] is divisible by 2^(n_layers - 1)
        if input_seq.shape[0] % math.pow(2, self.n_layers) != 0: input_seq = torch.cat((input_seq, self.pad_vector.repeat(int(math.pow(2, self.n_layers) - (input_seq.shape[0] % math.pow(2, self.n_layers))), batch_size, 1)), dim=0)

        # Feed through rnn layers
        for i in range(len(self.rnns)):
            # Concat neighbors
            input_seq = input_seq.transpose(1, 2) if i > 0 else input_seq.transpose(0, 1) # Reshape messes up if batch dim does not come first
            input_seq = input_seq.contiguous().reshape(2, batch_size, int(input_seq.shape[2] / 2), int(input_seq.shape[3] * 2)) if i > 0 else input_seq.contiguous().reshape(batch_size, int(input_seq.shape[1] / 2), int(input_seq.shape[2] * 2))
            input_seq = input_seq.transpose(1, 2) if i > 0 else input_seq.transpose(0, 1)
            # Feed through layer
            input_seq, hidden = self.rnns[i](input_seq)
            # Dropout
            if i != self.n_layers - 1: F.dropout(input_seq, self.dropout)
        # Concat final hiddens
        hidden = hidden.transpose(0, 1)
        hidden = torch.cat((hidden[:, 0], hidden[:, 1]), dim=-1)[-1]
        # Concat final outputs
        input_seq = torch.cat((input_seq[0], input_seq[1]), dim=-1)

        # return input_seq, hidden
        return input_seq, None

# Decoder based RNN using Luong Attention
class DecoderRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, use_attention=True, rnn_type=nn.GRU, n_layers=1, dropout=0.1):
        super().__init__()

        # Keep for reference
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.n_layers = n_layers
        self.dropout = dropout
        self.use_attention = use_attention

        # Define layers
        self.rnn = rnn_type(input_size, hidden_size, n_layers, dropout=(0 if n_layers == 1 else dropout))
        if use_attention: 
            self.concat = nn.Linear(hidden_size * 2, hidden_size)
            self.attn = ContentAttention(hidden_size, hidden_size)
        self.out = nn.Linear(hidden_size, output_size)

    def forward(self, input_step, last_hidden, encoder_outputs=None):
        # Note: we run this one step at a time
        # input_step: (batch size, hidden dim)
        input_step.unsqueeze_(0)
        # Pack
        input_step = nn.utils.rnn.pack_padded_sequence(input_step, torch.LongTensor([1 for i in range(input_step.shape[1])]), enforce_sorted=False)
        # Forward through unidirectional GRU
        rnn_output, hidden = self.rnn(input_step, last_hidden)
        rnn_output, _ = nn.utils.rnn.pad_packed_sequence(rnn_output)
        output = rnn_output.squeeze(0)

        if self.use_attention:
            # Calculate context vector from the current GRU output
            context = self.attn(rnn_output.squeeze(0), encoder_outputs.transpose(0, 1), return_weighted_sum=True)
            # Concatenate weighted context vector and GRU output using Luong eq. 5
            concat_input = torch.cat((rnn_output.squeeze(0), context), 1)
            output = torch.tanh(self.concat(concat_input))
        # Predict next word
        output = F.softmax(self.out(output), dim=-1)

        return output, hidden

class Seq2SeqRNN(nn.Module):
    '''A Seq2Seq RNN which embeds inputs and outputs distributions over the output vocab\n
    Init Inputs:
        inpur_size (int): The size of embeddings / inputs to the network
        hidden_size (int): The RNN hidden size
        target_vocab (vocab): The target vocab
        encoder_layers (int): The number of layers in the transformer encoder
        decoder_layers (int): The number of layers in the transformer decoder
        input_vocab (vocab) [Default: None]: The input vocab, if none, then inputs are already expected as vectors
        dropout (float) [Default: 0.1]: The amount of dropout
        teacher_forcing_ratio (float): The percentage of the time to use teacher forcing
        max_len (int) [Default: 200]: The max target length used when a target is not provided
        device (torch.device): The device that the network will run on
    Inputs:
        src (Tensor): The input sequence of shape (src length, batch size)
        trg (Tensor) [default=None]: The target sequence of shape (trg length, batch size)
    Returns:
        output (Tensor): The return sequence of shape (target length, batch size, target tokens)'''
    def __init__(self, input_size, hidden_size, target_vocab, encoder_layers, decoder_layers, input_vocab=None, use_attention=True, dropout=0., rnn_type=nn.GRU, teacher_forcing_ratio=1., max_length=200, device=torch.device("cuda" if torch.cuda.is_available() else "cpu")):
        super().__init__()
        self.hyperparameters = locals()
        self.device = device
        self.output_embedding = nn.Embedding(target_vocab.num_words, hidden_size)
        if input_vocab is not None: self.input_embedding = nn.Embedding(input_vocab.num_words, input_size) if input_vocab != target_vocab else self.output_embedding # If input and output vocabs are the same, reuse embeddings
        self.encoder = EncoderRNN(input_size=hidden_size, hidden_size=hidden_size, n_layers=encoder_layers, rnn_type=rnn_type, dropout=dropout)
        self.decoder = DecoderRNN(input_size=hidden_size, hidden_size=hidden_size * 2, output_size=target_vocab.num_words, use_attention=use_attention, rnn_type=rnn_type, n_layers=decoder_layers, dropout=dropout)
        self.input_vocab, self.target_vocab = input_vocab, target_vocab
        self.max_length = max_length
        self.hidden_dropout = nn.Dropout(dropout)
        self.teacher_forcing_ratio = teacher_forcing_ratio
        self.convert_input = nn.Linear(input_size, hidden_size) if input_size != hidden_size and input_vocab != target_vocab else None
    
    def forward(self, input_seq, target_seq=None):
        # Ensure there is no SOS_token at the start of the input seq or target seq
        if self.input_vocab is not None and input_seq[0, 0].item() == self.input_vocab.SOS_token: input_seq = input_seq[1:]
        if target_seq is not None and target_seq[0, 0].item() == self.target_vocab.SOS_token: target_seq = target_seq[1:]
        # Warn if there is no EOS token at the end of the target
        if target_seq is not None and not (target_seq[-1] == self.target_vocab.EOS_token).any(): print("Warning: There is no EOS token at the end of the target passed to the model!")

        input_lengths = torch.IntTensor([len(input_seq[:, i][(input_seq[:, i] != self.input_vocab.PAD_token)]) for i in range(input_seq.shape[1])]) if self.input_vocab is not None else torch.IntTensor([len(input_seq) for i in range(input_seq.shape[1])])
        if self.input_vocab is not None: input_seq = self.input_embedding(input_seq)
        if self.convert_input is not None: input_seq = self.convert_input(input_seq)
        encoder_outputs, encoder_hidden = self.encoder(input_seq, input_lengths)
        # Create initial decoder input (start with SOS tokens for each sentence)
        decoder_input = torch.LongTensor([self.target_vocab.SOS_token for _ in range(input_seq.shape[1])])
        decoder_input = decoder_input.to(self.device)

        # Set initial decoder hidden state to the encoder's final hidden state
        decoder_hidden = self.hidden_dropout(encoder_hidden[:self.decoder.n_layers])

        # Forward batch of sequences through decoder one time step at a time
        final_outputs = torch.empty((target_seq.shape[0], target_seq.shape[1], self.target_vocab.num_words), device=self.device) if target_seq is not None else torch.empty((self.max_length, input_seq.shape[1], self.target_vocab.num_words), device=self.device)
        for t in range(target_seq.shape[0] if target_seq is not None else self.max_length):
            decoder_output, decoder_hidden = self.decoder(self.output_embedding(decoder_input), decoder_hidden, encoder_outputs)
            final_outputs[t] = decoder_output
            # Teacher forcing / Autoregressive
            decoder_input = target_seq[t].view(-1) if random.random() < self.teacher_forcing_ratio and target_seq is not None else torch.argmax(decoder_output, dim=-1).view(-1)
            if target_seq is None and torch.argmax(decoder_output, dim=-1)[0].item() == self.target_vocab.EOS_token: return final_outputs[:t+1]

        return final_outputs