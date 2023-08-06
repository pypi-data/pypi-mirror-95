crc16
=====

介绍
----

查表法实现crc16算法.参数模型是CRC-16/MODBUS 多项式是8005。

API
---

.. code:: python

    """
    计算校验和.参数模型是CRC-16/MODBUS 多项式是8005,返回值是高字节在前的16位校验值
    """
    def checksum(data: bytearray) -> int

示例
----

.. code:: python

    class _UnitTest(unittest.TestCase):
        def test_case1(self):
            data = bytearray([1, 2, 3, 4, 5, 6, 7, 8, 9])
            self.assertEqual(crcmodbus.checksum(data), 0x0eb2)

        def test_case2(self):
            data = bytearray([3, 1, 4])
            self.assertEqual(crcmodbus.checksum(data), 0x8193)

        def test_case3(self):
            data = bytearray([0x19, 0x89, 0x56])
            self.assertEqual(crcmodbus.checksum(data), 0x47a9)


    if __name__ == '__main__':
        suite = unittest.TestSuite()
        suite.addTest(_UnitTest('test_case1'))
        suite.addTest(_UnitTest('test_case2'))
        suite.addTest(_UnitTest('test_case3'))
        runner = unittest.TextTestRunner()
        runner.run(suite)

