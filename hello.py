print("Hello World!")



if "A">"a":
    print("true")
else:
    print("false")


my_list= [2,5,3,82,8,"A",3,82,652,54,26,0,2555,475,24]
my_dictionary={"key1":15,"key1":16,"key1":19,"key1":11,"key1":13,"key1":14,"key1":51,"key1":61, }
my_tuple= (2,5,3,82,8,"A",3,82,652,54,26,0,2555,475,24)
my_set={"a"}
my_set.add("b")

try:
    for num in my_list:
        if num%2!=0:
            print(num)
except Exception as e:
    print(f"error message: {e}")

    print(type(my_dictionary))
    print((my_tuple[::]))
    print((my_set))

    for elem in my_tuple:
        if(isinstance(elem,int)):
            print(elem)

    x=0
    while x<5:
        print(x)
        x+=1
    else:
        print("X is >=5")           