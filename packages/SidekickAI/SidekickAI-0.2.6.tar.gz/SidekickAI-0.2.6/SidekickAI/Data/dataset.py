import multiprocessing
try: multiprocessing.set_start_method('spawn') # Make multiprocessing behave like Windows (spawn not fork)
except: pass
import time, torch, math, random
from SidekickAI.Data import batching

class Dataset:
    ''' The Sidekick Dataloader Class \n
    Handles multithreaded data loading, batching, preparing, etc... \n
    Inputs:
        batch_size (int): The size of batches to feed out
        load_function (function) Parameters: (data (a dict with only the current index of data in it), other (a dict with other random things in it), global_index (the index to be loaded, global based on the start/end indexes passed into the dataset)): The function responsible for directly loading examples.  
            This function should load a single example if the collate_function is defined, or a batch of examples if not. 
            What gets returned will either be fed directly to the collate function, or directly out of the iterator.
        end_index (int): The index to stop loading the dataset. This index will be the highest one passed into the load_function. This will also be fed into the init_function.
        init_function (function) Parameters: (loader (the loader class), start_index (passed into the dataset), end_index (passed into the dataset)) [Default: None]: The function for handling initialization. Should store all nessacary variables in the data dict and the other dict.
        collate_function (function) Parameters: (batch (the list of batch_size outputs from the load_function), other (dict containing non data stuff)) [Default: None]: The function responsible for combining batch_size examples into a batch. Any additional preprocessing should be put in here. 
            If this function is not specified, the output of one call of the load_function will be assumed to be a full batch and be returned from the iterator.
        start_index (int) [Default: 0]: The index to start loading the dataset from. This index will be the lowest one passed into the load_function. This will also be fed into the init_function.
        preload (bool) [Default: False]: Whether or not to load all the data on initialization or not.
        num_workers (int) [Default: 0]: The number of multiprocessing processes to use to load data. The load/collate functions are called from these processes. If num_workers = 0, all loading will be done syncronously.
        data_chunk_size (int) [Default: None (Dynamic)]: The max number of examples to be loaded in at once. If left as none, will be decided dynamically based on full dataset size. Practically this will never be hit, but it is the theoretical max.
    '''
    def __init__(self, batch_size, load_function, init_function=None, collate_function=None, start_index=0, end_index=None, preload=False, data_chunk_size=None, **kwargs):
        self.__dict__.update(kwargs) # For any custom variables the user wants to pass in
        self.kwargs = kwargs
        self.batch_size = batch_size
        self.preload = preload
        self.num_workers = multiprocessing.cpu_count() - 1 if not preload else 0 # Haven't figured out a good way to preload with multiprocessing yet, so defaults to sync loading
        self.start_index = start_index
        self.end_index = end_index
        self.load_function = load_function
        self.init_function = init_function
        self.collate_function = collate_function
        self.workers = []

        # If data and other are already provided, don't run the init function
        if "data" not in kwargs or "other" not in kwargs:
            self.data, self.other = {}, {}
            if init_function is not None: init_function(self)
        if len(list(self.data.keys())) > 0:
            for (key, value) in self.data.items(): assert isinstance(value, list), str(key) + " is not a list. All items in the data dict must be a list!" # Make sure all items in the data dict are lists
            assert len(set([len(value) for (key, value) in self.data.items()])) <= 1, "Not all lists are of the same length!" # Ensure all of the lists are of the same length
            self.end_index = start_index + len(self.data[list(self.data.keys())[0]]) # Ensure the end_index is not furthur than the data itself
        else: assert end_index is not None, "If end index is not specified, data must be provided in the init function to know how many examples to load"

        if "batch_queue" not in kwargs or not self.preload:
            self.batch_queue = multiprocessing.JoinableQueue() if not preload else []
            if preload:
                # Call the loading function and join all of the created processes before returning fron the __init__ function
                self.load_data(self.start_index, self.end_index)

        self.loaded_index = start_index
        self.waits = 0
        self.iterations = 0
        # Find dynamic data_chunk_size
        self.data_chunk_size = min(min(max(int(self.example_len() / 5), 2000), 20000), self.example_len()) if data_chunk_size is None else data_chunk_size # 2000: min, 20000: max | These are arbitrary

    
    def __len__(self):
        return len(self.data[list(self.data.keys())[0]]) // self.batch_size if not self.preload else len(self.batch_queue)

    def example_len(self):
        return int(self.__len__() * self.batch_size)

    def __str__(self):
        return "[Sidekick Dataset | Batches: " + str(self.__len__()) + " Examples: " + str(self.example_len()) + "]"

    # Add two datasets together
    def __add__(self, other):
        # Ensure data is the same
        assert self.data.keys() == other.data.keys(), "Both datasets being combined must have the same type of data! (Data dicts don't match)"
        # Merge data
        for (k, v) in self.data:
            self.data[k] += other[k]
        
        # Resulting dataset will be preloaded only if both being combined are preloaded
        if self.preload and other.preload:
            self.batch_queue += other.batch_queue
        else: # Set preload to false if either dataset is not preloaded
            self.preload = False
            self.batch_queue = multiprocessing.JoinableQueue()
        return self

    # For list adding (reverse adding)
    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __iter__(self):
        self.reset()
        return iter(self.batch_queue) if self.preload else self

    def sample(self):
        if not self.preload:
            return self.__next__() # f not preloaded we aren't actually randomly sampling. This needs to be changed
        else:
            return self.batch_queue[random.randint(0, len(self.batch_queue) - 1)]

    def sample_iter(self):
        return DatasetSampler(self)

    def preload(self):
        self.load_data(self.start_index, self.end_index)

    def __next__(self):
        self.iterations += 1
        if self.iterations > self.__len__(): # Stop iterating
            self.stop_iteration()

        while self.batch_queue.empty():
            self.waits += 1
            time.sleep(1)
            if self.waits > 2:
                for job in self.workers: job.terminate()
                self.workers = []
                self.waits = 0
            if len(self.workers) < self.num_workers or self.num_workers == 0:
                if self.loaded_index >= self.end_index - self.batch_size: self.stop_iteration()
                self.load_data(self.loaded_index, min(self.loaded_index + self.data_chunk_size, self.example_len() - 1))
                self.loaded_index = min(self.loaded_index + self.data_chunk_size, self.example_len() - 1)
                self.waits = 0
                time.sleep(2)
        try:
            return self.batch_queue.get()
        except: return None

    def __getitem__(self, i):
        if isinstance(i, slice):
            # Return altered version of self
            return self.__class__(batch_size=self.batch_size, load_function=self.load_function, init_function=self.init_function, collate_function=self.collate_function, start_index=self.start_index,
                preload=self.preload, num_workers=self.num_workers, data_chunk_size=self.data_chunk_size, batch_queue=self.batch_queue[slice(int(math.floor(i.start / self.batch_size)) if i.start is not None else None, int(math.ceil(i.stop / self.batch_size)) if i.stop is not None else None, int(math.floor(i.step / self.batch_size)) if i.step is not None else None)] if self.preload else None, 
                data={key:value[i] for (key, value) in self.data.items()}, other=self.other, **self.kwargs)
        elif isinstance(i, int):
            if i + 1 > self.__len__(): raise Exception("Index out of range of the dataset!")
            if self.preload: return self.batch_queue[i]
            batch = self.collate_function([self.load_function({key:value[x] for (key, value) in self.data.items()}, self.other, i + x) for x in range(self.batch_size)], self.other)
            return batch
        else:
            raise Exception("Index is an unknown type! (Not an int or slice)")

    def stop_iteration(self):
        self.loaded_index = 0
        self.iterations = 0
        self.waits = 0
        self.batch_queue = multiprocessing.JoinableQueue()
        raise StopIteration

    def reset(self):
        self.loaded_index = 0
        self.iterations = 0
        self.waits = 0
        if not self.preload: self.batch_queue = multiprocessing.JoinableQueue()

    def shuffle(self):
        # Shuffle data
        if self.preload:
            random.shuffle(self.batch_queue)
        else:
            lists = batching.shuffle_lists_retain_batches(self.batch_size, *self.data.values())
            for i, key in enumerate(self.data.keys()):
                self.data[key] = lists[i]
        return self

    def load_data(self, start_index, end_index):
        # If num_workers = 0, run load_job syncrounously
        if self.num_workers == 0:
            load_job({key:value[start_index - self.start_index:end_index - self.start_index] for (key, value) in self.data.items()}, self.other, start_index, self.batch_size, self.load_function, self.collate_function, self.batch_queue, None if len(list(self.data.keys())) > 0 else self.end_index)
        else:
            # Divide the data into num_workers slices to feed into each worker
            slice_size = (end_index - start_index) // self.num_workers
            self.workers = []
            for i in range(self.num_workers):
                job = multiprocessing.Process(target=load_job, args=({key:value[start_index + (slice_size * i) - self.start_index:start_index + (slice_size * (i + 1)) - self.start_index] for (key, value) in self.data.items()}, self.other, start_index + (slice_size * i), self.batch_size, self.load_function, self.collate_function, self.batch_queue))
                job.start()
                self.workers.append(job)

