class test:
    def __init__(self, decorated):
        self.data = "123"
        self._decorated = decorated

    def test123(self):
        print(self.data)

    def __call__(self):
        print(self._decorated.__name__)
        self._decorated()
        print(self._decorated.__name__)
            

@test
def test12():
    print("함수호출")

test12()


