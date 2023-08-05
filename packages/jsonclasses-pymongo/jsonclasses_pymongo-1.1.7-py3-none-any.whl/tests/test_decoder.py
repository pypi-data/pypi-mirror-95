from __future__ import annotations
from unittest import TestCase
from typing import List, Dict
from datetime import date, datetime
from bson import ObjectId
from jsonclasses import jsonclass, types
from jsonclasses_pymongo import MongoObject
from jsonclasses_pymongo.decoder import Decoder


class TestDecoder(TestCase):

    def test_decode_str_into_str(self):
        @jsonclass
        class SimpleDecodeStr(MongoObject):
            val1: str
            val2: str
        data = {
            '_id': ObjectId(),
            'createdAt': datetime.now(),
            'updatedAt': datetime.now(),
            'val1': '12345',
            'val2': '67890'
        }
        instance = Decoder().decode_root(data, SimpleDecodeStr)
        self.assertEqual(instance.id, str(data['_id']))
        self.assertEqual(instance.val1, '12345')
        self.assertEqual(instance.val2, '67890')
        self.assertIsInstance(instance.val1, str)
        self.assertIsInstance(instance.val2, str)

    def test_decode_int_into_int(self):
        @jsonclass
        class SimpleDecodeInt(MongoObject):
            val1: int
            val2: int
        data = {
            '_id': ObjectId(),
            'createdAt': datetime.now(),
            'updatedAt': datetime.now(),
            'val1': 12345,
            'val2': 67890
        }
        instance = Decoder().decode_root(data, SimpleDecodeInt)
        self.assertEqual(instance.id, str(data['_id']))
        self.assertEqual(instance.val1, 12345)
        self.assertEqual(instance.val2, 67890)

    def test_decode_float_into_float(self):
        @jsonclass
        class SimpleDecodeFloat(MongoObject):
            val1: float
            val2: float
        data = {
            '_id': ObjectId(),
            'createdAt': datetime.now(),
            'updatedAt': datetime.now(),
            'val1': 12345.6,
            'val2': 67890.1
        }
        instance = Decoder().decode_root(data, SimpleDecodeFloat)
        self.assertEqual(instance.id, str(data['_id']))
        self.assertEqual(instance.val1, 12345.6)
        self.assertEqual(instance.val2, 67890.1)

    def test_decode_bool_into_bool(self):
        @jsonclass
        class SimpleDecodeBool(MongoObject):
            val1: bool
            val2: bool
        data = {
            '_id': ObjectId(),
            'createdAt': datetime.now(),
            'updatedAt': datetime.now(),
            'val1': True,
            'val2': False
        }
        instance = Decoder().decode_root(data, SimpleDecodeBool)
        self.assertEqual(instance.id, str(data['_id']))
        self.assertEqual(instance.val1, True)
        self.assertEqual(instance.val2, False)

    def test_decode_datetime_into_date(self):
        @jsonclass
        class SimpleDecodeDate(MongoObject):
            val1: date
            val2: date
        data = {
            '_id': ObjectId(),
            'createdAt': datetime.now(),
            'updatedAt': datetime.now(),
            'val1': datetime(2012, 9, 5, 0, 0, 0),
            'val2': datetime(2020, 9, 5, 0, 0, 0),
        }
        instance = Decoder().decode_root(data, SimpleDecodeDate)
        self.assertEqual(instance.id, str(data['_id']))
        self.assertEqual(instance.val1, date(2012, 9, 5))
        self.assertEqual(instance.val2, date(2020, 9, 5))

    def test_decode_datetime_into_datetime(self):
        @jsonclass
        class SimpleDecodeDatetime(MongoObject):
            val1: datetime
            val2: datetime
        data = {
            '_id': ObjectId(),
            'createdAt': datetime.now(),
            'updatedAt': datetime.now(),
            'val1': datetime(2012, 9, 5, 6, 25, 0),
            'val2': datetime(2020, 9, 5, 8, 25, 0),
        }
        instance = Decoder().decode_root(data, SimpleDecodeDatetime)
        self.assertEqual(instance.id, str(data['_id']))
        self.assertEqual(instance.val1, datetime(2012, 9, 5, 6, 25, 0))
        self.assertEqual(instance.val2, datetime(2020, 9, 5, 8, 25, 0))

    def test_decode_embedded_list(self):
        @jsonclass
        class SimpleDecodeList(MongoObject):
            vals: List[int]
        data = {
            '_id': ObjectId(),
            'createdAt': datetime.now(),
            'updatedAt': datetime.now(),
            'vals': [1, 2, 3, 4, 5]
        }
        instance = Decoder().decode_root(data, SimpleDecodeList)
        self.assertEqual(instance.id, str(data['_id']))
        self.assertEqual(instance.vals, [1, 2, 3, 4, 5])

    def test_decode_local_keys_list(self):
        @jsonclass
        class SimpleDecodeLocalKeyListAddress(MongoObject):
            city: str
            owner: SimpleDecodeLocalKeyList = types.instanceof(
                'SimpleDecodeLocalKeyList').linkedby('address')

        @jsonclass
        class SimpleDecodeLocalKeyList(MongoObject):
            addresses: List[SimpleDecodeLocalKeyListAddress] = (types.linkto
                .listof(SimpleDecodeLocalKeyListAddress))
        data = {
            '_id': ObjectId(),
            'createdAt': datetime.now(),
            'updatedAt': datetime.now(),
            'addressesIds': [ObjectId(), ObjectId()]
        }
        instance = Decoder().decode_root(data, SimpleDecodeLocalKeyList)
        self.assertEqual(instance.id, str(data['_id']))
        self.assertEqual(getattr(instance, 'addresses_ids')
                         [0], str(data['addressesIds'][0]))
        self.assertEqual(getattr(instance, 'addresses_ids')
                         [1], str(data['addressesIds'][1]))

    def test_decode_embedded_dict(self):
        @jsonclass
        class SimpleDecodeDict(MongoObject):
            vals: Dict[str, int]
        data = {
            '_id': ObjectId(),
            'createdAt': datetime.now(),
            'updatedAt': datetime.now(),
            'vals': {'one': 1, 'two': 2}
        }
        instance = Decoder().decode_root(data, SimpleDecodeDict)
        self.assertEqual(instance.id, str(data['_id']))
        self.assertEqual(instance.vals, {'one': 1, 'two': 2})

    def test_decode_embedded_shape(self):
        @jsonclass
        class SimpleDecodeShape(MongoObject):
            vals: Dict[str, int] = types.shape({
                'one': types.int,
                'two': types.int
            })
        data = {
            '_id': ObjectId(),
            'createdAt': datetime.now(),
            'updatedAt': datetime.now(),
            'vals': {'one': 1, 'two': 2}
        }
        instance = Decoder().decode_root(data, SimpleDecodeShape)
        self.assertEqual(instance.id, str(data['_id']))
        self.assertEqual(instance.vals, {'one': 1, 'two': 2})

    def test_decode_embedded_instance(self):
        @jsonclass
        class SimpleDecodeInstanceAddress(MongoObject):
            city: str

        @jsonclass
        class SimpleDecodeInstance(MongoObject):
            address: SimpleDecodeInstanceAddress
        data = {
            '_id': ObjectId(),
            'createdAt': datetime.now(),
            'updatedAt': datetime.now(),
            'address': {
                '_id': ObjectId(),
                'createdAt': datetime.now(),
                'updatedAt': datetime.now(),
                'city': 'Shanghai'
            }
        }
        instance = Decoder().decode_root(data, SimpleDecodeInstance)
        self.assertEqual(instance.id, str(data['_id']))
        self.assertEqual(instance.address.id, str(data['address']['_id']))
        self.assertEqual(instance.address.city, "Shanghai")

    def test_decode_local_key_instance(self):
        @jsonclass
        class SimpleDecodeLocalKeyInstanceAddress(MongoObject):
            city: str
            owner: SimpleDecodeLocalKeyInstance = types.instanceof(
                'SimpleDecodeLocalKeyInstance').linkedby('address')

        @jsonclass
        class SimpleDecodeLocalKeyInstance(MongoObject):
            address: SimpleDecodeLocalKeyInstanceAddress = (types
                    .linkto.instanceof(
                        SimpleDecodeLocalKeyInstanceAddress))
        data = {
            '_id': ObjectId(),
            'createdAt': datetime.now(),
            'updatedAt': datetime.now(),
            'addressId': ObjectId()
        }
        instance = Decoder().decode_root(data, SimpleDecodeLocalKeyInstance)
        self.assertEqual(instance.id, str(data['_id']))
        self.assertEqual(getattr(instance, 'address_id'),
                         str(data['addressId']))

    def test_decode_camelized_dict_keys(self):
        @jsonclass
        class MediumDecodeCamelizeDictKeys(MongoObject):
            val: Dict[str, str] = types.dictof(types.str)
        data = {
            'val': {
                'keyOne': 'val_one',
                'keyTwo': 'val_two'
            }
        }
        instance = Decoder().decode_root(data, MediumDecodeCamelizeDictKeys)
        self.assertEqual(
            instance.val, {'key_one': 'val_one', 'key_two': 'val_two'})

    def test_decode_uncamelized_dict_keys(self):
        @jsonclass(camelize_db_keys=False)
        class MediumDecodeUncamelizeDictKeys(MongoObject):
            val: Dict[str, str] = types.dictof(types.str)
        data = {
            'val': {
                'keyOne': 'val_one',
                'keyTwo': 'val_two'
            }
        }
        instance = Decoder().decode_root(data, MediumDecodeUncamelizeDictKeys)
        self.assertEqual(
            instance.val, {'keyOne': 'val_one', 'keyTwo': 'val_two'})

    def test_decode_camelized_shape_keys(self):
        @jsonclass
        class MediumDecodeCamelizeShapeKeys(MongoObject):
            val: Dict[str, str] = types.shape({
                'key_one': types.str,
                'key_two': types.str
            })
        data = {
            'val': {
                'keyOne': 'val_one',
                'keyTwo': 'val_two'
            }
        }
        instance = Decoder().decode_root(data, MediumDecodeCamelizeShapeKeys)
        self.assertEqual(
            instance.val, {'key_one': 'val_one', 'key_two': 'val_two'})

    def test_decode_uncamelized_shape_keys(self):
        @jsonclass(camelize_db_keys=False)
        class MediumDecodeUncamelizeShapeKeys(MongoObject):
            val: Dict[str, str] = types.shape({
                'key_one': types.str,
                'key_two': types.str
            })
        data = {
            'val': {
                'key_one': 'val_one',
                'key_two': 'val_two'
            }
        }
        instance = Decoder().decode_root(data, MediumDecodeUncamelizeShapeKeys)
        self.assertEqual(
            instance.val, {'key_one': 'val_one', 'key_two': 'val_two'})
