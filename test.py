#!/env/python3

import os
import re
import numpy as np
import pandas as pd

fname = ["a_example.txt", "b_read_on.txt", "c_incunabula.txt",
         "d_tough_choices.txt",
         "e_so_many_books.txt", "f_libraries_of_the_world.txt"]


def read_input(fin):
    with open(fin) as f:
        B, L, D = [int(v) for v in f.readline().split(' ')]
        books = [int(v) for v in f.readline().split(' ')]
        idl = 0
        toggle = True
        libraries = []
        p = []
        for l in f:
            if l == "\n":
                continue
            if toggle:
                p.append([int(v) for v in l.split(' ')] + [idl])
            else:
                p.append(sorted([int(v) for v in l.split(' ')],
                                key=lambda i: books[i], reverse=True))
                libraries.append(p.copy())
                p.clear()
                idl = idl + 1
            toggle = not toggle
    return B, L, D, books, libraries


def value(libraries, nbooks):
    v = sum([books[i] for i in libraries[1][0:nbooks]])
    print(v)
    return v


def fitness(library, days):
    v = (value(library, days * library[0][2])/library[0][1])
    return v


if __name__ == '__main__':
    for inputfile in fname:
        B, L, D, books, libraries = read_input(inputfile)
        print(books)
        libraries = sorted(libraries, key=lambda x: fitness(x, D))
        print(libraries)
        selected_libraries = []
        while D > 0 and len(libraries) > 0:
            D = D - libraries[-1][0][1]
            if D < 0:
                break
            l = libraries[-1]
            nbooks = D * l[0][2]
            l[1] = l[1][0:nbooks]
            selected_libraries.append(l)
            libraries = libraries[0:-1]

        with open(inputfile.split(".txt")[0] + ".out", "w") as f:
            f.write(str(len(selected_libraries)) + "\n")
            for library in selected_libraries:
                f.write(str(library[0][-1]) + " " + str(len(library[1])) + "\n")
                for book in library[1]:
                    f.write(str(book) + " ")
                f.write("\n")