def load_job(data, other, start_index, batch_size, load_function, collate_function, batch_queue, end_index): # The job to be run in each worker
    end_index = start_index + len(data[list(data.keys())[0]]) if len(list(data.keys())) > 0 else end_index
    for i in range(0, end_index - start_index, batch_size):
        if collate_function is None:
            batch = load_function({key:value[i] for (key, value) in data.items()}, other, start_index + i) # Pass in data, other, global index
        else:
            batch = collate_function([load_function({key:value[x] for (key, value) in data.items()}, other, start_index + x) for x in range(i, min(i + batch_size, end_index - start_index))], other)
        # for item in batch: # Ensure all tensors are in shared memory to help with multiprocessing (NOT SURE IF THIS IS NEEDED, SOMETIMES CAUSES PROBLEMS)
        #     if isinstance(item, torch.Tensor):
        #         item.share_memory_()
        if isinstance(batch_queue, list): batch_queue.append(batch)
        else: batch_queue.put_nowait(batch)
    if not isinstance(batch_queue, list): batch_queue.join()


class DatasetSampler:
    def __init__(self, dataset):
        self.dataset = dataset
        self.counter = 0
        self.dataset_len = len(dataset)

    def __iter__(self): 
        self.counter = 0
        return self

    def __next__(self): 
        self.counter += 1
        if self.counter >= self.dataset_len: raise StopIteration
        return self.dataset.sample()