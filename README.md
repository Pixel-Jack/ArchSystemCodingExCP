# Arch IOTILE Engineer - Virtual Device
**By Clément Ponthieu 28/11/2017**


## Goal :
#### OK - build a virtual IOTile Device 
    - It's called engine_vibration_device 
#### OK - output vibration data each data point is a random integer in [min_value, max_value]
#### OK    - implement Remote procedure call (RPC) with id 0x9000 that let you *get* and *set* min_value 
    - this RPC is called manage_min_value : _ manage_min_value get _ return min_value (integer)  
                                            _ manage_min_value set=3 _ return min_value (integer)   
#### OK  - implement Remote procedure call (RPC) with id 0x9001 that let you *get* and *set* max_value 
    - this RPC is called manage_max_value : _ manage_max_value get _ return max_value (integer) 
                                            _ manage_max_value set=300 _ return max_value (integer)   
#### OK    - implement RPC with id 0x8000 that returns a random integer value between min_value and max_value
    - this RPC is called get_vibration : _ get_vibration _ return vibration (integer in [min_value, max_value])  

#### OK - play with the iotile

#### OK - Tests : python script (test_assert.py)
   ##### OK - setting min_value
    - test_set_correct_min_value()
    - test_set_incorrect_min_value()
   ##### OK - setting max_value
    - test_set_correct_max_value()
    - test_set_incorrect_max_value()
   ##### OK - getting min_value
    - test_initialisation()
   ##### OK - getting max_value
    - test_initialisation()
   ##### OK - collecting data be sure that they are in the range
    - test_crossed_changes()
    - vibration_test() (That is launch after each change in all test function)
    Launch _python realTimeReadingWithRandomTest.py_ to see in realTime stream with random change and test.
    
    
## Bonus
#### OK - automatic test with tox and pytest
    - all test are in the file test_assert, you can launch it with _pytest test_assert.py_
    - tox is configure for Python2.7
#### OK - output vibration without having to call an RPC
    - Streams can be activated on the device 
    - You can launch realTimeReading.py to see the constant measure (fake) of vibration every second
    - You can also launch  realTimeReadingWithRandomTest.py in which stream random change of min_value and max_value occured


    