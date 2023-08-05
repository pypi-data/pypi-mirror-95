'''

SPDX-Copyright: Copyright (c) Schoening Consulting, LLC
SPDX-License-Identifier: Apache-2.0
Copyright 2020 Schoening Consulting, LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

'''

import unittest
from ff3 import FF3Cipher

# Test vectors taken from here: http://csrc.nist.gov/groups/ST/toolkit/documents/Examples/FF3samples.pdf

testVector = [
	{
		"radix" : 26,
		"key" : "EF4359D8D580AA4F7F036D6F04FC6A942B7E151628AED2A6ABF7158809CF4F3C",
		"tweak" :"9A768A92F60E12D8",
		"plaintext" : "0123456789abcdefghi",
		"ciphertext" : "p0b2godfja9bhb7bk38",
	}
]

class TestFF3(unittest.TestCase):
	c = None

	def test_encrypt_all(self):
		for i in range(10000):
			s = c.encrypt(testVector[0]['plaintext'])

	def test_decrypt_all(self):
		for i in range(10000):
			s = c.decrypt(testVector[0]['ciphertext'])

if __name__ == '__main__':
	c = FF3Cipher(testVector[0]['radix'], testVector[0]['key'], testVector[0]['tweak'])
	unittest.main()
