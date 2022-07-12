import re
import os
from rich.console import Console
from rich.table import Table

# path = "/home/chris/Dir"
path = os.getcwd()
os.chdir(path)

var_list = []


# data content : word / statistics
class WordData:
    def __init__(self, word_input, file_input):
        self.word = word_input
        self.list_marked_data = []
        self.list_marked_data_count = []
        self.list_marked_data.append(file_input)
        self.list_marked_data_count.append(1)

    def append_word(self, file_input):
        if len(self.list_marked_data):
            for i in range(len(self.list_marked_data)):
                if self.list_marked_data[i] == file_input:
                    self.list_marked_data_count[i] += 1
                    return
        self.list_marked_data.append(file_input)
        self.list_marked_data_count.append(1)


# binary tree node object
class ObjectNode:
    def __init__(self, index, bin_stream, word_insert, file_insert, search):
        self.left = None
        self.right = None
        self.data = None
        # pass everything to check
        self.check(index, bin_stream, word_insert, file_insert, search)

    def check(self, index, bin_stream, word_insert, file_insert, search):
        if index >= len(bin_stream):  # end of word, retrieve or insert data
            if self.data is not None:  # data exists
                if search is not True:
                    self.data.append_word(file_insert)
                else:
                    var_list.append(self.data)
            else:  # no data ready
                if search is not True:
                    self.data = WordData(word_insert, file_insert)
                    var_list.append(self.data)
                else:
                    var_list.append(WordData(word_insert, "Not Found"))
        else:  # index is less than binary length, keep traversing the tree
            if int(bin_stream[index]) == 0:  # 0 detected go left
                if self.left is None:
                    self.left = ObjectNode(index + 1, bin_stream, word_insert, file_insert, search)  # node creation
                else:
                    self.left.check(index + 1, bin_stream, word_insert, file_insert, search)
            else:  # 1 detected go right
                if self.right is None:
                    self.right = ObjectNode(index + 1, bin_stream, word_insert, file_insert, search)  # node creation
                else:
                    self.right.check(index + 1, bin_stream, word_insert, file_insert, search)


# String to Binary
def to_binary(a):
    l = []
    m = ""
    for i in a:
        l.append(ord(i))
    for i in l:
        m = m + bin(i)[2:]
    return m


Head = None
# iterate through all file
for file in os.listdir():
    # Check whether file is in text format or not
    if file.endswith(".txt"):
        file_path = f"{path}/{file}"
        # call read text file function
        with open(file_path, 'r') as f:
            words = f.read().lower()  # make everything lower case
            words = re.sub('[^a-z]+', " ", words)  # remove everything except a-z
            words = list(words.split())  # break it into list
            for i in words:
                if Head is not None:
                    Head.check(0, to_binary(i), i, file, False)
                else:
                    Head = ObjectNode(0, to_binary(i), i, file, False)

c = Console()

print("\n")
c.print("                                             *************************************** ", style="blue")
c.print("                                             ****** Welcome to Machine Search ****** ", style="blue")
c.print("                                             *************************************** \n", style="blue")

c.print("<*>                   Options : \n")
c.print("<*>    [1] ---> Find the most common used Strings on the web ", style="#7df9ff")
c.print("<*>    [2] ---> Search Machine ", style="#7df9ff")
c.print("<*>    [3] ---> Exit  ", style="#7df9ff")

i = c.input("\n<*>    Select option : ")
print("<*>  Selected Option is : " + i)

if i == '1':  # Option 1
    table = Table(title="Output")
    table.add_column(" Word ", style="bright_yellow", no_wrap=True)
    table.add_column(" Found ", style="magenta", no_wrap=True)
    table.add_column(" Found on file ", justify="right", style="green", no_wrap=True)
    console = Console()
    # list testing, alphabetical sorting and printing
    # To sort the list in place...
    var_list.sort(key=lambda x: x.word, reverse=False)
    for i in var_list:
        table.add_row(i.word, str(i.list_marked_data_count), *i.list_marked_data)
        # print(i.word + " [Found] : " + str(len(i.list_marked_data)) + " [Times on] : ")
        # print(*i.list_marked_data)
        # print()
    console.print(table)
    c.print("\n<*>    The list is Shorted Alphabetically !", style="yellow")
    # to search make last parameter true to print the values
    # Head.check(0, to_binary("two"), "", "", True)

elif i == "2":  # Option 2
    var_list = []
    input_words = c.input("\n<*> Write the Words to Search : ")
    input_words = input_words.lower()  # make everything lower case
    input_words = re.sub('[^a-z]+', " ", input_words)  # remove everything except a-z
    input_words = list(input_words.split())  # break it into list
    print("<*> The words for Search are " + str(input_words))

    for i in input_words:
        Head.check(0, to_binary(i), i, "", True)

    table = Table(title="Output")
    table.add_column(" Word ", style="bright_yellow", no_wrap=True)
    table.add_column(" Found ", style="magenta", no_wrap=True)
    table.add_column(" Found on file ", justify="right", style="green", no_wrap=True)
    console = Console()

    for i in var_list:
        table.add_row(i.word, str(i.list_marked_data_count), *i.list_marked_data)
    console.print(table)

elif i == "3":
    quit()



