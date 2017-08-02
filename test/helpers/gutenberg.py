# This file is used by the TestHandleGutenberg class in
#   test.unit_test.test_scrubber.py

FRONT_PLATE = "'The Project Gutenberg EBook of Pride and Prejudice, by Jane" \
              " Austen\n\nThis eBook is for the use of anyone anywhere at no" \
              " cost and with\nalmost no restrictions whatsoever.  You may " \
              "copy it, give it away or\nre-use it under the terms of the " \
              "Project Gutenberg License included\nwith this eBook or online" \
              " at www.gutenberg.org\n\nTitle: Pride and Prejudice\n\n" \
              "Author: Jane Austen\n\nPosting Date: August 26, 2008 [EBook" \
              " #1342]\nRelease Date: June, 1998\nLast Updated: October 17," \
              " 2016\n\nLanguage: English\n\nCharacter set encoding: " \
              "UTF-8\n\n*** START OF THIS PROJECT GUTENBERG EBOOK PRIDE " \
              "AND PREJUDICE ***"

FRONT_PLATE_EXTRA = "\n\nProduced by Anonymous Volunteers\n\nPRIDE AND " \
                    "PREJUDICE\n\nBy Jane Austen\n\n"

FRONT_COPY = "Blah blah blah.\n\nThis text is Copyright Joe Schmoe 2017. All" \
             " rights reserved. If you are reading this, I will have your " \
             "first born son. Bye bye.\n\n\n"

TEXT_NEITHER = "Chapter 1\n\nIt is a truth universally acknowledged, that a" \
               " single man in possession\nof a good fortune, must be in" \
               " want of a wife.\n\n<much text goes here>\n\n*** Testing" \
               " stars ***\n\nWith the Gardiners, they were always on the "\
               " most intimate terms.\nDarcy, as well as Elizabeth, really "\
               "loved them; and they were both ever\nsensible of the warmest" \
               " gratitude towards the persons who, by bringing\nher into "\
               " Derbyshire, had been the means of uniting them.\n\n"

BACK_PLATE = "End of the Project Gutenberg EBook of Pride and Prejudice, by" \
             " Jane Austen\n\n*** END OF THIS PROJECT GUTENBERG EBOOK PRIDE" \
             " AND PREJUDICE ***\n\n***** This file should be named " \
             "1342-0.txt or 1342-0.zip *****\nThis and all associated files" \
             " of various formats will be found in:\n" \
             "        http://www.gutenberg.org/1/3/4/1342/\n\nProduced by" \
             " Anonymous Volunteers\n\nUpdated editions will replace the" \
             " previous one--the old editions\nwill be renamed." \
             "\n\n<explanation of public domain goes here>\n\n*** START:" \
             " FULL LICENSE ***\n\nTHE FULL PROJECT GUTENBERG LICENSE\n" \
             "PLEASE READ THIS BEFORE YOU DISTRIBUTE OR USE THIS WORK\n\n" \
             "<much license goes here>\n\nMost people start at our Web site" \
             " which has the main PG search facility:\n\n     " \
             "http://www.gutenberg.org\n\nThis Web site includes information" \
             " about Project Gutenberg-tm,\nincluding how to make donations" \
             " to the Project Gutenberg Literary\nArchive Foundation, how to" \
             " help produce our new eBooks, and how to\nsubscribe to our" \
             " email newsletter to hear about new eBooks.\n\n"

TEXT_FRONT_PLATE = FRONT_PLATE + FRONT_PLATE_EXTRA + TEXT_NEITHER
TEXT_FRONT_COPY = FRONT_COPY + TEXT_NEITHER
TEXT_BACK = TEXT_NEITHER + BACK_PLATE
TEXT_BOTH_PLATE = TEXT_FRONT_PLATE + BACK_PLATE
TEXT_BOTH_COPY = TEXT_FRONT_COPY + BACK_PLATE
