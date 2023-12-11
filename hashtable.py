# This is a helper data class to allow us to store both the key 
# and the data associated with that key.
class KeyValuePair:
    def __init__(self, key, value) -> None:
        self.key = key
        self.value = value

# Used for iterating through hash table
class HashtableIterator:
    def __init__(self, hashtable):
        self.bucket_iterator = hashtable.buckets.__iter__()
        self.list_iterator = self.bucket_iterator.__next__().__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.list_iterator.__next__()
        except StopIteration:
            ## No more elements in this bucket; go to the next one
            try:
                self.list_iterator = self.bucket_iterator.__next__().__iter__()
                return self.__next__() ## Recursive call so we can move on from an empty bucket
            except StopIteration:
                ## No more buckets left to visit
                raise StopIteration

class Hashtable:
    def __init__(self, num_buckets:int = 9) -> None:
        self.num_buckets = num_buckets
        self.num_elements = 0
        self.buckets = [[] for _ in range(self.num_buckets)] ## List of lists

    # put new value in hashtable with corresponding key and assigned value
    def put(self, key:str, value:int or float or str or bool) -> None:
        index = hash(key) % self.num_buckets
        bucket = self.buckets[index]
        for kvp in bucket:
            if kvp.key == key:
                kvp.value = value
                return
        bucket.append(KeyValuePair(key, value))
        self.num_elements += 1
        if self.load_factor() > 0.7:
            self.resize()

    # grab desired key from hashmap
    def get(self, key:str) -> None or int or float or str or bool:
        index = hash(key) % self.num_buckets
        bucket = self.buckets[index]
        for kvp in bucket:
            if kvp.key == key:
                return kvp.value
        return None

    # load factor
    def load_factor(self) -> float:
        return self.num_elements / self.num_buckets

    # resize the hashtable
    def resize(self) -> None:
        ## If the load factor is > threshold
        ## Create a new hashtable
        ## Take elements out of this hashtable and put them in the new hashtable
        ## Set self equal to the new hashtable
        if self.num_elements == 9:
            # Resize to 27 buckets when exactly 9 elements are added
            new_num_buckets = 27
            new_hashtable = Hashtable(new_num_buckets)

            for bucket in self.buckets:
                for kvp in bucket:
                    # Rehash and add elements to the new hashtable
                    new_hashtable.put(kvp.key, kvp.value)

            # Update current hashtable
            self.__dict__.update(new_hashtable.__dict__)

    ## This is a helpful helper function
    def num_elems(self) -> int:
        num_elems = 0
        for bucket in self.buckets:
            num_elems += len(bucket)
        return num_elems

    # remove key and corresponding value from hash map
    def remove(self, key:str) -> KeyValuePair:
        index = hash(key) % self.num_buckets
        bucket = self.buckets[index]

        for i, kvp in enumerate(bucket):
            if kvp.key == key:
                removed_kvp = bucket.pop(i)  # Remove the KeyValuePair from the bucket
                self.num_elements -= 1  # Decrement the number of elements
                return removed_kvp  # Return the removed KeyValuePair
        raise NotImplementedError
    
    def __iter__(self) -> HashtableIterator:
        return HashtableIterator(self)
