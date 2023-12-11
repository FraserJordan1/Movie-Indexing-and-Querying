from hashtable import *

import pytest

class TestHashtable:

    def test_create(self):
        hashtable = Hashtable()
        assert hashtable.num_buckets == 9 ## Default
        assert hashtable.num_elements == 0
        assert hashtable.buckets is not None
        assert len(hashtable.buckets) == 9

    def test_create_non_default_size(self):
        num_buckets = 5
        hashtable = Hashtable(num_buckets)
        assert hashtable.num_buckets == num_buckets ## Default
        assert hashtable.num_elements == 0
        assert hashtable.buckets is not None
        assert len(hashtable.buckets) == num_buckets

    def test_insert_correct_bucket(self):
        hashtable = Hashtable(5)
        key = 1
        value = "testing"
        target_bucket = hash(key) % hashtable.num_buckets
        hashtable.put(key, value)
        assert len(hashtable.buckets[target_bucket]) == 1
        assert hashtable.buckets[target_bucket][0].value == "testing"
        assert hashtable.buckets[target_bucket][0].key == 1

    def test_remove(self):
        hashtable = Hashtable(5)
        key = 1
        value = "testing"
        target_bucket = hash(key) % hashtable.num_buckets
        hashtable.put(key, value)
        assert len(hashtable.buckets[target_bucket]) == 1
        assert hashtable.buckets[target_bucket][0].value == "testing"
        assert hashtable.buckets[target_bucket][0].key == 1

        removed_kvp = hashtable.remove(1)
        assert removed_kvp.key == 1
        assert removed_kvp.value == "testing"
        assert len(hashtable.buckets[target_bucket]) == 0
        assert hashtable.num_elems() == 0
        assert hashtable.num_elements == 0

    def test_remove_nonexistent_key(self):
        hashtable = Hashtable(5)
        key = 1
        value = "testing"
        target_bucket = hash(key) % hashtable.num_buckets
        hashtable.put(key, value)
        assert len(hashtable.buckets[target_bucket]) == 1
        assert hashtable.buckets[target_bucket][0].value == "testing"
        assert hashtable.buckets[target_bucket][0].key == 1

        with pytest.raises(NotImplementedError):
            removed_kvp = hashtable.remove(3)


    def test_get_non_existent_key(self):
        hashtable = Hashtable(5)
        key = 1
        value = "testing"
        target_bucket = hash(key) % hashtable.num_buckets
        hashtable.put(key, value)
        assert len(hashtable.buckets[target_bucket]) == 1
        assert hashtable.buckets[target_bucket][0].value == "testing"
        assert hashtable.buckets[target_bucket][0].key == 1

        value = hashtable.get(15)
        assert value is None


    ## This is just for sanity checking; it helps us ensure that we
    ##   update Hashtable.num_elements in all the right places
    def test_num_elems(self):
        hashtable = Hashtable(5)
        hashtable.put(1, "testing")
        assert hashtable.num_elems() == 1
        assert hashtable.num_elems() == hashtable.num_elements

        hashtable.put(2, "testing")
        assert hashtable.num_elems() == 2
        assert hashtable.num_elems() == hashtable.num_elements

    def test_resize(self):
        hashtable = Hashtable(3)

        assert hashtable.num_elements == 0
        assert hashtable.num_buckets == 3

        for i in range(8):
            hashtable.put(i, f"testing{i}")
            assert hashtable.num_elements == i + 1
            assert hashtable.num_buckets == 3

        for i in range(8,20):
            hashtable.put(i, f"testing{i}")
            assert hashtable.num_elements == i + 1
            assert hashtable.num_buckets == 27

        for i in range(20):
            value = hashtable.get(i)
            assert value == f"testing{i}"


class TestHashtableIterator():

    def test_messy_basic(self):
        bucket1 = [11, 12, 13]
        bucket2 = [14]
        bucket3 = [15, 16]
        bucket4 = []
        bucket5 = [17, 18, 19, 110]

        results = [11, 12, 13, 14, 15, 16, 17, 18, 19, 110]

        hashtable = Hashtable(5)
        ## NOTE: I'm "breaking the abstraction" so we can test the enumerator specifically
        hashtable.buckets = [bucket1, bucket2, bucket3, bucket4, bucket5]
        for index, item in enumerate(hashtable):
            assert item == results[index]  ## The items being returned here aren't KVPs, just numbers, because I broke the abstraction with the buckets

    def test_basic_iterator(self):
        hashtable = Hashtable()
        for i in range(10):
            hashtable.put(i, f"value{i}")

        ## We want to check that the iterator returns all the elements, and none that aren't in there
        seen = [False] * 10
        for index, item in enumerate(hashtable):
            assert item.value == f"value{item.key}"
            if seen[item.key]:
               assert False ## This means we are seeing a KVP multiple times
            else:
                seen[item.key] = True
        ## Ensures that all items were seen
        for item in seen:
            assert item
