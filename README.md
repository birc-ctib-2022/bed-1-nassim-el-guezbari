[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=8916531&assignment_repo_type=AssignmentRepo)
# Processing BED files (Part 1)

In this, and the next, project we will look at [BED files](https://en.wikipedia.org/wiki/BED_(file_format)), or at least a slightly simplified version of them. BED files are a textual file format developed for storing genomic information in a form that is readable for both humans and computers, and while it is on the simpler side of file formats, it resembles other formats you are likely to work with in your future career. The two projects we will do with BED files will show you have a little bit of computational thinking will help you when working with this kind of data.

You can read the full specification for BED files on the Wikipedia page linked to above, but we will restrict ourself to a subset of the format (that is still valid BED, however).

Full BED files can contain a header, which we will not allow, and then between 3 and 12 space separated (3 mandatory and 9 optional) columns. When it comes to such tabular data, some file formats are very restrictive, requiring space separation (a single space) or tab separated (a single tab character) between columns. BED allows both, but does specify that tab is preferable. What this means is that some tools will not accept anything else, making tab-separation the de facto standard. Bioinformatics is full of such crap. 

We will not have header-data and we will ignore the kind of data a file can contain beyond genomic locations and a feature name. For us, a BED file consists of four space separated columns, with the interpretation

```
1: chrom      -- chromosome name
2: chromStart -- chromosomal position (zero indexed)
3: chromEnd   -- chromosomal position (zero indexed)
4: name       -- the name of this line (think of it as a feature name)
```

For columns two and three, zero indexed means that we index into the genome the same way we do into Python lists: the first index is zero. There is absolutely no consistency in the file formats used in bioinformatics when it comes to indexing from zero or one, and you have to check it every time you get data in a new format, but for BED files we index from zero.

Since BED files are allowed to have either space or tabs between columns, we will allow the same, but we will only allow that for input. If we output BED data, we hold ourselves to higher standards and always use a single tab between columns. Be liberal in how you read input and conservative in how you output is a good way to code, and it will make your life easier if you get used to that early.

You should interpret a row such as

```
chrFoo  200 250 qux
```

as saying that from position 200 to 250 chromosome `chrFoo` has feature `qux`. For intervals, BED files include the start index and exclude the end index, the same way that Python does (and no, there is no consistency in what formats do with intervals either). So if you have a chromsome and the interval `start` to `end`, think `chrom[start:end]`. BED files work a lot like Python here (and it isn't an accident that I chose BED for these projects).

We will make one more simplifying assumption about our data: all the intervals are a single nucleoptide, so `chromEnd = chromStart + 1`. This simplifies the exercises we have to do (but who knows, maybe we will remove this simplification in future exercises?).

## Reading BED files

The first thing we need to do is write code such that we can read a BED file. By itself that isn't much use, but we might be in a situation where we have BED files output by some fool program that uses mixed spaces and tabs, and we need that data in a tool that only reads tabs. While it might not be the most straightforward solution to the problem, there are existing tools that can solve this for us, if we do have a tool that can read in BED data and then write it out again, we certainly do have a solution. So, we will write such a tool; then once we have the code for that, we can start doing more useful things with it.

I've already done most of the work for you. In the module `bed` I have put two functions, `parse_line()` and `print_line()` that parses a single line of BED information and prints it to a file, respectively. In the file `format_bed.py` I have written most of a tool for solving this exercise; you just need to fill in the final few details.

(In this file, notice that I have changed how we parse options compared to the previous project. In the last project, you saw the basic way processes work with options, but different languages and different environmments typically have better solutions. The `argparse` module is one of the prefered ways to handle options in Python, and you might want to use that for your own projects).

## Slicing genomic features

"Genomics" sounds sexy, and we like to pretend that we analyse whole genomes, sometimes even several genomes, at the same time. The truth is, though, that we often spend most of our times looking at a small fraction of a genome, and we are interested in what features those parts of the genome hold.

If you have a BED file that contains the features for the entire genome, and you have a few select regions you want to extract, you need to come up with a method to achieve that; you need all the BED lines that overlap your regions.

This, now, is your task: write a program that takes two files as input, a BED file with features and a "query" file in a similar format, described below. Output all the lines in the BED file that falls inside the regions in the query file.

The query file will essentially consist of one or more lines of the first three columns in a BED file:

```
chrom   chromStart  chromEnd
```

Here, we do not require that `chromEnd` is one past `chromStart` (`chromEnd == chromStart + 1`), but a line like the one above should be interpreted as asking for all features on chromosome `chrom` between `chromStart` and `chromEnd`, with `chromStart` included and `chromEnd` excluded.

To get you started, I have written the option parsing in the file `query_bed.py` (you might want to check it out, as it differs slightly from `format_bed.py` and shows a new way to do this). 

Then, realising that just parsing command line options isn't much compared to the work I have left for you, I also put some code in `query.py` that you might find helpful. It is a table where you can insert BED lines, and extract only those that sits on a desired chromosome. When you read the BED file, you can put the lines into this table, and when you need to query, you can get the lines from the correct chromosome. Then all you need to do filter the lines so you only get those in the right interval.

The rest, however, is up to you. Implement me a `query_bed.py` so I can extract all features that overlap a set of regions.

When you have implemented the tool, answer the questions below, commit it to GitHub, and you are done.

## Questions

How does your method for extracting features work?

Firstly I make sure the format is "ideal" bed with tabs seperating the 4 couloums. Accomplishing this i use
    parse_line function, in a for loop over the input file, to parse each line of the bedfile.
Then I define every value into their position (abusing the fact that we are working with input no larger than 3).
    This is done through naming every position making them alle easily accesible for searching through.
Afterwards every line that is on the chromosome of interest is added to a list, basicly creating a subset of the
    input file. This is accomplished through the "get_chrom" command.
Lastly I run through this list checking if a line fits in the designated area, the user has searched for.
    If the start and end is found within that searched area it gets printed directly to the output.file.
    This one is accomplished through a for loop, of every line/entry in the list that was made in the earlier step.
    Then checking if the start and end positions are within the seared interval by an if statement at the end of the loop.

What is the complexity of the algorithm, as a function of the size of the two input files? When you answer this, you need to know that you can get the list of chromosomse from a `query.Table` in constant time, but it does, of course, take longer to run through all the lines in it.

Not-complex? I have avoided any heavy processing by making the code only function for reagion no larger nor smaller than 3.
    So for the most part i would assume its constant in that i am rather specific with telling it to look at position X, rather
    than searching for something more general making sure to avoide pitfalls like overlaps.

Did you, at any point, exploit that our features are on single nucleotides and not larger regions?

Yes as mention a couple times above, this code would for the most part be unusable for any other sizes than 3.
    Though that mostly in the query_bed where that is abused in 2 seperate loops.
Though i also think only "upgrading" those two loops is all thats needed to allow for broader regions. 

If you did, what would it take to handle general regions?

I am thinking that instead of using positions [0],[1] and [2] i would be able to replave these by the user input.
    So something along the lines of [0],[chrom_start] and [chrom_end]. Then we just need to account for overlapping
    which i think can be done through a while loop, to check if any one line matched something from any other line.