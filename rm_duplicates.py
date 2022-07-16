#!/usr/bin/env python3

# File: rm_duplicates.py

"""
I was just doing an experiment of removing consecutive duplicates from a
list . Did it in the following ways  and it all worked . Just need to know
which one should be preferred ?  which one is more good ?

lst = [2, 2, 3, 3, 3, 2, 2, 5, 5, 6, 3, 3, 3, 3]
# Ways of removing consequtive duplicates
[ele for i, ele in enumerate(lst) if i==0 or ele != lst[i-1]]
[2, 3, 2, 5, 6, 3]
val = object()
[(val := ele) for ele in lst if ele != val]
[2, 3, 2, 5, 6, 3]
import itertools
[val for val, grp in itertools.groupby(lst)]
[2, 3, 2, 5, 6, 3]

Is there anything else more efficient ?

Re: [Tutor] Ways of removing consequtive duplicates from a list
Inbox
avi.e.gross@gmail.com via python.org
Sat 16 Jul 2022 02:43:08 PM PDT
Manprit,

Your message is not formatted properly in my email and you just asked any
women present to not reply to you, nor anyone who has not been knighted by a
Queen. I personally do not expect such politeness but clearly some do.

What do you mean by most efficient? Seriously.

For a list this size, almost any method runs fast enough. Efficiency
considerations may still apply but mainly consist of startup costs that can
differ quite a bit and even change when some of the underlying functionality
is changed such as to fix bugs, or deal with special cases or added options.

lst = [2, 2, 3, 3, 3, 2, 2, 5, 5, 6, 3, 3, 3, 3]


So are you going to do the above ONCE or repeatedly in your program? There
are modules and methods available to do testing by say running your choice a
million times that might provide you with numbers. Asking people here,
probably will get you mostly opinions or guesses. And it is not clear why
you need to know what is more efficient unless the assignment asks you to
think analytically and the thinking is supposed to be by you.

Here are your choices that I hopefully formatted in a way that lets them be
seen. But first, this is how your original looked:

[ele for i, ele in enumerate(lst) if i==0 or ele != lst[i-1]] [2, 3, 2, 5,
6, 3] val = object() [(val := ele) for ele in lst if ele != val] [2, 3, 2,
5, 6, 3] import itertools [val for val, grp in itertools.groupby(lst)] [2,
3, 2, 5, 6, 3]

The first one looks like a list comprehension albeit it is not easy to see
where it ends. I stopped when I hit an "or" but the brackets were not
finished:

[ele for i, ele in enumerate(lst) if i==0


And even with a bracket, it makes no sense!

So I read on:

#-----Choice ONE:
[ele for i, ele in enumerate(lst) if i==0 or ele != lst[i-1]]

OK, that worked and returned: [2, 3, 2, 5, 6, 3]

But your rendition shows the answer "[2, 3, 2, 5, 6, 3"  which thus is not
code so I remove that and move on:

val = object() [(val := ele) for ele in lst if ele != val]

This seems to be intended as two lines:

#-----Choice TWO:
val = object()
[(val := ele) for ele in lst if ele != val]

And yes it works and produces the same output I can ignore.

By now I know to make multiple lines as needed:

#-----Choice THREE:
import itertools
[val for val, grp in itertools.groupby(lst)]

So how would you analyze the above three choices, once unscrambled? I am not
going to tell you what I think.

What do they have in common?

What I note is they are all the SAME in one way. All use a list
comprehension. If one would have used loops for example, that might be a
factor as they tend to be less efficient in python. But they are all the
same.

So what else may be different?

Choice THREE imports a module. There is a cost involved especially if you
import the entire module, not just the part you want so the import method
adds a somewhat constant cost. But if the module is already used elsewhere
in your program, it is sort of a free cost to use it here and if you use
this method on large lists or many times, the cost per unit drops. How much
this affects efficiency is something you might need to test and even then
may vary.

Do you know what "enumerate()" does in choice ONE? It can really matter in
deciding what is efficient. If I have a list a million or billion units
long, will enumerate make another list of numbers from 1 to N that long in
memory, or will it make an iterator that is called repeatedly to make the
next pair for you?

Choices ONE and TWO both have visible IF clauses but the second one has an
OR with two parts to test. In general, the more tests or other things done
in a loop, compared to a loop of the same number of iterations, the more
expensive it can be. But a careful study of the code

if i==0 or ele != lst[i-1]

suggests the first condition is only true the very first time but is
evaluated all N times so the second condition is evaluated N-1 times.
Basically, both are done with no real savings.

Choice TWO has a single test in the if, albeit it is for an arbitrary object
which can be more or less expensive depending on the object. The first
condition in choice ONE was a fairly trivial integer comparison and the
second, again, could be for any object. So these algorithms should work on
things other than integers.

Consider this list containing tuples and sets:

obj_list = [ (1,2), (1,2,3), (1,2,3), {"a", 1}, {"b", 2}, {"b", 2} ]

Should this work?

[ele for i, ele in enumerate(obj_list) if i==0 or ele != obj_list[i-1]]

[(1, 2), (1, 2, 3), {1, 'a'}, {'b', 2}]

I think it worked but the COMPARISONS between objects had to be more complex
and thus less efficient than for your initial example. So the number and
type of comparisons can be a factor in your analysis depending on how you
want to use each algorithm.

For completeness, I also tried the other two algorithms using this alternate
test list:

[(val := ele) for ele in obj_list if ele != val]

[(1, 2), (1, 2, 3), {1, 'a'}, {'b', 2}]

And

[val for val, grp in itertools.groupby(obj_list)]

[(1, 2), (1, 2, 3), {1, 'a'}, {'b', 2}]

Which brings us to the latter. What exactly does the groupby() function do?

If it is an iterator, and it happens to be, it may use less memory but for
small examples, the iterator overhead may be more that just using a short
list, albeit lists are iterators of a sort too.

You can look at these examples analytically and find more similarities and
differences but at some point you need benchmarks to really know. The
itertools module is often highly optimized, meaning in many cases being done
mostly NOT in interpreted python but in C or C++ or whatever. If you wrote a
python version of the same idea, it might be less efficient. And in this
case, it may be overkill. I mean do you know what is returned by groupby? A
hint is that it returns TWO things and you are only using one. The second is
nonsense for your example as you are using the default function that
generates keys based on a sort of equality so all the members of the group
are the same. But the full power of group_by is if you supply a function
that guides choices such as wanting all items that are the same if written
in all UPPER case.

So my guess is the itertools module chosen could be more than you need. But
if it is efficient and the defaults click right in and do the job, who
knows? My guess is there is more cost than the others for simple things but
perhaps not for more complex things. I think it does a form of hashing
rather than comparisons like the others.

I hope my thoughts are helpful even if they do not provide a single
unambiguous answer. They all seem like reasonable solutions and probably
NONE of them would be expected if this was homework for a class just getting
started. That class would expect a solution for a single type of object such
as small integers and a fairly trivial implementation in a loop that may be
an unrolled variant of perhaps close to choice TWO. Efficiency might be a
secondary concern, if at all.

And for really long lists, weirdly, I might suggest a variant that starts by
adding a unique item in front of the list and then removing it from the
results at the end.
"""

def rm_duplicates(iterable):
    last = ''
    for item in iterable:
        if item != last:
            yield item
            last = item

lst = [2, 2, 3, 3, 3, 2, 2, 5, 5, 6, 3, 3, 3, 3]


if __name__ == '__main__':
    res = [res for res in rm_duplicates(lst)]
    print(res)
    assert res == [2, 3, 2, 5, 6, 3]

