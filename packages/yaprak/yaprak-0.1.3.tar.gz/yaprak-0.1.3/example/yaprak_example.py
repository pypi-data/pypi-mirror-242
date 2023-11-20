from yaprak.yaprak import Yaprak

class myClass(Yaprak):
    def __init__(self, config):
        Yaprak.__init__(self, config)
        self.total = 0
        self.product = 0
        self.file_input = None

    def load(self, file):
        with open(file, 'r') as f:
            self.file_input = int(f.readline())
            print(self.file_input)


    def save(self, file):
        with open(file, 'w') as f:
            f.write("Sum is " + str(self.total) +"\n")		
            f.write("Product is " + str(self.product))		

    def report(self):
        print('Finished processing')

    def add(self, process_spec):
        self.total = process_spec['a1'] + int(str(self.file_input))

    def mul(self, process_spec):
        self.product = process_spec['m1'] * self.config['m_global'] 


yap = myClass('myconfig.json')
yap.run()
