# Sidekick Batching v1.0
import itertools, random, re
from torch import LongTensor, BoolTensor, Tensor
import SidekickAI.Data.tokenization
# This file holds functions to convert sentence pair batches to structured tensors to feed into models

def pad_mask(input_batch, pad_value):
    '''Makes binary (0, 1) matrix for batch depending on if token is padding (0 if so, 1 if not)'''
    m = []
    for i, seq in enumerate(input_batch):
        m.append([])
        for token in seq:
            if token != pad_value:
                m[i].append(0)
            else:
                m[i].append(1)
    return m

def pad_batch(batch: list, pad_value: str) -> list:
    '''Pads all inputs to longest input'''
    return list(itertools.zip_longest(*batch, fillvalue=pad_value))

# Makes batches from a raw list of examples
#def batch(dataset):

# Returns padded sequence tensor, lengths, and pad mask
def batch_to_train_data(indexes_batch: list, PAD_token: str, return_lengths:bool =False, return_pad_mask:bool =False):
    '''
    Returns training data for a given batch.
        Inputs:
            indexes_batch (list): A list of lists of token indexes
            PAD_token (int): An index of the pad token
            *return_lengths (bool): Whether or not to return the lengths of the unpadded sequences [default: False]
            *return_pad_mask (bool): Whether or not to return a pad mask over all the padding [default: False]

        Returns:
            output_tensor (tensor: (seq len, batch size)): The padded tensor to input to the model
            *lengths (tensor: (batch size)): A tensor specifying the actual lengths of each sequence without padding
            *mask (tensor: (batch size, seq len)): A binary tensor specifying if the current position is a pad token or not
    '''
    # Pad inputs to longest length
    padList = pad_batch(indexes_batch, pad_value=PAD_token)
    padVar = LongTensor(padList)
    return_list = [padVar]
    if return_lengths:
        # Get lengths of each sentence in batch
        return_list.append(Tensor([len(indexes) for indexes in indexes_batch]))
    if return_pad_mask:
        # Get mask over all the pad tokens
        return_list.append(BoolTensor(pad_mask(padList, pad_value=PAD_token)))
    return tuple(return_list) if len(return_list) > 1 else return_list[0]

def filter_by_length(*lists, max_length=None, min_length=None, length_function=lambda item: len(item), use_specific_list=None):
    '''Filters list or lists by a max length and returns the ones under the max'''
    assert max_length is not None or min_length is not None, "Either max_length or min_length must be specified"
    min_length = 0 if min_length is None else min_length
    max_length = float("inf") if max_length is None else max_length
    lists = list(zip(*lists))
    lists = [lists[i] for i in range(len(lists)) if (all([min_length <= length_function(lists[i][x]) <= max_length for x in range(len(lists[i]))]) if use_specific_list is None else min_length <= length_function(lists[i][use_specific_list]) <= max_length)]
    return [list(x) for x in zip(*lists)]

# Shuffles multiple lists of the same length in the same ways
def shuffle_lists(*lists):
    '''
    Shuffle multiple lists in the same way
        Inputs:
            lists (lists): The lists to be shuffled
        Outputs:
            lists (lists): The shuffled lists
        Usage:
            list1, list2, list3 = shuffle_lists(list1, list2, list3)
    '''
    zipped_lists = list(zip(*lists)) if len(lists) > 1 else lists[0]
    random.shuffle(zipped_lists)
    return [list(f) for f in zip(*zipped_lists)] if len(lists) > 1 else [zipped_lists]

def normalize_string(s: str) -> str:
    '''Lowercase, trim, and remove non-letter characters'''
    # Turn a Unicode string to plain ASCII, thanks to
    # https://stackoverflow.com/a/518232/2809427
    def unicodeToAscii(s):
        import unicodedata
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    s = re.sub(r"\s+", r" ", s).strip()
    return s

def sort_lists_by_length(sorting_list, *other_lists, length_function=lambda x: len(x), longest_first=False):
    '''
    Sort multiple lists by the lengths of the first list of lists
        Inputs:
            sorting_list (list of lists): The list of lists to be used when sorting
            other_lists (lists): The other lists to be sorted in the same way
            length_function (function): A function determining the way to find the length of the example
            *longest_first (bool): Sort with the longest coming first [default: False]
        Outputs:
            lists (lists): The sorted lists
        Usage:
            list1, list2, list3 = sort_lists_by_length(list1, list2, list3)
    '''
    assert len(sorting_list) > 0, "A list to be sorted must have elements in it!"
    for i in range(len(other_lists)): assert len(other_lists[i]) == len(sorting_list), "All lists to be sorted must have the same length!"
    is_other_lists = other_lists is not None and len(other_lists) > 0
    zipped_lists = list(zip(sorting_list, *other_lists)) if is_other_lists else sorting_list
    if is_other_lists: zipped_lists.sort(key=lambda x: length_function(x[0]))
    else: zipped_lists.sort(key=lambda x: length_function(x))
    if longest_first: zipped_lists.reverse()
    return [list(lis) for lis in zip(*zipped_lists)] if is_other_lists else zipped_lists

def shuffle_lists_retain_batches(batch_size: int, *args):
        # Shuffle but retain the batches
        # Batch
        args = list(args)
        for i in range(len(args)):
            args[i] = [args[i][x:x + batch_size] for x in range(0, len(args[i]), batch_size)]
        # Shuffle them
        args = list(shuffle_lists(*args))
        # Unbatch
        for i in range(len(args)):
            args[i] = [subitem for sublist in args[i] for subitem in sublist]
        return args