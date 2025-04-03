def test_312():
    test_verion = '3.12'
    new_feature = F"A f-string can contain \\ in {test_verion}"
    abc = ['A', 'B', 'C']
    print(f"""{new_feature} such as {'\N{BLACK HEART SUIT}'.join(abc)} """)
if __name__ == '__main__':
    print("Test c01a_proj1g0_sy")
    test_312()